import copy
import logging
import time
from collections import deque

import numpy as np
from wfdb.processing import XQRS, xqrs_detect
from queue import Queue, Empty
from threading import Thread

from PySide6.QtCore import QObject, Signal, Qt

from device.device import SignalDatablock
from device.enums import TypeSignal

logger = logging.getLogger(__name__)

class RPeakDetector(QObject):
    """
    Класс детектора RR-пиков ЭКГ сигнала.
    Генерирует события обнаружения пиков.
    События принимаются графиками отображения стрим и классом хранилищем.
    """
    event = Signal(object)
    parentevent = Signal(object)

    CONF_RAT = XQRS.Conf(hr_init=350, hr_max=600, hr_min=150, qrs_width=0.018, ref_period=0.06)
    CONF_RAT = XQRS.Conf(hr_init=350, hr_max=600, hr_min=150, qrs_width=0.018, ref_period=0.06)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._ecg_enable = True
        self._receivers = []
        self._input_queue: Queue = Queue()
        self._running: bool = False
        self._worker: Thread | None = None
        self._params: SignalDatablock | None = None

        self._window_sec = 1
        self._fs = 1000
        self._buffer = deque(maxlen=self._window_sec * self._fs)
        self._window_len = int(self._window_sec * self._fs)
        self._xqrs = None
        # params
        self._refractory_ms = 250
        self._refractory = int(self._refractory_ms * self._fs / 1000)
        self._abs_index = 0
        self._last_peak_abs = -np.inf
        self._peak_times = []
        self._rr_intervals = []

        self._last_heart_rate = 60

    def update_params(self, params: SignalDatablock | None):
        if params is not None and params.type_signal == TypeSignal.ECG:
            self._ecg_enable = True
            self._params = params
            # recalc param for new fs
            self._fs = params.sample_rate
            self._refractory = int(self._refractory_ms * self._fs / 1000)
            self._window_len = int(self._window_sec * self._fs)
            self._buffer = deque(maxlen=self._window_len)
            logger.debug(f"{self.__class__}: детектор RR-пиков активирован")
        else:
            self._ecg_enable = False
            self._params = None
            # self._xqrs = XQRS(conf=self.CONF, fs=params.sample_rate)


    def start(self):
        """ запуск """
        
        try:
            self.process_start()
        except Exception as err:
            pass

        
        if not self._running:
            self._running = True
            self._worker = Thread(target=self._worker_thread)
            self._worker.start()

    def stop(self):
        """ остановка """
        self._running = False
        if self._worker:
            self._worker.join(1.0)
            self._worker = None

    def _worker_thread(self):
        """
        рабочий поток берет данные из входной очереди
        и помещает обработанные данные в выходную очередь
        """
        while self._running:
            try:
                data = self._input_queue.get(False)
                self.process_input(data)
            except Empty:
                data = None
            # except Exception as err:
            #     data = None
            #     logger.error(f"{self.__class__}: {err}")

            # try:
            #     data = self.process_output(data)
            # except Exception as e:
            #     data = None

            # if data:
            #     for rec in self._receivers:
            #         rec._transmit_data(copy.deepcopy(data))

            time.sleep(0.001)

    def process_input(self, data):
        """ метод для получения и обработки данных из входной очереди """
        if not self._ecg_enable or data is None:
            return

        ecg = (data["signal"]).tolist()[0]  # to mV
        self._buffer.extend(ecg)
        self._abs_index += self._params.counter_per_sample

        if len(self._buffer) < self._window_len:    # load buffer
            return

        peaks_rel = xqrs_detect(
            sig=np.array(self._buffer),
            fs=self._fs,
            # conf=self.CONF,
            learn=False, verbose=False
        )
        oldest_abs = self._abs_index - self._window_len + 1
        peaks_abs = oldest_abs + peaks_rel

        for p_abs in peaks_abs:
            if p_abs - self._last_peak_abs < self._refractory:
                continue

            if p_abs > self._last_peak_abs:
                self._last_peak_abs = p_abs
                t = p_abs / self._fs
                self._peak_times.append(t)
                logger.debug(f"{self._peak_times=}")

                if len(self._peak_times) >= 2:
                    self._rr_intervals.append(self._peak_times[-1] - self._peak_times[-2])

                if len(self._peak_times) >= 3:
                    self._last_heart_rate = self._get_heart_rate()
                    self.send_event({"type":"HeartRate", "value": self._last_heart_rate, "counter": p_abs})

    def _get_heart_rate(self) -> float | int:
        """ расчёт чсс """
        dt_rr = self._peak_times[-1] - self._peak_times[-2]
        a = 0.2
        hr = int(a * (60 / dt_rr) + (1 - a) * self._last_heart_rate)
        return hr

    def process_start(self):
        self.send_event({"type": "HeartRate", "value": self._last_heart_rate, "timestamp": 0})

    def process_output(self, data):
        """ метод для передачи обработанных данных в выходную очередь """
        return data

    def _transmit_data(self, data):
        """ отправление данных в очередь """
        try:
            self._input_queue.put(data, False)
        except:
            pass # todo send event error

    def process_event(self, event):
        """ обработка событий"""
        pass

    def add_receiver(self, receiver):
        """ добавить объект приёмника акселерометра в коллекцию """
        if self._running:
            receiver.start()

        if receiver not in self._receivers:
            self._receivers.append(receiver)
            receiver.event.connect(self.receiver_event, Qt.ConnectionType.QueuedConnection)
            self.parentevent.connect(receiver.parent_event, Qt.ConnectionType.QueuedConnection)
        else:
            logger.warning(f"Попытка дублировать {receiver} в приёмниках акселерометра")

    def remove_receiver(self, receiver):
        """ удалить объект приёмника из коллекции акселерометра """
        if receiver in self._receivers:
            self._receivers.remove(receiver)
        receiver.stop()

    def send_event(self, event):
        """ отправить события во все связанные слоты(методы класса) """
        logger.debug(f"Отправка события: {event}")
        self.event.emit(event)
        self.parentevent.emit(event)

    def receiver_event(self, event):
        """ получение событий от прикрепленных приемников """
        self.process_event(event)
        self.event.emit(event)

    def parent_event(self, event):
        """ получение событий от прикрепленного родителя """
        self.process_event(event)
        self.parentevent.emit(event)