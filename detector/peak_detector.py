import copy
import logging
import time
from collections import deque

from queue import Queue, Empty
from threading import Thread

from PySide6.QtCore import QObject, Signal, Qt

from detector.detector import RealTimeRPeakDetector
from detector.models import ConfigDetector
from detector.ui.config_pane import FrmConfigDetectorPane
from device.device import SignalDatablock
from device.enums import TypeSignal

logger = logging.getLogger(__name__)


CONFIG_HUMAN = ConfigDetector(low_freq=5, high_freq=15, win_sec=0.15,refractory_sec=0.2)
CONFIG_RAT = ConfigDetector(low_freq=5, high_freq=15, win_sec=0.15,refractory_sec=0.2)

class QrsDetector(QObject):
    """
    Класс детектора RR-пиков ЭКГ сигнала.
    Генерирует события обнаружения пиков.
    События принимаются графиками отображения стрим и классом хранилищем.
    """
    event = Signal(object)
    parentevent = Signal(object)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._ecg_enable = True
        self._receivers = []
        self._input_queue: Queue = Queue()
        self._running: bool = False
        self._worker: Thread | None = None
        self._params: SignalDatablock | None = None

        self._fs = 1000

        self._detector = None
        self._last_heart_rate = 60
        self._abs_idx_peaks = deque(maxlen=10)

        # ui config
        self._config_pane = FrmConfigDetectorPane(self)

    @property
    def enable(self) -> bool:
        return self._ecg_enable
    @enable.setter
    def enable(self, state: bool):
        self._ecg_enable = state

    @property
    def config_pane(self) -> FrmConfigDetectorPane | None:
        return self._config_pane

    def update_params(self, params: SignalDatablock | None):
        if params is not None and params.type_signal == TypeSignal.ECG:
            self._params = params
            # recalc param for new fs
            self._fs = params.sample_rate

            detector_human = RealTimeRPeakDetector(
                sampling_rat=self._fs,
                config=CONFIG_HUMAN,
                init_sec=2
            )

            self._detector = detector_human
            logger.debug(f"{self.__class__}: детектор RR-пиков активирован")
        else:
            self._ecg_enable = False
            self._params = None


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

            time.sleep(0.001)

    def process_input(self, data):
        """ метод для получения и обработки данных из входной очереди """
        if not self._ecg_enable:
            return

        if data is None or data["type"] == "ev":
            return

        packet = data["signal"][0,:]  # to mV
        abs_idx_peaks = self._detector.process_packet(packet)

        if len(abs_idx_peaks) == 0:
            return
        logger.debug(f"idx peaks: {abs_idx_peaks}")


        for idx_peak in abs_idx_peaks:
            self._abs_idx_peaks.append(idx_peak)
            self.send_event({"type": "RPeakDetected", "data": idx_peak})

        # if len(self._abs_idx_peaks) > 2:
        #     hr = self._get_heart_rate()
        #     self.send_event({"type": "RPeakDetected", "value": hr, "counter": self._abs_idx_peaks[-1]})

        # for p_abs in peaks_abs:
        #     if p_abs - self._last_peak_abs < self._refractory:
        #         continue
        #
        #     if p_abs > self._last_peak_abs:
        #         self._last_peak_abs = p_abs
        #         t = p_abs / self._fs
        #         self._peak_times.append(t)
        #         logger.debug(f"{self._peak_times=}")
        #
        #         if len(self._peak_times) >= 2:
        #             self._rr_intervals.append(self._peak_times[-1] - self._peak_times[-2])
        #
        #         if len(self._peak_times) >= 3:
        #             self._last_heart_rate = self._get_heart_rate()
        #             self.send_event({"type":"HeartRate", "value": self._last_heart_rate, "counter": p_abs})

    def _get_heart_rate(self) -> float | int:
        """ расчёт чсс """
        dt_rr = (self._abs_idx_peaks[-1] - self._abs_idx_peaks[-2]) / self._fs
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