import asyncio
import logging
import pyqtgraph as pg

import numpy as np
from PySide6 import QtAsyncio
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QMainWindow, QApplication

from config import DATA_PATH
from device import RatSens
from storage import Storage
from ui.main_window import Ui_MainWindow
from utils.scanner import find_device

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, device, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)

        self.ecg = np.array([])
        self.time = np.array([])

        self.device: RatSens = device
        self.ecg_queue = asyncio.Queue()

        self.is_save_ecg = None
        self.storage = Storage()

        self.pushButtonFind.clicked.connect(lambda: asyncio.ensure_future(self.find_device()))
        self.pushButtonStart.clicked.connect(lambda: asyncio.ensure_future(self.start_device()))
        self.pushButtonStop.clicked.connect(lambda: asyncio.ensure_future(self.stop_device()))
        self.pushButtonRecording.clicked.connect(self.change_recording)
        self.comboBoxFormat.currentTextChanged.connect(self.storage.set_format)

        # set plot
        pen = pg.mkPen(color=(255, 0, 0))
        self.plot_ecg = self.plotWidget.plot(self.time, self.ecg, pen=pen)
        self.plotWidget.setLabel("left", "ECG (μV)", )
        self.plotWidget.setLabel("bottom", "Time (sec)", )
        self.plotWidget.addLegend()

        # timer for get ecg from device and draw plot
        self.time_update = 1
        self.timer = QTimer()
        self.timer.setInterval(self.time_update)
        self.timer.timeout.connect(lambda: asyncio.ensure_future(self.updatePlot()))


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

        elif self.is_save_ecg is None or not self.is_save_ecg:
            self.is_save_ecg = True

            self.pushButtonRecording.setText("Stop Recording")
            self.comboBoxFormat.setEnabled(False)
            logger.debug("Select start recording ECG.")


    async def find_device(self):
        device, _ = await find_device()
        self.device = RatSens(device)
        await self.device.connect()
        # device_name = await self.device.get_device_name()

        # disable and activate btn state when find device
        if self.device.is_connected:
            self.pushButtonStart.setEnabled(True)
            self.pushButtonFind.setEnabled(False)


    async def start_device(self):
        logger.debug("Start device")
        await self.device.get_ecg(ecg_queue=self.ecg_queue)
        self.timer.start()

        # activate and disable btn when start device
        self.pushButtonStart.setEnabled(False)
        self.pushButtonRecording.setEnabled(True)
        self.pushButtonStop.setEnabled(True)
        self.comboBoxFormat.setEnabled(True)

    async def updatePlot(self):
        ecg = await self.ecg_queue.get()
        self.ecg = np.append(self.ecg, ecg["ecg"])

        # calculate time
        if len(self.time) == 0:
            self.time = np.arange(1, len(ecg["ecg"]) + 1) * 0.01
        else:
            self.time = np.append(self.time, np.arange(1, len(ecg["ecg"]) + 1) * 1 / 500 + self.time[-1])

        # check shape ecg and time
        if self.ecg.shape != self.time.shape:
            raise ValueError("shapes ecg and t is not same!!!")

        self.plot_ecg.setData(self.time, self.ecg)

        # buffer ecg in storage
        if self.is_save_ecg:
            self.storage(ecg["ecg"])


    async def stop_device(self):
        logger.debug("Stop device")
        await self.device.stop()
        self.timer.stop()

        if self.is_save_ecg:
            self.storage.save()
            self.change_recording()

        # activate and disable btn when stop device
        self.pushButtonStop.setEnabled(False)
        self.pushButtonStart.setEnabled(True)
        self.pushButtonRecording.setEnabled(False)
        self.comboBoxFormat.setEnabled(False)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)-15s %(name)-8s %(levelname)s: %(message)s",
    )

    app = QApplication([])

    window = MainWindow(device=None)
    window.show()

    QtAsyncio.run(handle_sigint=True, debug=True)