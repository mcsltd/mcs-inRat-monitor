import numpy as np
import pyqtgraph as pg
from PySide6 import QtCore
from PySide6.QtGui import QFont
from pyqtgraph import mkPen

from device.constants import Pkt

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
        # self.addItem(self.scatter_activity)
        self.scatter_orientation = pg.ScatterPlotItem(name="Orientation", symbol="o", brush=pg.mkBrush(0, 0, 255, 180),
                                                      size=10, )
        # self.addItem(self.scatter_orientation)
        self.scatter_freefall = pg.ScatterPlotItem(name="Freefall", symbol='s', brush=pg.mkBrush(255, 0, 0, 180),
                                                   size=10, )
        # self.addItem(self.scatter_freefall)

        self.setLabel("left", "V", pen=pg.mkPen(color='k'), font=font)
        self.getAxis("left").label.setFont(font)
        self.getAxis("left").setPen(pg.mkPen(color='k'))
        self.getAxis("left").setTextPen(pg.mkPen(color='k'))
        self.getAxis("left").setTickFont(font)
        self.setLabel("bottom", "Time (s)", pen=pg.mkPen(color='k'), font=font)
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


class StreamAccelerationViewer(pg.PlotWidget):
    """ класс для отображения сигналов в стриме"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setBackground((64, 64, 64))
        self.setDisabled(True)

        pen = mkPen("w")
        font = QFont("Arial", 11)
        self.setLabel("left", "mg", color="white")
        self.setLabel("bottom", color="white")  # "Время", units="s",
        for ax in ["bottom", "left"]:
            self.getAxis(ax).label.setFont(font)
            self.getAxis(ax).setPen(pen)
            self.getAxis(ax).setTickPen(pen)
            self.getAxis(ax).setTextPen(pen)
            self.getAxis(ax).setTickFont(font)

        self.plot_ax = self.plot(pen=pg.mkPen(color=(255, 0, 0), width=1.5), legend="ax")
        self.plot_ay = self.plot(pen=pg.mkPen(color=(0, 255, 0), width=1.5), legend="ay")
        self.plot_az = self.plot(pen=pg.mkPen(color=(0, 0, 255), width=1.5), legend="az")
        self.addLegend()

        # data
        self._fs = 500
        self.max_timebase = 60
        self.timebase = 10
        self.dt = 1 / self._fs
        self._acceleration_buffer = np.zeros((Pkt.ChannelsCountAcc, int(self.max_timebase * self._fs)))

        # переменные для управления отображением
        self.buffer_filled = False  # флаг заполнения буфера
        self.current_position = 0  # текущая позиция для заполнения буфера
        self.pending_update = False # флаг что доступны данные

        # таймер обновления графика
        self.update_timer = QtCore.QTimer()
        self.update_timer.timeout.connect(self.update_plot)
        self.update_timer.setInterval(16)

    def set_data(self, data: dict | None):
        """ добавление данных сигнала в буфер """
        if not data:
            return

        print(f"{data['counter']=}, {data['acceleration']=}")
        return

        # if not self.buffer_filled:
        #     # вставка данных в незаполненный буфер
        #     if self.current_position + Pkt.SamplesCountAcc < len(self.ecg_buffer):
        #         self.ecg_buffer[self.current_position:self.current_position + Pkt.SamplesCountEcg] = signal
        #         self.current_position += Pkt.SamplesCountEcg
        #     else:
        #         offset = len(self.ecg_buffer) - self.current_position
        #         self.ecg_buffer[self.current_position:] = signal[:offset]
        #         signal = signal[offset:]
        #         self.buffer_filled = True
        # # вставка данных в заполненный буфер
        # if self.buffer_filled and len(signal) != 0:
        #     self._signal_buffer = np.roll(self.ecg_buffer, -len(signal))
        #     self.ecg_buffer[-len(signal):] = signal
        #     self.time_buffer += len(signal) * self.dt
        # self.pending_update = True

    def update_plot(self):
        """Обновление графика по таймеру"""
        if not self.pending_update:
            return

        if not self.buffer_filled:
            end_idx = self.current_position
            start_idx = 0

            if end_idx > self.timebase * self.fs:
                start_idx = end_idx - int(self.timebase * self.fs)
        else:
            end_idx = len(self.ecg_buffer)
            start_idx = end_idx - int(self.timebase * self.fs)
        visible_time = self.time_buffer[start_idx:end_idx]
        visible_ecg = self.ecg_buffer[start_idx:end_idx]

        try:
            y_min = 0
            if len(visible_ecg) != 0:
                y_min = visible_ecg.min()
            # отображение событий из буфера
            self.event_display(y_min)
            self.replot()

        except Exception as err:
            ...

        # установка данных из буфера на дисплей
        self.plot_signal.setData(visible_time, visible_ecg)

        # отображение по оси времени
        if not self.buffer_filled and end_idx <= self.timebase * self.fs:
            self.setXRange(0, self.timebase, padding=0)
        else:
            current_time = visible_time[-1] if len(visible_time) > 0 else 0
            self.setXRange(current_time - self.timebase, current_time, padding=0)

        # отображение по оси напряжения
        if not self.y_max and not self.y_min:
            if len(visible_ecg) > 0:
                data_min = visible_ecg.min()
                data_max = visible_ecg.max()
                if data_max > data_min:
                    padding = (data_max - data_min) * 0.05
                    self.setYRange(data_min - padding, data_max + padding)
        else:
            self.setYRange(self.y_min, self.y_max)

        self.replot()
        self.pending_update = False
