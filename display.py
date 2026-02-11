from PySide6.QtGui import QFont
from pyqtgraph import PlotWidget, PlotDataItem

import pyqtgraph as pg

RED = pg.mkPen(color=(255, 0, 0), width=2)


class DisplayScope(PlotWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        font = QFont()
        font.setPointSize(12)

        self.curve: PlotDataItem = self.plot()
        self.timebase = 10 # in sec

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

    def process_input(self, datablock: dict):
        self.curve.setData(datablock["data"])



