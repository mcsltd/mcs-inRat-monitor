import asyncio
import datetime
import logging
import os
import numpy as np
import pyqtgraph as pg


from PySide6 import QtAsyncio, QtCore
from PySide6.QtCore import QTimer, Signal, Qt
from PySide6.QtGui import QIcon, QFont
from PySide6.QtWidgets import QMainWindow, QApplication, QMessageBox, QFileDialog

from device.device import Device
from scanner.scanner import BLEScanner
from utils.check_bluetooth import check_bluetooth_status
from resources.main_window import Ui_MainWindow

logger = logging.getLogger(__name__)


RED = pg.mkPen(color=(255, 0, 0), width=2)
HZ = 500

class MainWindow(QMainWindow, Ui_MainWindow):

    signal_connect = Signal()

    def __init__(self, qt_loop: QtAsyncio.QAsyncioEventLoop, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.setWindowTitle("InRat monitor")
        self.setWindowIcon(QIcon("resources/iconMCS.ico"))

        # hide
        self.qt_loop = qt_loop

        # build queue
        self.ecg_queue = asyncio.Queue()

        # data
        self.ecg = np.array([])
        self.time = np.array([])

        # main classes
        self.device = Device(loop=self.qt_loop)
        self.scanner = BLEScanner(loop=self.qt_loop)

        self.scanner.signal_device_selected.connect(self.device.set_device)
        self.device.signal_disconnected.connect(self.scanner.start)
        self.device.signal_data_accepted.connect(self.updatePlot)

        # setup plot
        self.plot_ecg = self.plotWidget.plot(self.time, self.ecg, pen=RED)

        font = QFont()
        font.setPointSize(12)

        self.plotWidget.setLabel("left", "ECG (uV)", pen=pg.mkPen(color='k'), font=font)
        self.plotWidget.getAxis("left").label.setFont(font)
        self.plotWidget.getAxis("left").setPen(pg.mkPen(color='k'))
        self.plotWidget.getAxis("left").setTextPen(pg.mkPen(color='k'))
        self.plotWidget.getAxis("left").setTickFont(font)

        self.plotWidget.setLabel("bottom", "Time (sec)", pen=pg.mkPen(color='k'), font=font)
        self.plotWidget.getAxis("bottom").label.setFont(font)
        self.plotWidget.getAxis("bottom").setPen(pg.mkPen(color='k'))
        self.plotWidget.getAxis("bottom").setTextPen(pg.mkPen(color='k'))
        self.plotWidget.getAxis("bottom").setTickFont(font)

        self.plotWidget.addLegend()
        self.plotWidget.setBackground("w")
        self.plotWidget.setDownsampling(auto=True, mode='peak', ds=50)

        # timer for get ecg from device and draw plot
        self.time_update = 2
        self.timer = QTimer()
        self.timer.setInterval(self.time_update) # in msec
        self.timer.timeout.connect(self.updatePlot)

        self.verticalLayout.insertWidget(0, self.scanner.control_panel, 2)
        self.verticalLayout.insertWidget(1, self.device.control_panel, 2)
        self.verticalLayout.addStretch(10)

        self.timebase = 10


    def updatePlot(self, signal: np.ndarray):
        self.ecg = np.append(self.ecg, signal)

        # calculate time
        if len(self.time) == 0:
            self.time = np.arange(1, len(signal) + 1) * 0.01 # ToDo: check it
        else:
            self.time = np.append(self.time, np.arange(1, len(signal) + 1) * 1 / HZ + self.time[-1])
        # check shape ecg and time
        if self.ecg.shape != self.time.shape:
            raise ValueError("Arrays time and ecg have not same shape!")

        # add data in plot
        self.plot_ecg.setData(self.time, self.ecg, antialias=False, clipToView=True)

        if self.time[-1] < self.timebase:
            self.plotWidget.setXRange(0, self.timebase)
        else:
            self.plotWidget.setXRange(self.time[-1] - self.timebase, self.time[-1])

        slide = self.ecg[- int(self.timebase * HZ):]
        self.plotWidget.setYRange(
            min(slide), max(slide), # padding=0.15
        )

    def reset(self) -> None:
        """
        Reset data.
        """
        self.plotWidget.clear()
        self.ecg = np.array([])
        self.time = np.array([])
        self.plot_ecg = self.plotWidget.plot(self.time, self.ecg, pen=RED)


    def closeEvent(self, event):
        if self.timer.isActive():
            self.timer.stop()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)-15s %(name)-8s %(levelname)s: %(message)s",
    )

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
        window.showMaximized()
        loop.run_forever()

    # QtAsyncio.run(handle_sigint=True, debug=True)