import queue
import time
from threading import Thread

import numpy as np
import pyqtgraph as pg
from PySide6 import QtCore
from PySide6.QtGui import QFont
from pyqtgraph import mkPen

from device.constants import Pkt
from device.device import SignalDatablock
from device.enums import TypeSignal


# ToDo: переписать на единый класс (?)
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
            self._acceleration_buffer[:,-acceleration.shape[1]:] = acceleration
            self._time_buffer += acceleration.shape[1] * self.dt

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
            end_idx = len(self._acceleration_buffer)
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


class StreamViewer(pg.PlotWidget):

    def __init__(
            self,
            left_label: str | None = None, bottom_label: str | None = None, *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.setBackground((64, 64, 64))
        self.setDisabled(True)

        self._input_queue = queue.Queue()
        self._work = None
        self._running = False

        self._signal_buffer: np.ndarray | None = None
        self._time_buffer: np.ndarray | None = None
        self._buffer_filled = False  # флаг заполнения буфера
        self.current_position = 0  # текущая позиция для заполнения буфера
        
        self._sig_datablock: SignalDatablock | None = None
        
        # self._channels_count: int | None = None
        # self._counter_per_sample: int | None = None
        # self._sample_rate: int | None = None

        self._timebase: int | None = 10
        self._max_timebase: int | None = 60

        # объекты отображения сигналов len(traces) = _channels_count
        self.traces: list = []
        self.update_display: bool = False

        pen = mkPen("w")
        font = QFont("Arial", 9)

        self.setLabel("left", left_label, color="white")
        self.setLabel("bottom", bottom_label, color="white")
        for ax in ["bottom", "left"]:
            self.getAxis(ax).label.setFont(font)
            self.getAxis(ax).setPen(pen)
            self.getAxis(ax).setTickPen(pen)
            self.getAxis(ax).setTextPen(pen)
            self.getAxis(ax).setTickFont(font)

        self.startTimer(16)

    def update_params(self, params: SignalDatablock | None):
        """ установка параметров для начала отображения сигналов """
        self._sig_datablock = params

        if not params:
            return None

        pens = []
        if self._sig_datablock.type_signal is TypeSignal.ECG or self._sig_datablock.type_signal is TypeSignal.EEG:
            pens.append(mkPen(color=(255, 255, 0)))
        elif self._sig_datablock.type_signal is TypeSignal.ACC:
            pens.extend([mkPen(color=(255, 0, 0)), mkPen(color=(0, 255, 0)), mkPen(color=(173, 216, 230))])

        self._signal_buffer = np.zeros(
            (self._sig_datablock.number_channels, self._sig_datablock.sample_rate * self._max_timebase),
            dtype=np.float32
        )
        self._time_buffer = np.arange(0.0, self._max_timebase, 1 / self._sig_datablock.sample_rate)

        self._arrange_traces(pens)

    def _arrange_traces(self, pens: list):
        """ настройка объектов отображения сигнала под новое количество каналов """
        # удаление старых графиков
        for ch in self.traces:
            self.removeItem(ch)
        self.traces = []

        pen = None
        for ch in range(self._sig_datablock.number_channels):
            if len(pens) == self._sig_datablock.number_channels:
                pen = pens[ch]

            self.traces.append(self.plot(pen=pen))

    def process_input(self, data: dict):
        """ обработка входящего сигнала и добавление в буфер """
        current_sample, signal = data["counter"], data["signal"]
        signal = signal[np.newaxis] # .shape = (1,32) for ecg/eeg

        # todo: добавить проверку сигнала на соответствие channels_count, count_per_samples
        if not self._buffer_filled:
            if self.current_position + self._sig_datablock.counter_per_sample < self._signal_buffer.shape[1]:

                self._signal_buffer[:, self.current_position: self.current_position + self._sig_datablock.counter_per_sample] = signal
                self.current_position += self._sig_datablock.counter_per_sample
            else:
                offset = self._signal_buffer.shape[1] - self.current_position
                self._signal_buffer[:, self.current_position] = signal[:, :offset]
                signal = signal[:, offset:]
                self._buffer_filled = True

        if self._buffer_filled and signal.shape[1] != 0:
            self._signal_buffer = np.roll(self._signal_buffer, -len(signal))
            self._signal_buffer[: -signal.shape[1]:] = signal
            self._time_buffer += signal.shape[1] * (1 / self._sig_datablock.sample_rate)

        self.update_display = True

    def timerEvent(self, event, /):
        """ событие отрисовки графиков """
        if not self.update_display:
            return

        if not self._buffer_filled:
            end_idx = self.current_position
            start_idx = 0
            if end_idx > self._timebase * self._sig_datablock.sample_rate:
                start_idx = end_idx - int(self._timebase * self._sig_datablock.sample_rate)
        else:
            end_idx = self._signal_buffer.shape[1]
            start_idx = end_idx - int(self._timebase * self._sample_rate)

        visible_time = self._time_buffer[start_idx:end_idx]
        for ch in range(self._sig_datablock.number_channels):
            self.traces[ch].setData(visible_time, self._signal_buffer[ch, start_idx: end_idx])

        # подстройка по оси времени
        if not self._buffer_filled and end_idx <= self._timebase * self._sig_datablock.sample_rate:
            self.setXRange(0, self._timebase, padding=0)
        else:
            current_time = visible_time[-1] if len(visible_time) > 0 else 0
            self.setXRange(current_time - self._timebase, current_time, padding=0)

        self.update_display = False

    def start(self):
        """ запуск модуля на прием и отображения сигнала """
        while not self._input_queue.empty():
            self._input_queue.get_nowait()

        if not self._running:
            self._running = True
            self._work = Thread(target=self._worker_thread)
            self._work.start()

    def stop(self):
        """ остановка модуля на прием и отображения сигнала """
        self._running = False
        if self._work:
            self._work.join(5.0)
            self._work = None

        # self.process_stop()

    def _worker_thread(self):
        while self._running:
            try:
                data = self._input_queue.get(False)
                self.process_input(data)
            except queue.Empty:
                ...
            except Exception as exc:
                ...

            time.sleep(0.001)


    def _transmit_data(self, data):
        try:
            self._input_queue.put(data, False)
        except:
            ...