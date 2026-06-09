import asyncio
import time

from PySide6.QtCore import QObject, Signal
from PySide6 import QtAsyncio
from bleak import BLEDevice, BleakScanner

from utils.scanner import NAME_TEMPLATE


class BLEScannerWorker(QObject):
    signal_found = Signal(set)

    def __init__(self):
        super().__init__()
        self.timer = None
        self._sec_scan_time = 2
        self.event_stop_scan = asyncio.Event()
        self._running: bool = False

    def is_running(self) -> bool:
        return self._running

    async def _scanning(self):
        ble_devices: set[BLEDevice] = set()

        async with BleakScanner() as scanner:
            async for device, advertisement in scanner.advertisement_data():
                if self.event_stop_scan.is_set():
                    return

                if (
                        device is not None and
                        device.name is not None and
                        device.name.startswith(NAME_TEMPLATE)
                ):
                    ble_devices.add(device)

                if time.time() - self.timer > self._sec_scan_time:
                    self.timer = time.time()
                    self.signal_found.emit(ble_devices)

    def run(self, qt_loop: QtAsyncio.QAsyncioEventLoop):
        self.timer = 0
        self.event_stop_scan.clear()
        self._running = True
        asyncio.run_coroutine_threadsafe(self._scanning(), qt_loop)

    def stop(self):
        self.event_stop_scan.set()
        self._running = False
        time.sleep(0.7)
