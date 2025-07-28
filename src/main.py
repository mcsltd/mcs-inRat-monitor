import asyncio
import logging
import os
from configparser import ConfigParser
from typing import Optional

import pyqtgraph as pg

import numpy as np
from PySide6 import QtAsyncio, QtCore
from PySide6.QtCore import QTimer, Qt, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMainWindow, QApplication, QDialog, QVBoxLayout, QLabel, QProgressBar, QMessageBox

from device import RatSens
from storage import Storage
from ui.dlg_enter_device_info import Ui_Form
from ui.main_window import Ui_MainWindow
from utils.scanner import find_device
from widget import EnterDeviceInfoDialog, WaitingDialog

logger = logging.getLogger(__name__)


SEC_SLIDE_WINDOW = 2



class MainWindow(QMainWindow, Ui_MainWindow):
    preferences: str = "config.ini"

    signal_connect = Signal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.setWindowTitle("InRat monitor")
        self.setWindowIcon(QIcon("./ui/iconMCS.ico"))

        self.ecg = np.array([])
        self.time = np.array([])

        self.device: Optional[RatSens] = None
        self.device_info: Optional[dict] = self.get_preferences()

        self.ecg_queue = asyncio.Queue()

        self.is_save_ecg = None
        self.storage = Storage()

        self.pushButtonManage.clicked.connect(lambda: asyncio.ensure_future(self.connect_device()))
        self.pushButtonStart.clicked.connect(lambda: asyncio.ensure_future(self.start_device()))
        self.pushButtonStop.clicked.connect(lambda: asyncio.ensure_future(self.stop_device()))
        self.pushButtonRecording.clicked.connect(self.change_recording)
        self.comboBoxFormat.currentTextChanged.connect(self.storage.set_format)

        # setup plot
        pen = pg.mkPen(color=(255, 0, 0))
        self.plot_ecg = self.plotWidget.plot(self.time, self.ecg, pen=pen)
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

        self.enter_device_info()

    def enter_device_info(self):
        serial = None

        # check if device info already exists
        if self.device_info is not None:
            serial=self.device_info["serial"]

        dlg = EnterDeviceInfoDialog(
            self,
            serial=serial
        )
        dlg.signal_save.connect(self.save_preferences)
        dlg.signal_connect.connect(self.set_device_info_and_connect)
        dlg.show()

    def get_preferences(self) -> Optional[dict]:
        config = ConfigParser()

        # check file exists
        if not os.path.exists(self.preferences):
            logger.info(f"File {self.preferences} is not exists!")
            return None

        config.read(self.preferences)
        if not (
                config.has_option("Settings", "serial")
        ):
            logger.info(f"Trouble with field serial!")
            return

        logger.info(
            f"Set device info: "
            f"serial={config.get('Settings', 'serial')}"
        )
        return {"serial": config.get("Settings", "serial")}

    def save_preferences(self, device_info: dict):
        # set device info
        if None in device_info.values():
            return
        self.device_info = device_info
        logger.info(f"Set device info {self.device_info}")

        # save device info
        config = ConfigParser()

        # check file exists
        if (os.path.exists(self.preferences)
                and config.has_option("Settings", "serial")
        ):
            config.set("Settings", "serial", self.device_info["serial"])
        else:
            config.add_section("Settings")
            config.set("Settings", "serial", self.device_info["serial"])

        with open(self.preferences, "w") as config_file:
            config.write(config_file)

    def set_device_info_and_connect(self, device_info: dict):
        # set device info
        if None in device_info.values():
            return
        logger.info(f"Set device info {self.device_info}")
        self.device_info = device_info
        # simulate button click for connect device
        self.pushButtonManage.click()

    def add_marker(self, pos, text:str="event"):
        """ Add vertical line and text"""
        line = pg.InfiniteLine(
            pos=pos,
            angle=90,
            pen=pg.mkPen('gray', width=1, style=QtCore.Qt.PenStyle.DashLine),
            movable=False,
            label=text,
            labelOpts={'color': 'k', 'position': 0.1}
        )
        self.plotWidget.addItem(line)

    def change_recording(self):
        """
        Change state recording.
        """
        if self.is_save_ecg:
            self.is_save_ecg = False

            self.pushButtonRecording.setText("Start Recording")
            self.comboBoxFormat.setEnabled(True)
            logger.debug("Select stop recording ECG.")

            # check if device running when change button state (when press stop recording)
            if self.device.is_running:
                self.storage.save()

                self.add_marker(pos=self.time[-1], text="Stop recording")

        elif self.is_save_ecg is None or not self.is_save_ecg:
            self.is_save_ecg = True

            self.pushButtonRecording.setText("Stop Recording")
            self.comboBoxFormat.setEnabled(False)
            logger.debug("Select start recording ECG.")

            self.add_marker(pos=self.time[-1], text="Start recording")

    async def connect_device(self):
        if self.device_info is None:
            self.enter_device_info()
            return

        # when user want reset connection
        if self.device is not None and self.device.is_connected:
            await self.device.close()
            self.device = None
            self.device_info = None
            self.pushButtonStart.setEnabled(False)
            self.reset()
            self.enter_device_info()
            return

        event_stop_scanning = asyncio.Event()

        # raise waiting dialog
        dlg = WaitingDialog(parent=self, event_scanning=event_stop_scanning)
        dlg.show()

        try:
            device, _ = await find_device(
                template=f"inRat-1-{self.device_info['serial']}",
                event_stop_scanning=event_stop_scanning
            )

            if device is None:
                self.device_info = None
                return

            self.device = RatSens(device)
            await self.device.connect()
            d_info = await self.device.get_device_information()
        except Exception as exc:
            info = QMessageBox.information(
                self, "Connect error",
                f"An error occurred while connect to the device\n\nInfo:\n{exc}\n\nPlease, restart application!",
                QMessageBox.StandardButton.Ok
            )
        else:
            # disable and activate btn state when find device
            if self.device.is_connected:
                self.pushButtonStart.setEnabled(True)
                # self.pushButtonManage.setEnabled(False)
                self.set_device_information(d_info)
                dlg.close()
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

            # activate and disable btn when start device
            self.pushButtonManage.setEnabled(False)
            self.pushButtonStart.setEnabled(False)
            self.pushButtonRecording.setEnabled(True)
            self.pushButtonStop.setEnabled(True)
            self.comboBoxFormat.setEnabled(True)

            # when draw signal in online - disable mouse
            self.plotWidget.setMouseEnabled(x=False, y=False)

    async def updatePlot(self):
        ecg = await self.ecg_queue.get()
        self.ecg = np.append(self.ecg, ecg["ecg"])
        self.ecg_queue.task_done()

        logger.debug(f"Current {ecg['counter']=}")

        # calculate time
        if len(self.time) == 0:
            self.time = np.arange(1, len(ecg["ecg"]) + 1) * 0.01
        else:
            self.time = np.append(self.time, np.arange(1, len(ecg["ecg"]) + 1) * 1 / 500 + self.time[-1])

        # check shape ecg and time
        if self.ecg.shape != self.time.shape:
            raise ValueError("shapes ecg and t is not same!!!")

        self.plot_ecg.setData(self.time, self.ecg)
        self.plotWidget.setXRange(max(0, self.time[-1] - SEC_SLIDE_WINDOW), self.time[-1])

        # buffer ecg in storage
        if self.is_save_ecg:
            self.storage(ecg["ecg"])

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

            if self.is_save_ecg:
                self.storage.save()
                self.add_marker(pos=self.time[-1], text="Stop recording")
                self.change_recording()

            # activate and disable btn when stop device
            self.pushButtonStop.setEnabled(False)
            self.pushButtonManage.setEnabled(True)
            self.pushButtonStart.setEnabled(True)
            self.pushButtonRecording.setEnabled(False)
            self.comboBoxFormat.setEnabled(False)

            # when stop device - activate mouse
            self.plotWidget.setMouseEnabled(x=True, y=True)

    def reset(self):
        self.ecg = np.array([])
        self.time = np.array([])
        self.plot_ecg.setData(self.time, self.ecg)
        self.set_device_information()




if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)-15s %(name)-8s %(levelname)s: %(message)s",
    )

    app = QApplication([])
    window = MainWindow()
    window.showMaximized()

    QtAsyncio.run(handle_sigint=True, debug=True)