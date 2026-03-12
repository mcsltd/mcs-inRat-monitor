import asyncio
import copy
import logging
import threading
import time
from asyncio import AbstractEventLoop, Future, QueueShutDown, QueueEmpty
from threading import Thread

import numpy as np
from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QDialog
from bleak import BLEDevice

from device.constants import Pkt
from device.inrat import inRat
from resources.frm_online_device import Ui_FrmDevice
# from ui.waiting_dialog import WaitingDialog

logger = logging.getLogger(__name__)


class ECG_DataBlock:
    def __init__(self):
        self.sample_rate = 500.0
        self.sample_counter = 0
        self.ecg_channels = np.zeros(Pkt.SamplesCountEcg)

    def __repr__(self):
        return f"{self.sample_rate} Гц; {self.sample_counter}; ecg={self.ecg_channels}"

class inRatDevice(QObject):

    device_connected = Signal()
    device_disconnected = Signal()
    device_info = Signal(str)

    def __init__(self, loop: AbstractEventLoop, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._inrat: inRat | None = None

        # ui elements
        self._control_panel = DlgControlPanel()
        self._control_panel.pushButtonStart.clicked.connect(self.start)
        self._control_panel.pushButtonStop.clicked.connect(self.stop)
        self._control_panel.pushButtonDisconnect.clicked.connect(self.process_disconnect)

        self._async_queue = asyncio.Queue()
        self.datablock = ECG_DataBlock()


        self._receivers = []
        self._running: bool = False
        self._loop: AbstractEventLoop = loop
        self._work: None | Thread = None

    # properties
    @property
    def control_panel(self):
        return self._control_panel

    def process_connect(self, inrat: BLEDevice, wait: float = 10.0):
        """ метод обработки соединения с устройством """
        self._inrat = inRat(inrat)
        future = asyncio.run_coroutine_threadsafe(self._inrat.connect(wait=wait), self._loop)
        future.add_done_callback(self.on_device_connected)
    def on_device_connected(self, future: Future):
        """ метод обработки результата соединения """
        result, msg = future.result()
        if result and self.device_connected:
            logger.debug(f"info: {result}; msg: {msg}")
            self.device_connected.emit()
            # enable start
            self._control_panel.pushButtonDisconnect.setEnabled(True)
            self._control_panel.pushButtonStart.setEnabled(True)
            self._control_panel.groupBox.setTitle(self._inrat.name)
            return
        self.device_info.emit(msg)
        self.device_disconnected.emit()


    def start(self):
        """ метод запуска inRat на получение данных """
        # очистка очереди
        while not self._async_queue.empty():
            self._async_queue.get_nowait()

        # запуск прикрепленных классов приемников данных
        for receiver in self._receivers:
            receiver.start()

        res = self.process_start()
        if not self._running and res:
            self._running = True
            self._work = threading.Thread(target=self._worker_thread)
            self._work.start()


    def process_start(self):
        """ метод для запуска inRat """
        logger.debug("запуск inRat")
        future = asyncio.run_coroutine_threadsafe(self._inrat.start_acquisition(self._async_queue), self._loop)
        self._control_panel.pushButtonStart.setEnabled(False)
        try:
            res, msg = future.result(timeout=10)
            if not res:
                self.device_info.emit(msg)
            self._control_panel.pushButtonStop.setEnabled(True)
        except TimeoutError:
            logger.debug("Время запуска устройства истекло")
            self._control_panel.pushButtonStart.setEnabled(True)
            return False
        except Exception as err:
            logger.debug(f"При запуске возникла ошибка: {err}")
            self._control_panel.pushButtonStart.setEnabled(True)
            return False
        return True

    def _worker_thread(self):
        logger.debug("Запуск асинхронного обработчика событий")
        while self._running:

            try:
                data = self._async_queue.get_nowait()
            except (QueueShutDown, QueueEmpty):
                data = None

            if data:
                data = self.process_output(data)
                logger.debug(f"{data=}")
        # todo: process_idle()

    def process_output(self, data: dict) -> ECG_DataBlock | None:
        if data["type"] == "signal":
            self.datablock.ecg_channels = data.get("signal")
            self.datablock.sample_counter = data.get("counter")
            ecg = copy.copy(self.datablock)
            return ecg
        return None

    def stop(self):
        """ метод остановки получения данных с inRat """
        # остановка цикла обработки очереди
        self._running = False
        if self._work:
            self._work.join(5.0)
            self._work = None

        # остановить все классы-приёмники
        for receiver in self._receivers:
            receiver.stop()

        self.process_stop()

    def process_stop(self):
        """ метод остановки устройства """
        future = asyncio.run_coroutine_threadsafe(self._inrat.stop_acquisition(), self._loop)
        future.add_done_callback(self._on_device_stopped)
    def _on_device_stopped(self, future):
        """ обработка результата задачи остановки устройства """
        self._control_panel.pushButtonStart.setEnabled(True)
        self._control_panel.pushButtonStop.setDisabled(True)



    def process_disconnect(self):
        """ метод обработчик отключения от inRat """
        if self._running:
            self.stop()
        future = asyncio.run_coroutine_threadsafe(self._inrat.disconnect(), self._loop)
        future.add_done_callback(self.on_device_disconnected)
    def on_device_disconnected(self, future):
        """ коллбек-обработчик результата отключения от inRat """
        result, msg = future.result()
        if result and not self._inrat.is_connected:
            self.device_disconnected.emit()
            self._inrat = None
            self._control_panel.disable()
            return
        self.device_info.emit(msg)


class DlgControlPanel(QDialog, Ui_FrmDevice):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.setupUi(self)

    def disable(self):
        self.pushButtonStart.setDisabled(True)
        self.pushButtonStop.setDisabled(True)
        self.pushButtonDisconnect.setDisabled(True)