import asyncio
import logging

import numpy as np
from PySide6 import QtAsyncio
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QMainWindow, QApplication

from device import RatSens
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

        self.pushButtonFind.clicked.connect(lambda: asyncio.ensure_future(self.find_device()))
        self.pushButtonStart.clicked.connect(lambda: asyncio.ensure_future(self.start_device()))
        self.pushButtonStop.clicked.connect(lambda: asyncio.ensure_future(self.stop_device()))

        # set plot
        self.plot_ecg = self.plotWidget.plot(self.time, self.ecg, pen="g")

        # timer for get ecg from device and draw plot
        self.time_update = 1
        self.timer = QTimer()
        self.timer.setInterval(self.time_update)
        self.timer.timeout.connect(lambda: asyncio.ensure_future(self.updatePlot()))

    async def find_device(self):
        device, _ = await find_device()
        self.device = RatSens(device)
        await self.device.connect()
        device_name = await self.device.get_device_name()
        print(f"Find device: {device_name}")

    async def start_device(self):
        logger.debug("Start device")
        await self.device.get_ecg(ecg_queue=self.ecg_queue)
        self.timer.start()

    async def updatePlot(self):
        ecg = await self.ecg_queue.get()

        self.ecg = np.append(self.ecg, ecg["ecg"])
        # calculate time
        if len(self.time) == 0:
            self.time = np.arange(1, len(ecg["ecg"]) + 1) * 0.01
        else:
            self.time = np.append(self.time, np.arange(1, len(ecg["ecg"]) + 1) * 1 / 500 + self.time[-1])

        if self.ecg.shape != self.time.shape:
            assert "shapes ecg and t is not same!!!"

        self.plot_ecg.setData(self.time, self.ecg)
        print("Ok!!!")


    async def stop_device(self):
        logger.debug("Stop device")
        await self.device.stop()
        self.timer.stop()

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)-15s %(name)-8s %(levelname)s: %(message)s",
    )

    app = QApplication([])

    window = MainWindow(device=None)
    window.show()

    QtAsyncio.run(handle_sigint=True, debug=True)