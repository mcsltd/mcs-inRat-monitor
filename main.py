import asyncio
import logging
from asyncio import AbstractEventLoop
from threading import Thread

import numpy as np
import pyqtgraph as pg

from PySide6 import QtAsyncio
from PySide6.QtCore import QTimer, Signal
from PySide6.QtGui import QIcon, QFont
from PySide6.QtWidgets import QMainWindow, QApplication, QMessageBox, QDialog, QWidget, QGridLayout, QFrame

from device.device import Device, DeviceConfigurationPane
from display import DisplayScope
from resources.frm_configuration import Ui_frmConfiguration
from scanner.scanner import BLEScanner
from utils.check_bluetooth import check_bluetooth_status
from resources.main_window import Ui_MainWindow

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow, Ui_MainWindow):

    signal_connect = Signal()

    def __init__(self, loop: AbstractEventLoop, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.setWindowTitle("InRat monitor")
        self.setWindowIcon(QIcon("resources/iconMCS.ico"))

        # hide
        self._loop = loop

        # main classes
        self.device = Device(loop=self._loop)
        self.scanner = BLEScanner(loop=self._loop)
        self.scope = DisplayScope()

        self.scanner.signal_device_selected.connect(self.device.set_device)
        self.device.signal_disconnected.connect(self.scanner.start)
        self.device.signal_data_accepted.connect(self.scope.process_input)

        self.verticalLayout.insertWidget(0, self.scanner.control_panel, 2)
        self.verticalLayout.insertWidget(1, self.device.control_panel, 2)
        self.verticalLayout.addStretch(20)

        self.pushButtonConfig.clicked.connect(self.on_configuration_clicked)

        self.horizontalLayout.addWidget(self.scope)

    def on_configuration_clicked(self):
        dlg = DlgConfiguration()
        dlg.add_tab(self.device.config_panel)
        dlg.exec()


class DlgConfiguration(QDialog, Ui_frmConfiguration):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.tabs = []
        self.buttonBox.clicked.connect(self.close)

    def add_tab(self, tab: QFrame | None):
        self.tabWidget.addTab(tab, "")
        self.tabs.append(tab)
        self.tabWidget.setTabText(self.tabWidget.indexOf(tab), tab.windowTitle())


class ThreadedEventLoop(Thread):
    
    def __init__(self, loop: AbstractEventLoop):
        super().__init__()
        self._loop = loop
        self.daemon = True

    def run(self):
        self._loop.run_forever()

def run_qevent_loop():
    app = QApplication([])
    loop = QtAsyncio.QAsyncioEventLoop(application=app)
    try:
        check_bluetooth_status()
    except Exception as exc:
        info = QMessageBox().information(
            None,"Bluetooth error",f"Bluetooth error\n\nInfo:\n{exc}",
            QMessageBox.StandardButton.Ok
        )
        app.quit()
    else:
        window = MainWindow(loop)
        window.showMaximized()
        loop.run_forever()

def run_async_event_loop():
    app = QApplication([])

    loop = asyncio.new_event_loop()
    asyncio_thread = ThreadedEventLoop(loop)
    asyncio_thread.start()

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
        window.showMaximized()
        app.exec()

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)-15s %(name)-8s %(levelname)s: %(message)s",)
    run_async_event_loop()
    # run_qevent_loop()

