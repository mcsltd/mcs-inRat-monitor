import copy
import logging
import time
from collections import deque

from queue import Queue, Empty
from threading import Thread, Lock

from PySide6.QtCore import QObject, Signal, Qt

from detector.detector import RealTimeRPeakDetector
from detector.models import CONFIG_HUMAN, ConfigDetector, Subject
from detector.ui.config_pane import FrmConfigDetectorPane
from device.device import SignalDatablock
from device.enums import TypeSignal

logger = logging.getLogger(__name__)

# параметры расчёта ЧСС по объекту исследования
HR_PARAMS = {
    Subject.HUMAN: {"n": 5, "timeout": 5.0, "min_rr": 3},
    Subject.RAT: {"n": 10, "timeout": 3.0, "min_rr": 4},
}


class QrsDetector(QObject):
    """
    Класс детектора RR-пиков ЭКГ сигнала.
    Генерирует события обнаружения пиков.
    События принимаются графиками отображения стрим и классом хранилищем.
    """
    event = Signal(object)
    parentevent = Signal(object)
    signal_enable_changed = Signal(bool)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._config = copy.deepcopy(CONFIG_HUMAN)
        self._receivers = []
        self._input_queue: Queue = Queue()
        self._running: bool = False
        self._worker: Thread | None = None
        self._params: SignalDatablock | None = None
        self._detector_lock = Lock()

        self._fs = 1000

        self._detector = None

        # состояние расчёта ЧСС
        self._last_heart_rate: int | None = None
        self._rr_buffer: deque = deque(maxlen=HR_PARAMS[Subject.HUMAN]["n"])
        self._last_peak_time: float | None = None  # время пика по индексам отсчётов
        self._last_peak_wall: float | None = None  # время пика по wall-clock, для тайм-аута
        self._hr_valid: bool = False
        self._awaiting_recovery: bool = True

        self._configure_hr()

        # ui config
        self._config_pane = FrmConfigDetectorPane(self)

    @property
    def config(self) -> ConfigDetector:
        """ текущий конфиг детектора """
        return self._config

    @property
    def enable(self) -> bool:
        return self._config.enabled

    @enable.setter
    def enable(self, state: bool):
        self._config.enabled = state
        self.signal_enable_changed.emit(state)

    @property
    def config_pane(self) -> FrmConfigDetectorPane | None:
        return self._config_pane

    def process_update(self, config: ConfigDetector):
        """ применение настроек детектора (кнопка Применить) """
        if config is None:
            return
        subject_changed = config.subject != self._config.subject
        self._config = config
        # переинициализация детектора, если ЭКГ уже запущена
        if self._params is not None:
            self._init_detector()
        # параметры расчёта ЧСС зависят от объекта исследования
        if subject_changed:
            self._configure_hr()
        self.signal_enable_changed.emit(self._config.enabled)
        logger.info(f"{self.__class__}: применены настройки детектора {config}")

    def _init_detector(self):
        """ создание детектора r-пиков по текущим параметрам """
        with self._detector_lock:
            self._detector = RealTimeRPeakDetector(
                sampling_rat=self._fs,
                config=self._config,
                init_sec=2
            )
        logger.debug(f"{self.__class__}: детектор RR-пиков активирован")

    def _get_hr_params(self) -> dict:
        """ параметры расчёта ЧСС для текущего объекта исследования """
        return HR_PARAMS.get(self._config.subject, HR_PARAMS[Subject.HUMAN])

    def _configure_hr(self):
        """ (пере)инициализация состояния расчёта ЧСС """
        self._rr_buffer = deque(maxlen=self._get_hr_params()["n"])
        self._last_peak_time = None
        self._last_peak_wall = None
        self._hr_valid = False
        self._awaiting_recovery = True
        self._last_heart_rate = None

    def _on_peak(self, idx_peak: int):
        """ обработка очередного R-пика и расчёт ЧСС """
        t = idx_peak / self._fs
        now = time.monotonic()

        # восстановление после тайм-аута: первый пик только инициализирует отсчёт
        if self._awaiting_recovery:
            self._rr_buffer.clear()
            self._last_peak_time = t
            self._last_peak_wall = now
            self._awaiting_recovery = False
            self._hr_valid = False
            return

        if self._last_peak_time is not None:
            rr = t - self._last_peak_time
            if rr > 0:
                self._rr_buffer.append(rr)

        self._last_peak_time = t
        self._last_peak_wall = now

        if len(self._rr_buffer) >= self._get_hr_params()["min_rr"]:
            mean_rr = sum(self._rr_buffer) / len(self._rr_buffer)
            if mean_rr > 0:
                self._last_heart_rate = int(round(60.0 / mean_rr))
                self._hr_valid = True
                logger.debug(f"hr value: {self._last_heart_rate}")

    def _check_timeout(self):
        """ проверка отсутствия R-пиков: заморозить и пометить ЧСС невалидной """
        if self._last_peak_wall is None:
            return
        if time.monotonic() - self._last_peak_wall > self._get_hr_params()["timeout"]:
            self._hr_valid = False
            self._awaiting_recovery = True

    def update_params(self, params: SignalDatablock | None):
        if params is not None and params.type_signal == TypeSignal.ECG:
            self._params = params
            # recalc param for new fs
            self._fs = params.sample_rate
            self._init_detector()
        else:
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
        if not self._config.enabled:
            return

        if data is None or data["type"] == "ev":
            return

        packet = data["signal"][0,:]  # to mV
        with self._detector_lock:
            if self._detector is None:
                return
            abs_idx_peaks = self._detector.process_packet(packet)

        if abs_idx_peaks:
            logger.debug(f"idx peaks: {abs_idx_peaks}")
            for idx_peak in abs_idx_peaks:
                self._on_peak(idx_peak)
                self.send_event({"type": "RPeakDetected", "data": idx_peak})

        # проверка тайм-аута отсутствия пиков выполняется на каждом пакете
        self._check_timeout()

    def process_start(self):
        """ подготовка к работе: сброс состояния расчёта ЧСС """
        self._configure_hr()

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