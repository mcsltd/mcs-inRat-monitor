import numpy as np
import pyqtgraph as pg
from PySide6.QtGui import QFont

RED = pg.mkPen(color=(255, 0, 0), width=1.5)

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

    def load_data(self, time, temperature):
        self.time_buffer = np.array(time)
        self.temperature_buffer = np.array(temperature)
        self.plot_temperature.setData(self.time_buffer, self.temperature_buffer)
        self.setXRange(self.time_buffer[0], self.time_buffer[-1])
        self.setYRange(0.95 * self.temperature_buffer[0], self.temperature_buffer[-1] * 1.05)
        self.setMouseEnabled(x=True, y=True)


class PlotWidgetEcg(pg.PlotWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setTitle("ECG", color="k", size="12pt")

        font = QFont()
        font.setPointSize(12)
        # легенда
        self.legend = self.addLegend()
        self.legend.setLabelTextColor(0, 0, 0)

        self.time_buffer = np.array([])
        self.ecg_buffer = np.array([])

        # scatter plot for activity, freefall, orientation
        self.scatter_activity = pg.ScatterPlotItem(name="Activity", symbol='t', brush=pg.mkBrush(0, 255, 0, 180),
                                                   size=10, )
        self.addItem(self.scatter_activity)
        self.scatter_orientation = pg.ScatterPlotItem(name="Orientation", symbol="o", brush=pg.mkBrush(0, 0, 255, 180),
                                                      size=10, )
        self.addItem(self.scatter_orientation)
        self.scatter_freefall = pg.ScatterPlotItem(name="Freefall", symbol='s', brush=pg.mkBrush(255, 0, 0, 180),
                                                   size=10, )
        self.addItem(self.scatter_freefall)

        self.setLabel("left", "V", pen=pg.mkPen(color='k'), font=font)
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

        self.setMouseEnabled(x=False, y=False)
        self.plot_ecg = self.plot(pen=RED)

    def load_ecg(self, ecg: np.ndarray, sec_duration: float, sample_rate: int):
        self.time_buffer = np.arange(0, sec_duration, 1 / sample_rate)
        self.ecg_buffer = ecg
        self.plot_ecg.setData(self.time_buffer, self.ecg_buffer)
        self.setXRange(self.time_buffer[0], self.time_buffer[-1])
        self.setYRange(0.95 * min(self.ecg_buffer), np.max(self.ecg_buffer) * 1.05)
        self.setMouseEnabled(x=True, y=True)

    def load_event(self, events: list[dict]):
        y_min = 0
        if len(self.ecg_buffer) != 0:
            y_min = min(self.ecg_buffer) * 1.15

        for ev in events:
            if ev["event"] == "Activity":
                self.scatter_activity.addPoints([{'pos': (ev["time"], y_min)}])
            if ev["event"] == "Orientation":
                self.scatter_orientation.addPoints([{'pos': (ev["time"], y_min)}])
            if ev["event"] == "Freefall":
                self.scatter_freefall.addPoints([{'pos': (ev["time"], y_min)}])
        self.setMouseEnabled(x=True, y=True)