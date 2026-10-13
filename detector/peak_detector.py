import copy
import logging
import time

from queue import Queue, Empty
from threading import Thread

from PySide6.QtCore import QObject, Signal, Qt

from detector.detector import RealTimeQRSDetector
from detector.ui.config_pane import FrmConfigDetectorPane
from device.device import SignalDatablock
from device.enums import TypeSignal

logger = logging.getLogger(__name__)

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

            detector_human = RealTimeQRSDetector(
                sampling_rate=self._fs,
                low_cutoff=5.0,  # Классические частоты Пана-Томпкинса
                high_cutoff=15.0,
                refractory_period_sec=0.25,  # 250 мс (максимальный отслеживаемый пульс 240 уд/мин)
                algorithmic_delay_sec=0.15,  # Задержка 150 мс, чтобы захватить весь комплекс целиком
                threshold_coefficient=0.6,  # Чуть строже к амплитуде
                buffer_duration_sec=3.0
            )

            # detector_rat = RealTimeQRSDetector(
            #     sampling_rate=self._fs,          # Ваша частота
            #     low_cutoff=15.0,             # Режем дыхание и базовую линию
            #     high_cutoff=50.0,            # Оставляем только быстрый спад/подъем R-волны
            #     refractory_period_sec=0.07,  # 70 мс (максимальный отслеживаемый пульс ~850 уд/мин)
            #     algorithmic_delay_sec=0.04,  # Окно задержки всего 40 мс
            #     threshold_coefficient=0.5
            # )


            self._detector = detector_human
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
        if not self._ecg_enable:
            return

        if data is None or data["type"] == "ev":
            return

        packet = data["signal"][0,:]  # to mV
        logger.debug(f"Founded peaks: {self._detector.process_packet(packet)}")

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