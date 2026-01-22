import asyncio
import logging

from asyncio import AbstractEventLoop
from concurrent.futures import Future

from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QFrame
from bleak import AdvertisementData, BLEDevice, BleakScanner

from resources.frm_online_scanner import Ui_FrmScanner

logger = logging.getLogger(__name__)

class BLEScanner(QObject):

    signal_device_detected = Signal(object)

    def __init__(self, loop: AbstractEventLoop, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._loop: AbstractEventLoop = loop
        self._scan_future: None | Future = None
        self._control_panel = OnlineControlPanel(self)

        self.signal_device_detected.connect(self._control_panel.set_device)
        self._control_panel.pushButtonOpen.clicked.connect(self.stop)

        self.start()

    def start(self):
        """ Запуск сканера для обнаружения устройств с префиксом inRat-1"""
        future = asyncio.run_coroutine_threadsafe(self._scan(), self._loop)
        self._scan_future = future

        if self._scan_future.running():
            logger.info("Запущен BLE сканер")

    async def _scan(self, template: str = "inRat-1"):
        """ Сканирование сети """
        def detection_callback(device: BLEDevice, advertisement_data: AdvertisementData):
            if device.name and device.name.startswith(template):
                logger.debug(f"{device} {advertisement_data=}")
                self.signal_device_detected.emit(device)

        async with BleakScanner(detection_callback=detection_callback) as scanner:
            while True:
                await asyncio.sleep(1)

    def stop(self):
        """ Остановка сканера """
        logger.info("Остановка BLE сканера")
        if self._scan_future:
            self._loop.call_soon_threadsafe(self._scan_future.cancel)
        self.control_panel.reset()

    @property
    def control_panel(self):
        return self._control_panel


class OnlineControlPanel(QFrame, Ui_FrmScanner):

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent=None, *args, **kwargs)
        self.setupUi(self)
        self._detected_device = set()

    def set_device(self, device: BLEDevice):
        if device not in self._detected_device:
            self.comboBoxDevice.addItem(device.name, userData=device)
            self.pushButtonOpen.setEnabled(True)
        self._detected_device.add(device)

    def reset(self):
        self._detected_device.clear()
        self.comboBoxDevice.clear()
        self.comboBoxDevice.setEnabled(True)
        self.pushButtonOpen.setEnabled(False)

