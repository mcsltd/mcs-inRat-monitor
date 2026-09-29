from wfdb.processing import XQRS
from queue import Queue
from threading import Thread

from PySide6.QtCore import QObject


class RPeakDetector(QObject):

    """
    Класс детектора RR-пиков ЭКГ сигнала.
    Генерирует события обнаружения пиков.
    События принимаются графиками отображения стрим и классом хранилищем.
    """

    CONF = XQRS.Conf(hr_init=350, hr_max=600, hr_min=150, qrs_width=0.018, ref_period=0.06)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._receivers = []
        self._input_queue: Queue = Queue()
        self._running: bool = False
        self._worker: Thread | None = None

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
        """ обработка рабочего потока """
        while self._running:
            try:
                data = self._input_queue.get(False)
                self.process_input(data)
            except TimeoutError:
                data = None
            except Exception as err:
                raise ValueError(f"АХТУНГ!!! {err}")

            if data:
                for rec in self._receivers:
                    rec._transmit_data(data)

    def process_input(self, data):
        """ обработка входа """
        pass

    def _transmit_data(self, data):
        """ отправление данных в очередь """
        pass
