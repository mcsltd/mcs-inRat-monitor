import asyncio
from asyncio import AbstractEventLoop

from PySide6.QtCore import QObject, QTimer, Qt, Signal
from PySide6.QtWidgets import QMessageBox
from bleak import BleakScanner

from ble_scanner.ui.dlg_ble_scan import DlgBleScan
from ble_scanner.ui.frm_control_scanner import FrmControlScannerPane
from utils.check_bluetooth import get_bluetooth_error
from utils.scanner import NAME_TEMPLATE


class BleScanner(QObject):
    signal_found = Signal(object)
    signal_connect = Signal(object)
    signal_scan_requested = Signal()
    # результат окна поиска: True - устройство выбрано, False - отмена
    signal_scan_finished = Signal(bool)

    def __init__(self, loop: AbstractEventLoop, parent=None):
        super().__init__(parent)
        self._loop = loop

        self.timer = None
        self._sec_scan_time = 2
        self.event_stop_scan = asyncio.Event()
        self._running: bool = False
        self._seen_names: set[str] = set()
        self._dlg_scan: DlgBleScan | None = None
        self._scan_future = None
        # выбрано ли устройство в окне поиска
        self._selected = False

        self._control_pane = FrmControlScannerPane()
        self._control_pane.pushButtonStart.clicked.connect(self.on_start_clicked)
        # todo connect signal with slot

    def on_start_clicked(self):
        """ запрос поиска и подключения к inRat """
        self.signal_scan_requested.emit()

    def start_scan(self):
        """ запуск поиска и открытие окна выбора устройства """
        bt_error = get_bluetooth_error()
        if bt_error is not None:
            QMessageBox.warning(
                self.parent(),
                "Bluetooth",
                f"{bt_error}\n\n"
                "Включите Bluetooth и повторите попытку поиска."
            )
            return

        self.run()
        self._selected = False

        self._dlg_scan = DlgBleScan(self.parent())
        self._dlg_scan.setWindowModality(Qt.WindowModality.ApplicationModal)
        self._dlg_scan.setModal(True)
        self._dlg_scan.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, True)
        self.signal_found.connect(self._dlg_scan.set_device)
        self._dlg_scan.signal_select.connect(self.on_open_clicked)
        self._dlg_scan.signal_reset.connect(self._on_dlg_reset)
        self._dlg_scan.finished.connect(self._on_dlg_finished)
        self._dlg_scan.open()

    def _on_dlg_reset(self):
        """ очистка списка: сброс дедупликации для повторного поиска устройств """
        self._seen_names = set()

    def _on_dlg_finished(self, result):
        """ очистка после закрытия окна поиска """
        self.stop()
        if self._dlg_scan is not None:
            try:
                self.signal_found.disconnect(self._dlg_scan.set_device)
            except (RuntimeError, TypeError):
                pass
            try:
                self._dlg_scan.signal_reset.disconnect(self._on_dlg_reset)
            except (RuntimeError, TypeError):
                pass
            self._dlg_scan = None
        self.signal_scan_finished.emit(self._selected)

    def on_open_clicked(self, device):
        """ обработка кнопки открытия устройства """
        self.stop()
        if not device:
            return
        self._selected = True
        QTimer.singleShot(700, lambda: self.signal_connect.emit(device))

    @property
    def control_pane(self):
        return self._control_pane

    def set_enabled(self, enable: bool):
        """ блокировка/разблокировка кнопки поиска """
        self._control_pane.set_enabled(enable)

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
                        device.name.startswith(NAME_TEMPLATE) and
                        device.name not in self._seen_names
                ):
                    self._seen_names.add(device.name)
                    self.signal_found.emit(device)

    def run(self):
        if self._running:
            return
        self.timer = 0
        self._seen_names = set()
        self.event_stop_scan.clear()
        self._running = True
        self._scan_future = asyncio.run_coroutine_threadsafe(self._scanning(), self._loop)

    def stop(self):
        self.event_stop_scan.set()
        self._running = False

    def shutdown(self):
        """ остановка поиска с ожиданием завершения корутины сканирования """
        self.stop()
        if self._scan_future is not None and not self._scan_future.done():
            self._scan_future.cancel()
        return self._scan_future
