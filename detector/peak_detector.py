import copy

from wfdb.processing import XQRS
from queue import Queue, Empty
from threading import Thread

from PySide6.QtCore import QObject, Signal

from device.device import SignalDatablock


class RPeakDetector(QObject):
    """
    Класс детектора RR-пиков ЭКГ сигнала.
    Генерирует события обнаружения пиков.
    События принимаются графиками отображения стрим и классом хранилищем.
    """
    event = Signal(object)
    parentevent = Signal(object)

    CONF = XQRS.Conf(hr_init=350, hr_max=600, hr_min=150, qrs_width=0.018, ref_period=0.06)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._ecg_enable = True
        self._receivers = []
        self._input_queue: Queue = Queue()
        self._running: bool = False
        self._worker: Thread | None = None

    def update_params(self, params: SignalDatablock | None):
        pass

    def start(self):
        """ запуск """
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
            except Exception as err:
                raise ValueError(f"АХТУНГ!!! {err}")

            try:
                data = self.process_output()
            except Exception as e:
                data = None

            if data:
                for rec in self._receivers:
                    rec._transmit_data(copy.deepcopy(data))

    def process_input(self, data):
        """ метод для получения и обработки данных из входной очереди """
        pass

    def process_output(self):
        """ метод для передачи обработанных данных в выходную очередь """
        pass

    def _transmit_data(self, data):
        """ отправление данных в очередь """
        try:
            self._input_queue.put(data, False)
        except:
            pass # todo send event error

    def add_receiver(self, receiver):
        pass
    def remove_receiver(self, receiver):
        pass
    def process_event(self, event):
        """ обработка событий"""
        pass

    def send_event(self, event):
        """ отправить события во все связанные слоты(методы класса) """
        self.event.emit(event)
        self.parentevent.emit(event)

    def receiver_event(self, event):
        """ получение событий от прикрепленных приемников """
        self.process_event(event)
        self.event.emit(event)

    def parent_event(self, event):
        """ получение событий от прикрепленного родителя """
        self.parentevent.emit(event)