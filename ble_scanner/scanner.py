import asyncio
import time
from asyncio import AbstractEventLoop

from PySide6.QtCore import QObject, Signal
from bleak import BleakScanner

from ble_scanner.ui.dlg_ble_scan import DlgBleScan
from ble_scanner.ui.frm_control_scanner import FrmControlScannerPane
from utils.scanner import NAME_TEMPLATE


class BleScanner(QObject):
    signal_found = Signal(object)
    signal_connect = Signal(object)

    def __init__(self, loop: AbstractEventLoop):
        super().__init__()
        self._loop = loop

        self.timer = None
        self._sec_scan_time = 2
        self.event_stop_scan = asyncio.Event()
        self._running: bool = False

        self._control_pane = FrmControlScannerPane()
        self._control_pane.pushButtonStart.clicked.connect(self.on_start_clicked)
        # todo connect signal with slot

    def on_start_clicked(self):
        """ обработка кнопки поиска и подключения к inRat """
        self.run()

        dlg_scan = DlgBleScan()
        self.signal_found.connect(dlg_scan.set_device)
        dlg_scan.signal_select.connect(self.on_open_clicked)
        dlg_scan.exec()

    def on_open_clicked(self, device):
        """ обработка кнопки открытия устройства """
        self.stop()
        if not device:
            return
        self.signal_connect.emit(device)

    @property
    def control_pane(self):
        return self._control_pane

    def is_running(self) -> bool:
        return self._running

    async def _scanning(self):

        async with BleakScanner() as scanner:
            async for device, advertisement in scanner.advertisement_data():
                if self.event_stop_scan.is_set():
                    return

                if (
                        device is not None and
                        device.name is not None and
                        device.name.startswith(NAME_TEMPLATE)
                ):
                    self.signal_found.emit(device)

    def run(self):
        self.timer = 0
        self.event_stop_scan.clear()
        self._running = True
        asyncio.run_coroutine_threadsafe(self._scanning(), self._loop)

    def stop(self):
        self.event_stop_scan.set()
        self._running = False
        time.sleep(0.7)
