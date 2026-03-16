import numpy as np
import pyqtgraph as pg
from PySide6.QtGui import QFont


class PlotWidgetTemperature(pg.PlotWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setTitle("Temperature", color="k", size="12pt")

        font = QFont()
        font.setPointSize(12)

        self.max_timebase_min = 10
        self.time_buffer = np.array([])
        self.temperature_buffer = np.array([])

        self.setLabel("left", "°C", pen=pg.mkPen(color='k'), font=font)
        self.getAxis("left").label.setFont(font)
        self.getAxis("left").setPen(pg.mkPen(color='k'))
        self.getAxis("left").setTextPen(pg.mkPen(color='k'))
        self.getAxis("left").setTickFont(font)

        self.setLabel("bottom", "Time (minute)", pen=pg.mkPen(color='k'), font=font)
        self.getAxis("bottom").label.setFont(font)
        self.getAxis("bottom").setPen(pg.mkPen(color='k'))
        self.getAxis("bottom").setTextPen(pg.mkPen(color='k'))
        self.getAxis("bottom").setTickFont(font)

        self.addLegend()
        self.setBackground("w")

        self.setXRange(0,10)
        self.setYRange(20, 45)
        self.setMouseEnabled(x=False, y=False)

        self.plot_temperature = self.plot(pen=pg.mkPen(color='b', width=1.1), symbol='o', symbolSize=8, symbolBrush='b')
        self.plot_temperature.setData(self.time_buffer, self.temperature_buffer)


    def set_data(self, time_sec: float, temperature: float):
        """ установка температуры и отображение данных """
        time_min = time_sec / 60

        if time_min > self.max_timebase_min:
            self.temperature_buffer = np.roll(self.temperature_buffer, -1)
            self.temperature_buffer[-1] = temperature

            self.time_buffer = np.roll(self.time_buffer, -1)
            self.time_buffer[-1] = time_min

            self.setXRange(self.time_buffer[0], self.time_buffer[-1])
        else:
            self.time_buffer = np.append(self.time_buffer, time_min)
            self.temperature_buffer = np.append(self.temperature_buffer, temperature)
            self.setXRange(0, self.max_timebase_min)

        self.plot_temperature.setData(self.time_buffer, self.temperature_buffer)
        self.setYRange(min(self.temperature_buffer) * 0.95, max(self.temperature_buffer) * 1.05)


    def reset(self):
        self.temperature_buffer = np.array([])
        self.time_buffer = np.array([])
        self.plot_temperature.setData(self.time_buffer, self.temperature_buffer)
        self.setXRange(0, self.max_timebase_min)
