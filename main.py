import asyncio
import logging
from asyncio import AbstractEventLoop
from threading import Thread

import numpy as np
import pyqtgraph as pg


from PySide6 import QtAsyncio, QtCore
from PySide6.QtCore import QTimer, Signal, Qt
from PySide6.QtGui import QIcon, QFont
from PySide6.QtWidgets import QMainWindow, QApplication, QMessageBox, QFileDialog

from device.device import inRatDevice
from scanner.scanner import BLEScanner
from utils.check_bluetooth import check_bluetooth_status
from resources.main_window import Ui_MainWindow
from widget import WaitingDialog

logger = logging.getLogger(__name__)


RED = pg.mkPen(color=(255, 0, 0), width=2)
HZ = 500

class MainWindow(QMainWindow, Ui_MainWindow):

    signal_connect = Signal()

    def __init__(self, loop: AbstractEventLoop, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.setWindowTitle("InRat monitor")
        self.setWindowIcon(QIcon("resources/iconMCS.ico"))

        self._loop = loop

        # main classes
        self.device = inRatDevice(loop=self._loop)
        self.scanner = BLEScanner(loop=self._loop)
        # ToDo: self.display = ...
        # ToDo: self.storage = ...

        self.scanner.signal_device_selected.connect(self.device.process_connect)
        self.device.device_info.connect(self.on_device_info_received)
        self.device.device_disconnected.connect(self.scanner.start)

        self.verticalLayout.insertWidget(0, self.scanner.control_panel, 2)
        self.verticalLayout.insertWidget(1, self.device.control_panel, 2)
        self.verticalLayout.addStretch(10)

        self.timebase = 10

    def on_device_info_received(self, info: str):
        msg_box = QMessageBox.information(self, "Информация", info, buttons=QMessageBox.StandardButton.Ok)


class ThreadedEventLoop(Thread):
    
    def __init__(self, loop: AbstractEventLoop):
        super().__init__()
        self._loop = loop
        self.daemon = True

    def run(self):
        self._loop.run_forever()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)-15s %(name)-8s %(levelname)s: %(message)s",)
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
