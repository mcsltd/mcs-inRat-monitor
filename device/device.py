import asyncio
from asyncio import AbstractEventLoop
from threading import Thread

from PySide6.QtCore import QObject


class inRatDevice(QObject):
    """ класс для работы с inRat """
    def __init__(self, loop: asyncio.AbstractEventLoop | None = None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._inrat = None

        self._loop: AbstractEventLoop = loop
        self._work: Thread | None = None
        self._running: bool = False

    def start(self):
        """ запуск inRat на получение данных """
        if not self._running:
            self._running = True
            self._work = Thread(target=self._worker_thread)

    def _worker_thread(self):
        """ Рабочий поток получает данные из входной очереди
            и помещает обработанные данные в выходную очередь """
        while self._running:
            ...

    def stop(self):
        """ остановка получения данных с inRat """
        self._running = False
        if self._work:
            self._work.join(5.0)
            self._work = None