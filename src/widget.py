import asyncio
from typing import Optional

from PySide6.QtCore import Signal
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QDialog, QMessageBox, QVBoxLayout, QLabel, QProgressBar

from ui.dlg_enter_device_info import Ui_Form


class EnterDeviceInfoDialog(QDialog, Ui_Form):

    """
    Dialog box for entering information about the device.
    """

    signal_connect = Signal(dict)
    signal_save = Signal(dict)

    def __init__(
            self, parent=None,
            serial=None, # from initial settings if it set
            *args, **kwargs
    ):
        super().__init__(parent, *args, **kwargs)
        self.setupUi(self)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)

        if serial is not None:
            self.lineEditSNValue.setText(str(serial))

        self.pushButtonSave.clicked.connect(self.save_device_info)
        self.pushButtonConnect.clicked.connect(self.connect_to_device)

    def connect_to_device(self):
        device_info = self.get_device_info()
        if device_info["serial"] is not None:
            self.signal_connect.emit(device_info)
        self.close()

    def save_device_info(self):
        device_info = self.get_device_info()
        if device_info["serial"] is not None:
            self.signal_save.emit(device_info)


    def get_device_info(self) -> dict:
        """
        Get device info from line edit
        :return:
        """
        device_info = {"serial": None}

        sn = self.lineEditSNValue.text()
        if sn == "":
            info = QMessageBox.information(
                self, "Warning!",
                f"Empty Serial Number field!",
                QMessageBox.StandardButton.Ok
            )
            return device_info

        device_info["serial"] = sn

        return device_info



class WaitingDialog(QDialog):

    def __init__(self, event_scanning: Optional[asyncio.Event]=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Waiting for connection")
        self.setWindowModality(Qt.WindowModality.ApplicationModal)

        self.setFixedSize(300, 150)
        self.event_scanning = event_scanning
        layout = QVBoxLayout()

        self.label = QLabel("Please wait for the device to connect...")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.progress = QProgressBar()
        self.progress.setRange(0, 0)

        layout.addWidget(self.label)
        layout.addWidget(self.progress)

        self.setLayout(layout)

    def closeEvent(self, event):
        if self.event_scanning is not None:
            self.event_scanning.set()