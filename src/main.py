import asyncio
import datetime
import logging
import os.path
from typing import Optional

import pyqtgraph as pg

import numpy as np
from PySide6 import QtAsyncio, QtCore
from PySide6.QtCore import QTimer, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMainWindow, QApplication, QMessageBox, QComboBox, QFileDialog
from bleak import BLEDevice, BleakScanner

from device import RatSens
from src.config import DATA_PATH
from src.scanner import BLEScannerWorker
from storage import Storage
from ui.main_window import Ui_MainWindow
from widget import WaitingDialog

logger = logging.getLogger(__name__)


SEC_SLIDE_WINDOW = 2
HZ = 500

class MainWindow(QMainWindow, Ui_MainWindow):
    preferences: str = "config.ini"

    signal_connect = Signal()

    def __init__(self, qt_loop: QtAsyncio.QAsyncioEventLoop, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.setWindowTitle("InRat monitor")
        self.setWindowIcon(QIcon("./ui/iconMCS.ico"))

        self.qt_loop = qt_loop
        # build queue
        self.ecg_queue = asyncio.Queue()

        self.ecg = np.array([])
        self.time = np.array([])

        self.device: Optional[RatSens] = None
        self.storage = Storage(path_to_save=DATA_PATH, fs=500)

        # setup plot
        red = pg.mkPen(color=(255, 0, 0))
        green = pg.mkPen(color=(0, 255, 0))
        self.plot_ecg = self.plotWidget.plot(self.time, self.ecg, pen=red)
        self.plotWidget.setLabel("left", "ECG (μV)", pen=pg.mkPen(color='k'))
        self.plotWidget.getAxis("left").setPen(pg.mkPen(color='k'))
        self.plotWidget.getAxis("left").setTextPen(pg.mkPen(color='k'))
        self.plotWidget.setLabel("bottom", "Time (sec)", pen=pg.mkPen(color='k'))
        self.plotWidget.getAxis("bottom").setPen(pg.mkPen(color='k'))
        self.plotWidget.getAxis("bottom").setTextPen(pg.mkPen(color='k'))
        self.plotWidget.addLegend()
        self.plotWidget.setBackground("w")
        self.plotWidget.setDownsampling(auto=True, mode='peak')

        # timer for get ecg from device and draw plot
        self.time_update = 1
        self.timer = QTimer()
        self.timer.setInterval(self.time_update)
        self.timer.timeout.connect(lambda: asyncio.ensure_future(self.updatePlot()))

        # create scanner and run it
        self.scanner = BLEScannerWorker()
        self.scanner.run(self.qt_loop)
        self.scanner.signal_found.connect(self.set_combobox_items)
        self.pushButtonConnect.setEnabled(False)

        # setup combobox
        self.comboBoxDevice.setDuplicatesEnabled(False)
        self.comboBoxDevice.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)

        # connection
        self.pushButtonConnect.clicked.connect(lambda: asyncio.ensure_future(self.connect_device()))
        self.pushButtonStart.clicked.connect(lambda: asyncio.ensure_future(self.start_device()))
        self.pushButtonStop.clicked.connect(lambda: asyncio.ensure_future(self.stop_device()))
        self.pushButtonRecording.clicked.connect(self.change_recording)
        self.pushButtonSelectDirSave.clicked.connect(self._set_storage)

        self.lineEditSave.setText(self.storage.path_to_save) # set default folder
        self.comboBoxFormat.currentTextChanged.connect(self.storage.set_format)


    def _set_storage(self):
        path_to_save = QFileDialog.getExistingDirectory(
            self,
            "Select folder",
            DATA_PATH,
            QFileDialog.Option.ShowDirsOnly | QFileDialog.Option.DontResolveSymlinks
        )
        self.storage.set_save_dir(path_to_save)
        self.lineEditSave.setText(path_to_save)


    def set_combobox_items(self, devices: set[BLEDevice]):
        for device in devices:
            if self.comboBoxDevice.findText(device.name) == -1:
                self.comboBoxDevice.addItem(device.name, userData=device)
        if self.comboBoxDevice.count() != 0:
            self.pushButtonConnect.setEnabled(True)

    def change_recording(self): # ToDo: rename method
        """
        Change state recording.
        """
        if self.storage.is_recording:
            self.storage.is_recording = False

            self.pushButtonRecording.setText("Start Recording")

            # activate elements for setup storage when press "Stop Recording"
            self.comboBoxFormat.setEnabled(True)
            self.pushButtonSelectDirSave.setEnabled(True)

            logger.debug("Select stop recording ECG.")

            # check if device running when change button state (when press stop recording)
            if self.device.is_running:
                self.storage.save()
                self.labelRTvalue.setText(f"[00:00:00]")
                self.add_marker(pos=self.time[-1], text="Stop recording")

        elif self.storage.is_recording is None or not self.storage.is_recording:
            self.storage.is_recording = True

            self.pushButtonRecording.setText("Stop Recording")

            # deactivate elements when press "Start Recording"
            self.pushButtonSelectDirSave.setEnabled(False)
            self.comboBoxFormat.setEnabled(False)

            logger.debug("Select start recording ECG.")

            self.add_marker(pos=self.time[-1], text="Start recording")

    async def connect_device(self):
        # raise waiting dialog
        dlg = WaitingDialog(parent=self)
        dlg.show()

        device = self.comboBoxDevice.currentData()
        idx_device = self.comboBoxDevice.currentIndex()
        logger.debug(f"Select device with name: {device.name}.")

        # if already device is select and connected
        if self.device is not None and device.name == self.device.name:
            return

        # disconnect old ble device
        if self.device is not None and self.device.is_connected:
            await self.device.close()

        try:
            self.device = RatSens(device)
            await self.device.connect()

            # set device info
            d_info = await self.device.get_device_information()

        except Exception as exc:

            # remove device in combobox if not connected
            self.comboBoxDevice.removeItem(idx_device)

            if self.comboBoxDevice.count() == 0:
                self.pushButtonConnect.setEnabled(False)

            info = QMessageBox.information(
                self, "Connect error",
                f"An error occurred while connect to the device\n\nInfo:\n{exc}\n\nPlease, restart application!",
                QMessageBox.StandardButton.Ok
            )

        else:
            # disable and activate btn state when connect to device
            if self.device.is_connected:
                self.set_device_information(d_info)

                # enable settings for storage
                self.comboBoxFormat.setEnabled(True)
                self.pushButtonSelectDirSave.setEnabled(True)

                # enable button for start device
                self.pushButtonStart.setEnabled(True)
        finally:
            dlg.close()

    def set_device_information(self, device_information: Optional[dict] = None):
        if device_information is not None:
            self.labelModelValue.setText(device_information["model"])
            self.labelSerialNumberValue.setText(device_information["serial"])
            self.labelStatusValue.setText(device_information["status"])
            self.labelNameValue.setText(device_information["name"])
        else:
            self.labelModelValue.setText("None")
            self.labelSerialNumberValue.setText("None")
            self.labelStatusValue.setText("Not connected")
            self.labelNameValue.setText("None")

    async def start_device(self):
        logger.debug("Start device")

        # stop scanning
        self.scanner.stop()

        try:
            await self.device.get_ecg(ecg_queue=self.ecg_queue)
        except Exception as exc:
            info = QMessageBox.information(
                self, "Start error",
                f"An error occurred while starting the device\n\nInfo:\n{exc}\n\nPlease, restart application!",
                QMessageBox.StandardButton.Ok
            )
        else:
            self.timer.start()

            # disable
            self.pushButtonConnect.setEnabled(False)
            self.comboBoxDevice.setEnabled(False)
            self.pushButtonStart.setEnabled(False)

            # enable
            self.pushButtonRecording.setEnabled(True)
            self.pushButtonStop.setEnabled(True)

            # when draw signal in online - disable mouse
            self.plotWidget.setMouseEnabled(x=False, y=False)

    async def updatePlot(self):
        ecg = await self.ecg_queue.get()
        self.ecg = np.append(self.ecg, ecg["ecg"])
        self.ecg_queue.task_done()

        # ToDo: check device connection
        logger.debug(f"Current {ecg['counter']=}")

        # calculate time
        if len(self.time) == 0:
            self.time = np.arange(1, len(ecg["ecg"]) + 1) * 0.01
        else:
            self.time = np.append(self.time, np.arange(1, len(ecg["ecg"]) + 1) * 1 / 500 + self.time[-1])

        # check shape ecg and time
        if self.ecg.shape != self.time.shape:
            raise ValueError("Arrays time and ecg have not same shape!")

        # add data in plot
        self.plot_ecg.setData(self.time, self.ecg)

        self.plotWidget.setXRange(max(0, self.time[-1] - SEC_SLIDE_WINDOW), self.time[-1])

        if self.storage.is_recording:
            self.storage(ecg["ecg"]) # save ecg in storage
            str_time = str(datetime.datetime.now() - self.storage.start_time).split(".")[0]
            str_time = "0" + str_time if len(str_time) != 8 else str_time
            self.labelRTvalue.setText(f"[{str_time}]")


    async def stop_device(self):
        logger.debug("Stop device")

        # start scanning
        self.scanner.run(self.qt_loop)

        try:
            await self.device.stop()
        except Exception as exc:
            info = QMessageBox.information(
                self, "Stop error",
                f"An error occurred while stoping the device\n\nInfo:\n{exc}\n\nPlease, restart application!",
                QMessageBox.StandardButton.Ok
            )
        finally:
            self.timer.stop()

            if self.storage.is_recording:
                self.storage.save()
                self.add_marker(pos=self.time[-1], text="Stop recording")
                self.change_recording()

            # activate and disable btn when stop device
            self.pushButtonStop.setEnabled(False)
            self.pushButtonConnect.setEnabled(True)
            self.comboBoxDevice.setEnabled(True)
            self.pushButtonStart.setEnabled(True)
            self.pushButtonRecording.setEnabled(False)
            # self.comboBoxFormat.setEnabled(False)

            # when stop device - activate mouse
            self.plotWidget.setMouseEnabled(x=True, y=True)

    def reset(self) -> None:
        """
        Reset master data.
        :return: None
        """
        self.ecg = np.array([])
        self.time = np.array([])
        self.plot_ecg.setData(self.time, self.ecg)
        self.set_device_information()

    def add_marker(self, pos, text:str="event"):
        """ Add vertical line and text on the plot."""
        line = pg.InfiniteLine(
            pos=pos,
            angle=90,
            pen=pg.mkPen('gray', width=1, style=QtCore.Qt.PenStyle.DashLine),
            movable=False,
            label=text,
            labelOpts={'color': 'k', 'position': 0.1}
        )
        self.plotWidget.addItem(line)

    def closeEvent(self, event):
        self.scanner.stop()
        # while not self.scanner.event_stop_scan.is_set():
        #     ...

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)-15s %(name)-8s %(levelname)s: %(message)s",
    )

    app = QApplication([])
    loop = QtAsyncio.QAsyncioEventLoop(application=app)

    window = MainWindow(loop)

    window.show()
    # window.showMaximized()

    loop.run_forever()
    # QtAsyncio.run(handle_sigint=True, debug=True)