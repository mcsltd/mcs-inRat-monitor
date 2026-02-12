import numpy as np
from PySide6.QtGui import QFont
from pyqtgraph import PlotWidget, PlotDataItem

import pyqtgraph as pg

from device.device import EcgDataBlock

RED = pg.mkPen(color=(255, 0, 0), width=2)


class DisplayScope(PlotWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        font = QFont()
        font.setPointSize(12)

        self.start_time = 0

        self.curve: PlotDataItem = self.plot()
        self.timebase = 10 # in sec
        self.ecg_buffer = np.array([], "d")
        self.time_buffer = np.array([], "d")

        self.setLabel("left", "ECG (uV)", pen=pg.mkPen(color='k'), font=font)
        self.getAxis("left").label.setFont(font)
        self.getAxis("left").setPen(pg.mkPen(color='k'))
        self.getAxis("left").setTextPen(pg.mkPen(color='k'))
        self.getAxis("left").setTickFont(font)

        self.setLabel("bottom", "Time (sec)", pen=pg.mkPen(color='k'), font=font)
        self.getAxis("bottom").label.setFont(font)
        self.getAxis("bottom").setPen(pg.mkPen(color='k'))
        self.getAxis("bottom").setTextPen(pg.mkPen(color='k'))
        self.getAxis("bottom").setTickFont(font)

        self.addLegend()
        self.setBackground("w")

    def process_input(self, datablock: EcgDataBlock):
        dt = 1 / datablock.sample_rate
        st = datablock.block_time.timestamp()
        ft = datablock.block_time.timestamp() + 32 * dt
        if len(self.time_buffer) == 0:
            self.time_buffer = np.arange(st, ft, dt)
        else:
            time = np.arange(st, ft, dt)
            self.time_buffer = np.append(self.time_buffer, time)

        self.ecg_buffer = np.append(self.ecg_buffer, datablock.ecg_signal)
        self.curve.setData(self.time_buffer, self.ecg_buffer)

        if self.time_buffer[-1] < self.timebase:
            self.setXRange(0, self.timebase)
        else:
            self.setXRange(self.time_buffer[-1] - self.timebase, self.time_buffer[-1])





