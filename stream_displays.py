import numpy as np
import pyqtgraph as pg
from PySide6 import QtCore
from PySide6.QtGui import QFont
from pyqtgraph import mkPen

from device.constants import Pkt

# ToDo: переписать на единый класс
# ToDo: сделать адаптацию под выбранные настройки устройства
# ToDo: сделать виджеты для контроля параметров отрисовки


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
        self._fs = 100
        self.max_timebase = 60
        self.timebase = 10
        self.dt = 1 / self._fs
        self._acceleration_buffer = np.zeros((Pkt.ChannelsCountAcc, int(self.max_timebase * self._fs)))
        self._time_buffer = np.arange(0, self.max_timebase, self.dt)
        self.y_max, self.y_min = None, None

        # переменные для управления отображением
        self.buffer_filled = False  # флаг заполнения буфера
        self.current_position = 0  # текущая позиция для заполнения буфера
        self.pending_update = False # флаг что доступны данные

        # таймер обновления графика
        self.update_timer = QtCore.QTimer()
        self.update_timer.timeout.connect(self.update_plot)
        self.update_timer.start(16)

    def set_data(self, data: dict | None):
        """ добавление данных сигнала в буфер """
        if not data:
            return

        counter, acceleration = data['counter'], data['acceleration']
        if not self.buffer_filled:
            # вставка данных в незаполненный буфер
            if self.current_position + Pkt.SamplesCountAcc < self._acceleration_buffer.shape[1]:
                self._acceleration_buffer[:,self.current_position:self.current_position + Pkt.SamplesCountAcc] = acceleration
                self.current_position += Pkt.SamplesCountAcc
            else:
                offset = self._acceleration_buffer.shape[1] - self.current_position
                self._acceleration_buffer[:,self.current_position:] = acceleration[:,:offset]
                acceleration = acceleration[:,offset:]
                self.buffer_filled = True

        # вставка данных в заполненный буфер
        if self.buffer_filled and acceleration.shape[1] != 0:
            self._acceleration_buffer = np.roll(self._acceleration_buffer, -acceleration.shape[1])
            self._acceleration_buffer[-acceleration.shape[1]:] = acceleration
            self.time_buffer += acceleration.shape[1] * self.dt

        self.pending_update = True

    def update_plot(self):
        """Обновление графика по таймеру"""
        if not self.pending_update:
            return

        if not self.buffer_filled:
            end_idx = self.current_position
            start_idx = 0

            if end_idx > self.timebase * self._fs:
                start_idx = end_idx - int(self.timebase * self._fs)
        else:
            end_idx = len(self.ecg_buffer)
            start_idx = end_idx - int(self.timebase * self._fs)

        visible_time = self._time_buffer[start_idx:end_idx]
        visible_ax = self._acceleration_buffer[0, start_idx:end_idx]
        visible_ay = self._acceleration_buffer[1, start_idx:end_idx]
        visible_az = self._acceleration_buffer[2, start_idx:end_idx]

        self.plot_ax.setData(visible_time, visible_ax)
        self.plot_ay.setData(visible_time, visible_ay)
        self.plot_az.setData(visible_time, visible_az)

        # отображение по оси времени
        if not self.buffer_filled and end_idx <= self.timebase * self._fs:
            self.setXRange(0, self.timebase, padding=0)
        else:
            current_time = visible_time[-1] if len(visible_time) > 0 else 0
            self.setXRange(current_time - self.timebase, current_time, padding=0)

        # отображение по оси напряжения
        if not self.y_max and not self.y_min:
            if len(visible_ax) > 0 and len(visible_ay) > 0 and len(visible_az) > 0:
                data_min = min(visible_ax.min(), visible_ay.min(), visible_az.min())
                data_max = max(visible_ax.max(), visible_ay.max(), visible_az.max())
                if data_max > data_min:
                    padding = (data_max - data_min) * 0.05
                    self.setYRange(data_min - padding, data_max + padding)
        else:
            self.setYRange(self.y_min, self.y_max)

        self.replot()
        self.pending_update = False


class StreamSignalViewer(pg.PlotWidget):
    """ Класс для накопления и отображения сигнала на графике """

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.setBackground((64, 64, 64))
        self.setDisabled(True)

        # легенда
        self.legend = self.addLegend()
        self.legend.setLabelTextColor(255, 255, 255)

        pen = mkPen("w")
        font = QFont("Arial", 11)
        self.plot_signal = self.plot(pen=pg.mkPen(color=(255, 255, 0), width=1.5))

        # data
        self.fs = 500
        self.max_timebase = 60
        self.timebase = 10
        self.dt = 1 / self.fs
        self.ecg_buffer = np.zeros(int(self.max_timebase * self.fs))
        self.time_buffer = np.arange(0, self.max_timebase, self.dt)
        self.y_max, self.y_min = None, None

        # переменные для управления отображением
        self.buffer_filled = False  # флаг заполнения буфера
        self.current_position = 0  # текущая позиция для заполнения буфера

        self.setLabel("left", "ЭКГ", units="V", color="white")
        self.setLabel("bottom", color="white")    # "Время", units="s",
        for ax in ["bottom", "left"]:
            self.getAxis(ax).label.setFont(font)
            self.getAxis(ax).setPen(pen)
            self.getAxis(ax).setTickPen(pen)
            self.getAxis(ax).setTextPen(pen)
            self.getAxis(ax).setTickFont(font)

        self._markers = []
        self.pending_update = False

        # таймер обновления графика
        self.update_timer = QtCore.QTimer()
        self.update_timer.timeout.connect(self.update_plot)
        self.update_timer.start(16)


    def set_data(self, ecg: dict):
        """ добавление данных сигнала в буфер """
        signal, counter = ecg["signal"], ecg["counter"]
        if not self.buffer_filled:
            # вставка данных в незаполненный буфер
            if self.current_position + Pkt.SamplesCountEcg < len(self.ecg_buffer):
                self.ecg_buffer[self.current_position:self.current_position + Pkt.SamplesCountEcg] = signal
                self.current_position += Pkt.SamplesCountEcg
            else:
                offset = len(self.ecg_buffer) - self.current_position
                self.ecg_buffer[self.current_position:] = signal[:offset]
                signal = signal[offset:]
                self.buffer_filled = True

        # вставка данных в заполненный буфер
        if self.buffer_filled and len(signal) != 0:
            self.ecg_buffer = np.roll(self.ecg_buffer, -len(signal))
            self.ecg_buffer[-len(signal):] = signal
            self.time_buffer += len(signal) * self.dt

        self.pending_update = True


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


    def clear_plot(self):
        """Очистка графика"""
        # очистка графика от сигнала
        self.plot_signal.setData(np.array([]), np.array([]))  # clear signal
        self.plot_signal.clear()

        # очистка графика от событий
        if self.freefall_scatter:
            self.freefall_scatter.clear()
        if self.orientation_scatter:
            self.orientation_scatter.clear()
        if self.activity_scatter:
            self.activity_scatter.clear()
        self.event_buffer = []

        # очистка графика от маркеров
        for marker in self._markers:
            self.removeItem(marker)
        self._markers = []

        # сброс данных
        self.max_timebase = 60
        self.timebase = 10
        self.dt = 1 / self.fs
        self.ecg_buffer = np.zeros(int(self.max_timebase * self.fs))
        self.time_buffer = np.arange(0, self.max_timebase, self.dt)
        self.buffer_filled = False  # флаг заполнения буфера
        self.current_position = 0  # текущая позиция для заполнения буфера