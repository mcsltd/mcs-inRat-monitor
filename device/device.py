import asyncio
import logging
import queue
import time
from asyncio import AbstractEventLoop
from concurrent.futures import Future
from threading import Thread

from PySide6.QtCore import QObject, Signal
from bleak import BLEDevice

from device.enums import EnabledChannels
from device.inrat import inRat, FIRMWARE_V1, FIRMWARE_V0
from device.ui.config_dialog import DlgConfigDevice
from device.ui.control_pane import FrmControlPane

logger = logging.getLogger(__name__)

class inRatDevice(QObject):

    signal_connected = Signal()
    signal_disconnected = Signal()

    """ класс для работы с inRat """
    def __init__(self, loop: asyncio.AbstractEventLoop | None = None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._inrat = None
        self._receivers = []

        self._signal_queue = asyncio.Queue()
        self._event_queue = None
        self._acc_queue = None

        self._loop: AbstractEventLoop = loop
        self._work: Thread | None = None
        self._running: bool = False

        self._control_pane = FrmControlPane()
        self._control_pane.pushButtonStart.clicked.connect(self.start)
        self._control_pane.pushButtonStop.clicked.connect(self.stop)
        self._control_pane.pushButtonConfig.clicked.connect(self.on_config_clicked)

    def add_receiver(self, receiver):
        """ добавить объект приёмника в коллекцию """
        if self._running:
            receiver.start()
        self._receivers.append(receiver)

    def remove_receiver(self, receiver):
        self._receivers.remove(receiver)
        receiver.stop()

    @property
    def control_pane(self):
        return self._control_pane

    def process_connect(self, device: BLEDevice):
        """ обработка соединения с inRat """
        self._inrat = inRat(ble_device=device)
        future = asyncio.run_coroutine_threadsafe(self._inrat.connect(), self._loop)
        future.add_done_callback(self.on_device_connected)

    def on_device_connected(self, future: Future):
        """ обработка результата соединения с устройством """
        if self._inrat.is_connected:
            self._control_pane.state_connection()
            self.signal_connected.emit()

            if self._inrat.firmware == FIRMWARE_V0:
                self._inrat.enabled_channels = EnabledChannels.ECG
                self._inrat.sample_rate = 500
                self._inrat.activity_threshold = 2

            if self._inrat.firmware == FIRMWARE_V1:
                self._inrat.enabled_channels = EnabledChannels.ECG | EnabledChannels.ACC_X | EnabledChannels.ACC_Z | EnabledChannels.ACC_Y
                self._inrat.sample_rate = 500
                self._inrat.activity_threshold = 2

        else:
            self._control_pane.state_disconnect()

    def process_disconnect(self):
        """ обработка соединения с inRat """
        future = asyncio.run_coroutine_threadsafe(self._inrat.disconnect(), self._loop)
        self.signal_disconnected.emit()
        self._control_pane.state_disconnect()

    def process_start(self):
        """ обработка запуска устройства """
        self._control_pane.state_acquisition()

    def start(self):
        """ запуск inRat на получение данных """
        try:
            self.process_start()
        except Exception as exc:
            logger.error(f"Exception: {exc}")
            return

        future = asyncio.run_coroutine_threadsafe(self._inrat.start_acquisition(signal_queue=self._signal_queue), self._loop)

        for receiver in self._receivers:
            receiver.update_params(
                channels=1, counter_per_sample=32, sample_rate=500, type_signal="ЭЭГ")
            receiver.start()

        if not self._running:
            self._running = True
            self._work = Thread(target=self._worker_thread)
            self._work.start()
        logger.debug("Запущен поток обработки приёма и обработки данных с inRat")

    def _worker_thread(self):
        """ Рабочий поток получает данные из входной очереди
            и помещает обработанные данные в выходную очередь """
        while self._running:
            try:
                signal = self._signal_queue.get_nowait()
            except asyncio.queues.QueueEmpty:
                signal = None
            else:
                # logger.debug(f"Получены данные: {signal=}")
                self._signal_queue.task_done()

            if signal:
                for receiver in self._receivers:
                    receiver._transmit_data(signal)

            time.sleep(0.001)


    def stop(self):
        """ остановка получения данных с inRat """
        future = asyncio.run_coroutine_threadsafe(self._inrat.stop_acquisition(), self._loop)

        self._running = False
        if self._work:
            self._work.join(5.0)
            self._work = None

        for receiver in self._receivers:
            receiver.stop()

        self.process_stop()
        logger.debug("Поток обработки приёма и обработки данных с inRat остановлен")

    def process_stop(self):
        """ обработка остановки устройства """
        self._control_pane.state_connection()

    def on_config_clicked(self):
        dlg = DlgConfigDevice(self._inrat)
        dlg.exec()

