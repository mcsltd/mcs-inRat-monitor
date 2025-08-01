import asyncio

from PySide6.QtCore import QObject, Signal
from PySide6 import QtAsyncio
from bleak import BLEDevice, BleakScanner

from src.utils.scanner import NAME_TEMPLATE


class BLEScannerWorker(QObject):
    signal_found = Signal(BLEDevice)

    def __init__(self):
        super().__init__()

    async def _scanning(self):
        async with BleakScanner() as scanner:
            async for device, advertisement in scanner.advertisement_data():
                if device is not None and device.name is not None and device.name.startswith(NAME_TEMPLATE):
                    self.signal_found.emit(device)

    def run(self, qt_loop: QtAsyncio.QAsyncioEventLoop):
        # ToDo: watch another variant
        asyncio.run_coroutine_threadsafe(self._scanning(), qt_loop)