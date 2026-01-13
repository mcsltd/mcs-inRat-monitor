import asyncio
import datetime
import logging
import os
from typing import Optional

import pyqtgraph as pg

import numpy as np
from PySide6 import QtAsyncio, QtCore
from PySide6.QtCore import QTimer, Signal
from PySide6.QtGui import QIcon, QFont
from PySide6.QtWidgets import QMainWindow, QApplication, QMessageBox, QComboBox, QFileDialog
from bleak import BLEDevice

from device import RatSens
from config import DATA_PATH
from constants import HZ
from scanner import BLEScannerWorker
from utils.check_bluetooth import check_bluetooth_status
from storage import Storage
from ui.main_window import Ui_MainWindow
from widget import WaitingDialog

logger = logging.getLogger(__name__)


RED = pg.mkPen(color=(255, 0, 0), width=2)


class MainWindow(QMainWindow, Ui_MainWindow):

    signal_connect = Signal()

    def __init__(self, qt_loop: QtAsyncio.QAsyncioEventLoop, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.setWindowTitle("InRat monitor")
        self.setWindowIcon(QIcon("ui/iconMCS.ico"))

        # hide
        self.pushButtonDisconnect.hide()

        self.qt_loop = qt_loop

        # build queue
        self.ecg_queue = asyncio.Queue()

        # data
        self.ecg = np.array([])
        self.time = np.array([])

        # main classes
        self.device: Optional[RatSens] = None
        self.storage = Storage(path_to_save=DATA_PATH, fs=HZ)
        self.scanner = BLEScannerWorker()

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
        self.timer.timeout.connect(lambda: asyncio.ensure_future(self.updatePlot()))

        # create scanner and run it
        self.scanner.run(self.qt_loop)
        self.scanner.signal_found.connect(self.set_combobox_items)
        self.pushButtonConnect.setEnabled(False)

        # setup combobox
        self.comboBoxDevice.setDuplicatesEnabled(False)
        self.comboBoxDevice.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)

        for v in [(0.5, "0.5 s"), (1, "1 s"), (2, "2 s"), (4, "4 s"), (6, "6 s"), (8, "8 s"), (10, "10 s")]:
            self.comboBoxTimebase.addItem(v[1], userData=v[0])
        self.comboBoxTimebase.setCurrentIndex(6)
        self.timebase = self.comboBoxTimebase.currentData()
        self.comboBoxTimebase.currentTextChanged.connect(self.set_timebase)

        # connection
        self.pushButtonConnect.clicked.connect(lambda: asyncio.ensure_future(self.connect_device()))
        self.pushButtonStart.clicked.connect(lambda: asyncio.ensure_future(self.start_device()))
        self.pushButtonStop.clicked.connect(lambda: asyncio.ensure_future(self.stop_device()))
        self.pushButtonRecording.clicked.connect(self.change_recording)
        self.pushButtonSelectDirSave.clicked.connect(self._set_storage)
        self.pushButtonDisconnect.clicked.connect(lambda: asyncio.ensure_future(self.disconnect_device()))
        self.pushButtonShowRecords.clicked.connect(self.open_savedir)

        self.lineEditSave.setText(self.storage.path_to_save) # set default folder
        self.comboBoxFormat.currentTextChanged.connect(self.storage.set_format)

    def set_timebase(self):
        self.timebase = self.comboBoxTimebase.currentData()

    def _set_storage(self):
        path_to_save = QFileDialog.getExistingDirectory(
            self,
            "Select folder",
            self.storage.path_to_save,
            QFileDialog.Option.ShowDirsOnly | QFileDialog.Option.DontResolveSymlinks
        )
        self.storage.set_save_dir(path_to_save)
        self.lineEditSave.setText(path_to_save)

    def open_savedir(self):
        if os.name == 'nt':  # Windows
            os.system(f'start "" "{self.storage.path_to_save}"')
        elif os.name == 'posix':  # Linux, macOS
            os.system(f'open "{self.storage.path_to_save}"')

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
            # self.pushButtonSelectDirSave.setEnabled(True)

            logger.debug("Select stop recording ECG.")

            self.labelRTvalue.setText("00:00:00")
            # check if device running when change button state (when press stop recording)
            if self.device.is_running:
                self.storage.save()
                self.add_marker(pos=self.time[-1], text="Stop recording")

        elif self.storage.is_recording is None or not self.storage.is_recording:
            self.storage.is_recording = True

            self.pushButtonRecording.setText("Stop Recording")

            # deactivate elements when press "Start Recording"
            # self.pushButtonSelectDirSave.setEnabled(False)
            self.comboBoxFormat.setEnabled(False)

            logger.debug("Select start recording ECG.")

            self.add_marker(pos=self.time[-1], text="Start recording")

    async def connect_device(self):
        # raise waiting dialog
        dlg = WaitingDialog(parent=self)
        dlg.show()

        # get device name for connection
        device = self.comboBoxDevice.currentData()
        idx_device = self.comboBoxDevice.currentIndex()
        logger.debug(f"Select device with name: {device.name}.")

        # stop scanner
        self.scanner.stop()
        # remove all device in combobox
        self.comboBoxDevice.clear()
        # disable combobox and button connect
        self.comboBoxDevice.setDisabled(True)
        self.pushButtonConnect.setDisabled(True)

        # reconnect with new device or old
        if self.device is not None and not self.device.is_connected:
            self.device = None
            self.reset()

        try:
            self.device = RatSens(device)
            await self.device.connect()

            # set device info in label
            d_info = await self.device.get_device_information()

            # add in storage device name (for write additional info in edf)
            self.storage.set_device_name(self.device.name)

        except Exception as exc:
            self.device = None
            info = QMessageBox.information(
                self, "Connect error",
                f"An error occurred while connect to the device.\nCheck if the device has turned off.",
                QMessageBox.StandardButton.Ok
            )
            # remove device in combobox if not connected
            self.comboBoxDevice.removeItem(idx_device)
            self.comboBoxDevice.setEnabled(True)
            # run the scanner if can't connect
            self.scanner.run(self.qt_loop)
        else:
            # disable and activate btn state when connect to device
            if self.device.is_connected:
                self.set_device_information(d_info)

                # enable settings for storage
                self.comboBoxFormat.setEnabled(True)
                # self.pushButtonSelectDirSave.setEnabled(True)

                # enable button for start device
                self.pushButtonStart.setEnabled(True)

                self.pushButtonDisconnect.show()
                self.pushButtonConnect.hide()
        finally:
            dlg.close()

    async def disconnect_device(self):
        self.reset()

        if self.device.is_connected:
            await self.device.close()
            self.scanner.run(self.qt_loop)

        else:
            await self.lost_connection()

        # disable
        self.pushButtonStart.setEnabled(False)
        # self.pushButtonSelectDirSave.setEnabled(False)
        self.comboBoxFormat.setEnabled(False)

        # activate
        self.comboBoxDevice.setEnabled(True)

        self.pushButtonConnect.show()
        self.pushButtonDisconnect.hide()

    def set_device_information(self, device_information: Optional[dict] = None):
        if device_information is not None:
            self.labelModelValue.setText(device_information["model"])
            self.labelSerialNumberValue.setText(device_information["serial"])
            self.labelStatusValue.setText(device_information["status"])
            self.labelNameValue.setText(device_information["name"])
            self.labelSFValue.setText("500 Hz")
            self.labelHardwareValue.setText(device_information["hardware"])
            self.labelFirmwareValue.setText(device_information["firmware"])


        else:
            self.labelModelValue.setText("None")
            self.labelSerialNumberValue.setText("None")
            self.labelStatusValue.setText("Not connected")
            self.labelNameValue.setText("None")
            self.labelSF.setText("None")
            self.labelHardwareValue.setText("None")
            self.labelFirmwareValue.setText("None")

    async def start_device(self):
        logger.debug("Start device")

        if not self.device.is_connected:
            info = QMessageBox.information(
                self, "Lost device connection",
                f"Lost connection with device {self.device.name}",
                buttons=QMessageBox.StandardButton.Ok
            )

            # reset all
            await self.lost_connection()
            return

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
            # self.pushButtonConnect.setEnabled(False)
            self.pushButtonDisconnect.setEnabled(False)
            self.comboBoxDevice.setEnabled(False)
            self.pushButtonStart.setEnabled(False)

            # enable
            self.pushButtonRecording.setEnabled(True)
            self.pushButtonStop.setEnabled(True)

            # when draw signal in online - disable mouse
            self.plotWidget.setMouseEnabled(x=False, y=False)

    async def updatePlot(self):
        # check device connection
        if not self.device.is_connected:
            self.timer.stop()  # stop update plot

            info = QMessageBox.information(
                self, "Lost device connection",
                f"Lost connection with device {self.device.name}",
                buttons=QMessageBox.StandardButton.Ok
            )

            # reset all
            await self.lost_connection()

        ecg = await self.ecg_queue.get()
        self.ecg_queue.task_done()

        self.ecg = np.append(self.ecg, ecg["ecg"])
        logger.debug(f"Current {ecg['counter']=}")
        # calculate time
        if len(self.time) == 0:
            self.time = np.arange(1, len(ecg["ecg"]) + 1) * 0.01 # ToDo: check it
        else:
            self.time = np.append(self.time, np.arange(1, len(ecg["ecg"]) + 1) * 1 / HZ + self.time[-1])
        # check shape ecg and time
        if self.ecg.shape != self.time.shape:
            raise ValueError("Arrays time and ecg have not same shape!")

        if self.storage.is_recording:
            self.storage(ecg["ecg"]) # save ecg in storage
            str_time = str(datetime.datetime.now() - self.storage.start_time).split(".")[0]
            str_time = "0" + str_time if len(str_time) != 8 else str_time
            self.labelRTvalue.setText(f"{str_time}")

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

    async def stop_device(self):
        logger.debug("Stop device")

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
            self.pushButtonStart.setEnabled(True)
            self.pushButtonRecording.setEnabled(False)
            self.pushButtonDisconnect.setEnabled(True)
            # when stop device - activate mouse
            self.plotWidget.setMouseEnabled(x=True, y=True)

    async def lost_connection(self):
        """
        Action when lost connection with device.
        :return: None
        """
        logger.info("Lost device connetion.")

        # delete device information
        self.set_device_information()

        await self.device.disconnect()

        # save data in storage
        if self.storage.is_recording:
            self.storage.save()
            self.add_marker(pos=self.time[-1], text="Stop recording")
            self.change_recording()

        # disable button
        self.pushButtonStop.setEnabled(False)
        self.pushButtonStart.setEnabled(False)
        self.pushButtonRecording.setEnabled(False)
        # self.pushButtonSelectDirSave.setEnabled(False)
        self.comboBoxFormat.setEnabled(False)

        # hide disconnet and hide connect
        self.pushButtonDisconnect.hide()
        self.pushButtonConnect.show()

        # when lost connection - activate mouse
        self.plotWidget.setMouseEnabled(x=True, y=True)

        # run scanner
        self.scanner.run(self.qt_loop)

        # activate combobox
        self.comboBoxDevice.setEnabled(True)

    def reset(self) -> None:
        """
        Reset data.
        """
        self.plotWidget.clear()
        self.ecg = np.array([])
        self.time = np.array([])
        self.plot_ecg = self.plotWidget.plot(self.time, self.ecg, pen=RED)
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
        if self.timer.isActive():
            self.pushButtonStop.click()
            self.timer.stop()

        # stop scanner
        self.scanner.stop()

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
        # window.show()
        window.showMaximized()
        loop.run_forever()

    # QtAsyncio.run(handle_sigint=True, debug=True)