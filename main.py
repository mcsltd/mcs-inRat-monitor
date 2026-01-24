import asyncio
import datetime
import logging
import os
import numpy as np
import pyqtgraph as pg

from typing import Optional

from PySide6 import QtAsyncio, QtCore
from PySide6.QtCore import QTimer, Signal, Qt
from PySide6.QtGui import QIcon, QFont
from PySide6.QtWidgets import QMainWindow, QApplication, QMessageBox, QFileDialog

from config import DATA_PATH
from device.device import Device
from scanner.scanner import BLEScanner
from utils.check_bluetooth import check_bluetooth_status
from storage import Storage
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

        self.storage = Storage(path_to_save=DATA_PATH, fs=HZ)
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
        # setup combobox

        for v in [(0.5, "0.5 s"), (1, "1 s"), (2, "2 s"), (4, "4 s"), (6, "6 s"), (8, "8 s"), (10, "10 s")]:
            self.comboBoxTimebase.addItem(v[1], userData=v[0])
        self.comboBoxTimebase.setCurrentIndex(6)
        self.timebase = self.comboBoxTimebase.currentData()
        self.comboBoxTimebase.currentTextChanged.connect(self.set_timebase)

        # connection
        self.pushButtonRecording.clicked.connect(self.change_recording)
        self.pushButtonSelectDirSave.clicked.connect(self._set_storage)
        self.pushButtonShowRecords.clicked.connect(self.open_savedir)

        self.lineEditSave.setText(self.storage.path_to_save) # set default folder
        self.comboBoxFormat.currentTextChanged.connect(self.storage.set_format)

        self.verticalLayout.insertWidget(0, self.scanner.control_panel, 2)
        self.verticalLayout.insertWidget(1, self.device.control_panel, 2)

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
            self.timer.stop()

        # # stop scanner
        # self.scanner.stop()

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