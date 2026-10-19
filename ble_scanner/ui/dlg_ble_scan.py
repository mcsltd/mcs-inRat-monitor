from PySide6.QtCore import Signal
from PySide6.QtWidgets import QDialog
from bleak import BLEDevice

from ble_scanner.res.dlg_ble_scan_device import Ui_DlgBleScan


class DlgBleScan(QDialog, Ui_DlgBleScan):
    """ Диалоговое окно для вывода устройств """
    signal_select = Signal(object)
    signal_select_camera = Signal(object)  # название камеры (str) или None
    # очистка списка найденных устройств
    signal_reset = Signal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)

        self._founded_device = {}

        self.pushButtonOpen.clicked.connect(self._on_open_clicked)
        self.pushButtonReset.clicked.connect(self._on_reset_clicked)

    def set_device(self, device: BLEDevice):
        """ отображение найденных устройств """
        if device.name not in self._founded_device:
            self._founded_device[device.name] = device
            self.listWidgetFoundDevice.addItem(device.name)
            self.pushButtonOpen.setEnabled(True)
            self.pushButtonReset.setEnabled(True)
        return

    def _on_open_clicked(self):
        """ обработка кнопки подключения устройства """
        item = self.listWidgetFoundDevice.currentItem()
        if item is None:
            return
        self.signal_select.emit(self._founded_device[item.text()])
        self.close()

    def _on_reset_clicked(self):
        """ обработка кнопки подключения устройства """
        self._founded_device.clear()
        self.listWidgetFoundDevice.clear()
        self.pushButtonReset.setEnabled(False)
        self.pushButtonOpen.setEnabled(False)
        self.signal_reset.emit()

    def closeEvent(self, arg__1, /):
        """ обработка закрытия окна """
        self.signal_select.emit(None)
