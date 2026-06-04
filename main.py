import asyncio
import datetime
import logging
import time
from threading import Thread
from typing import Optional

import pyqtgraph as pg


from PySide6 import QtAsyncio
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QMainWindow, QApplication, QMessageBox, QComboBox
from bleak import BLEDevice

from device.device import inRatDevice
from scanner import BLEScannerWorker
from stream_displays import StreamViewer
from utils.check_bluetooth import check_bluetooth_status
from storage import DataStorage
from resources.main_window import Ui_MainWindow
from widget import WaitingDialog

logger = logging.getLogger(__name__)




class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, qt_loop: QtAsyncio.QAsyncioEventLoop, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)

        # hide
        self.pushButtonDisconnect.hide()
        self.qt_loop = qt_loop

        # main classes
        self.device = inRatDevice(qt_loop)
        self.device.signal_connected.connect(self.on_device_connected)
        self.device.signal_disconnected.connect(self.on_device_disconnected)

        self.scanner = BLEScannerWorker()
        self.storage = DataStorage()
        self.display_ecg_emg = StreamViewer()

        # self.verticalLayout.insertWidget(6, self.storage.control_pane)

        self.device.add_receiver(self.display_ecg_emg)

        # create scanner and run it
        self.scanner.run(self.qt_loop)
        self.scanner.signal_found.connect(self.set_combobox_items)
        self.pushButtonConnect.setEnabled(False)

        self._waiting_connection_dlg = WaitingDialog()

        # setup combobox
        self.comboBoxDevice.setDuplicatesEnabled(False)
        self.comboBoxDevice.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)
        self.verticalLayout.insertWidget(5, self.device.control_pane)
        self.verticalLayoutDisplay.addWidget(self.display_ecg_emg)

        # connection
        self.pushButtonConnect.clicked.connect(self.on_connect_clicked)
        self.pushButtonDisconnect.clicked.connect(self.on_disconnect_clicked)

    def on_connect_clicked(self):
        """ обработка нажатия кнопки открытия устройства """
        self._waiting_connection_dlg.show()
        self.scanner.stop()

        device = self.comboBoxDevice.currentData()
        self.device.process_connect(device)

        self.comboBoxDevice.setDisabled(True)
        self.pushButtonConnect.setDisabled(True)

    def on_device_connected(self):
        """ обработка случая подключения устройства """
        self._waiting_connection_dlg.close()
        self.pushButtonConnect.hide()
        self.pushButtonDisconnect.setVisible(True)
        self.pushButtonDisconnect.setEnabled(True)

    def on_disconnect_clicked(self):
        """ обработка нажатия кнопки отсоединения от устройства """
        self.scanner.run(self.qt_loop)
        self.device.process_disconnect()

    def on_device_disconnected(self):
        """ обработка случая если устройство отсоединено """
        self.pushButtonDisconnect.hide()
        self.pushButtonConnect.setVisible(True)
        self.comboBoxDevice.clear()
        self.comboBoxDevice.setEnabled(True)


    def set_combobox_items(self, devices: set[BLEDevice]):
        for device in devices:
            if self.comboBoxDevice.findText(device.name) == -1:
                self.comboBoxDevice.addItem(device.name, userData=device)
        if self.comboBoxDevice.count() != 0:
            self.pushButtonConnect.setEnabled(True)

    def closeEvent(self, event):
        self.scanner.stop()

if __name__ == "__main__":
    # logging.basicConfig(
    #     level=logging.DEBUG,
    #     format="%(asctime)-15s %(name)-8s %(levelname)s: %(message)s",
    # )

    app = QApplication([])
    loop = QtAsyncio.QAsyncioEventLoop(application=app)

    try:
        check_bluetooth_status()
    except Exception as exc:
        info = QMessageBox().information(
            None,
            "Bluetooth error",
            f"Bluetooth error\n\nInfo:\n{exc}",
            QMessageBox.StandardButton.Ok
        )
        app.quit()
    else:
        window = MainWindow(loop)
        # window.show()
        window.showMaximized()
        loop.run_forever()

    # QtAsyncio.run(handle_sigint=True, debug=True)