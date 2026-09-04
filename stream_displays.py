import logging
import queue
import time
from threading import Thread

import numpy as np
import pyqtgraph as pg
from PySide6.QtCore import Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QFrame
from pyqtgraph import mkPen, ScatterPlotItem, LegendItem, ItemSample

from device.device import SignalDatablock
from device.enums import TypeSignal, EventType
from resources.frm_control_xy_range import Ui_FrmControlXYRange

# ToDo: переписать на единый класс (?)
# ToDo: сделать адаптацию под выбранные настройки устройства

logger = logging.getLogger(__name__)


class FrmControlXYRange(QFrame, Ui_FrmControlXYRange):
    """ Виджет контроля параметров по оси X, Y"""

    signal_y_changed = Signal(object)
    signal_x_changed = Signal(object)

    def __init__(
            self,
            x_values: list[tuple] | None = None, default_idx_x: int | None = None,
            y_values: list[tuple] | None = None, default_idx_y: int | None = None,
            *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.comboBoxXRange.setEnabled(False)
        self.comboBoxYRange.setEnabled(False)

        if x_values:
            self._set_x_values(x_values)
            if default_idx_x:
                self.comboBoxXRange.setCurrentIndex(default_idx_x)
            self.comboBoxXRange.currentIndexChanged.connect(self._get_current_x_value)
        if y_values:
            self._set_y_values(y_values)
            if default_idx_y:
                self.comboBoxYRange.setCurrentIndex(default_idx_y)
            self.comboBoxYRange.setCurrentIndex(default_idx_y)
            self.comboBoxYRange.currentIndexChanged.connect(self._get_current_y_value)

    def _set_y_values(self, values: list[tuple]):
        for v, d in values:
            self.comboBoxYRange.addItem(v, d)
        # self.comboBoxYRange.setCurrentIndex(2)
        self.comboBoxYRange.setEnabled(True)

    def _get_current_y_value(self, index):
        value = self.comboBoxYRange.currentData()
        self.signal_y_changed.emit(value)

    def _set_x_values(self, values: list[tuple]):
        for v, d in values:
            self.comboBoxXRange.addItem(v, d)
        # self.comboBoxXRange.setCurrentIndex(2)
        self.comboBoxXRange.setEnabled(True)

    def _get_current_x_value(self, index):
        value = self.comboBoxXRange.currentData()
        self.signal_x_changed.emit(value)


class StreamViewer(pg.PlotWidget):

    def __init__(
            self,
            left_label: str | None = None, *args, **kwargs
    ):
        kwargs['axisItems'] = {'bottom': FormatterTimeAxisItem(orientation="bottom")}
        super().__init__(*args, **kwargs)
        self.setBackground((64, 64, 64))
        self.setDisabled(True)

        self._input_queue = queue.Queue()
        self._work = None
        self._running = False

        self.unit = None
        self._signal_buffer: np.ndarray | None = None
        self._time_buffer: np.ndarray | None = None
        self._buffer_filled = False  # флаг заполнения буфера
        self.current_position = 0  # текущая позиция для заполнения буфера

        # блок данных с параметром
        self._sig_datablock: SignalDatablock | None = None

        # настройки отображения
        self._y_max, self._y_min = None, None
        self._timebase: int | None = 10
        self._max_timebase: int | None = 60

        # объекты отображения сигналов len(traces) = _channels_count
        self.traces: list = []
        self.scatters: dict = {}
        self.point_scatters: dict ={}
        self.update_display: bool = False

        pen = mkPen("w")
        font = QFont("Arial", 9)

        # легенды для сигнала
        self.legend_sig = LegendItem(colCount=3, labelTextColor="white", labelTextSize="12pt")
        self.legend_sig.setParentItem(self.getPlotItem())
        self.legend_sig.anchor(offset=(50, 0), itemPos=(0,0), parentPos=(0, 0))

        self.legend_ev = LegendItem(colCount=3, labelTextColor="white", labelTextSize="9pt")
        self.legend_ev.setParentItem(self.getPlotItem())
        self.legend_ev.anchor(itemPos=(0, 1), parentPos=(0, 1), offset=(35, -35))

        self.legend_temp = LegendItem(labelTextColor="white", labelTextSize="18pt")
        self.legend_temp.setParentItem(self.getPlotItem())
        self.legend_temp.anchor(offset=(-120, 0), itemPos=(0,0), parentPos=(1, 0))

        self.setLabel("left", left_label, color="white")
        self.setLabel("bottom", color="white") # "mm:ss",
        for ax in ["bottom", "left"]:
            self.getAxis(ax).label.setFont(font)
            self.getAxis(ax).setPen(pen)
            self.getAxis(ax).setTickPen(pen)
            self.getAxis(ax).setTextPen(pen)
            self.getAxis(ax).setTickFont(font)

        self.startTimer(16)

    def set_x_range(self, value: float):
        """ установка окна отображения сигнала """
        if value > self._max_timebase:
            logger.warning(f"Диапазон вывода сигнала по оси x {value} c. не можеть быть больше чем {self._max_timebase} с.")
            return
        self._timebase = value

    def set_y_range(self, value: float | None):
        """ установка ограничения выводимого сигнала """
        if value is None:
            self._y_min, self._y_min = None, None
            self.enableAutoRange(axis='y', enable=True)
            logger.info("Установлено АРУ")
            return

        if value < 0:
            logger.warning("Значение не может быть меньше 0")
            return
        self._y_min = -value
        self._y_max = value
        logger.info(f"Установлен диапазон отображения по оси y - ({-self._y_min};{self._y_max};)")

    def update_params(self, params: SignalDatablock | None):
        """ установка параметров для начала отображения сигналов """
        self._sig_datablock = params

        if not params:
            return None

        type_signal = self._sig_datablock.type_signal.value
        self.unit = self._sig_datablock.units
        # настройка отрисовки графиков разными цветами
        pens = []
        if self._sig_datablock.type_signal is TypeSignal.ECG or self._sig_datablock.type_signal is TypeSignal.EEG:
            # self.y_min, self.y_max = -5 * 1e-3, 5 * 1e-3
            pens.append(mkPen(color=(255, 255, 0)))

            if self.unit == "uV":
                self.setLabel("left", text=type_signal, units="V", color="white", force=True)
            else:
                self.setLabel("left", text=type_signal, units=self.unit, color="white", force=True)

        elif self._sig_datablock.type_signal is TypeSignal.ACC:
            # self.y_min, self.y_max = -1e3, 1e3
            pens.extend([mkPen(color=(255, 0, 0)), mkPen(color=(0, 255, 0)), mkPen(color=(173, 216, 230))])
            self.setLabel("left", text=type_signal, units=self.unit, color="white", force=True)

        # пересоздание буфера
        self._signal_buffer = np.zeros(
            (self._sig_datablock.number_channels, self._sig_datablock.sample_rate * self._max_timebase),
            dtype=np.float32
        )
        self._time_buffer = np.arange(0.0, self._max_timebase, 1 / self._sig_datablock.sample_rate)
        self._buffer_filled = False  # флаг заполнения буфера
        self.current_position = 0  # текущая позиция для заполнения буфера
        self.update_display: bool = False

        self._arrange_traces(pens)
        self._arrange_scatters()

    def _arrange_traces(self, pens: list):
        """ настройка объектов отображения сигнала под новое количество каналов """
        # удаление старых графиков
        for ch in self.traces:
            self.legend_sig.removeItem(ch)
            self.removeItem(ch)
        self.traces = []

        pen = None
        for ch in range(self._sig_datablock.number_channels):
            if len(pens) == self._sig_datablock.number_channels:
                pen = pens[ch]

            plot = self.plot(pen=pen, name=self._sig_datablock.channel_names[ch])
            self.traces.append(plot)
            self.legend_sig.addItem(item=plot, name=self._sig_datablock.channel_names[ch])

    def _arrange_scatters(self):
        """ настройка объектов отображения диаграмм рассеяния для графиков """
        # удаление графиков событий
        events = list(self.scatters.keys())
        for ev in events:
            self.scatters[ev].clear()
            self.removeItem(self.scatters[ev])
            self.legend_ev.removeItem(self.scatters[ev])
            self.scatters.pop(ev)
        self.scatters = {}

        # добавление графиков рассеяния для отображения событий
        for type_event in self._sig_datablock.type_events:

            # if type_event == "temp":
            #     empty_sample = ItemSample(item=None)
            #     self.legend_temp.clear()
            #     self.legend_temp.addItem(empty_sample, "--°C")
            #     continue

            symbol, brush, event_name = None, None, None
            if type_event == "activity":
                event_name = "Активность(A)"
                symbol, brush = 't', pg.mkBrush(0, 255, 0, 180)
            elif type_event == "freefall":
                event_name = "Невесомость(F)"
                symbol, brush = 'o', pg.mkBrush(0, 0, 255, 180)
            elif type_event == "orientation":
                event_name = "Ориентация(O)"
                symbol, brush = 's', pg.mkBrush(255, 0, 0, 180),
            else:
                logger.warning(f"Не поддерживаемый тип событий - {type_event}")
                continue

            self.scatters[type_event] = ScatterPlotItem(name=type_event, symbol=symbol, brush=brush, size=10) # temp не добавляется
            self.point_scatters[type_event] = list()
            self.addItem(self.scatters[type_event])
            self.legend_ev.addItem(self.scatters[type_event], name=event_name)

    def set_event_point(self, data: dict):
        """ добавление на график точек событий """
        ev = data["signal"]
        t = ev.Counter / self._sig_datablock.sample_rate

        y_pos = 0
        if self._y_min:
            y_pos = self._y_min

        if ev.Type == EventType.FREEFALL.bit_length() - 1 and "freefall" in self.scatters:
            self.point_scatters["freefall"].append({"pos": (t, y_pos)})
        if ev.Type == EventType.ORIENTATION.bit_length() - 1 and "orientation" in self.scatters:
            self.point_scatters["orientation"].append({"pos": (t, y_pos)})
        if ev.Type == EventType.ACTIVITY.bit_length() - 1 and "activity" in self.scatters:
            self.point_scatters["activity"].append({"pos": (t, y_pos)})
        # if ev.Type == EventType.TEMP.bit_length() - 1:
        #     self.legend_temp.clear()
        #     self.legend_temp.addItem(ItemSample(item=None), f"{round(ev.Data / 1000, 1)}°C")

        return

    def process_input(self, data: dict):
        """ обработка входящего сигнала и добавление в буфер """
        if data["type"] == "ev":
            self.set_event_point(data)
            return

        current_sample, signal = data["sample"], data["signal"]  # .shape = (1,32) for exg; .shape = (3,8) for acc

        if self.unit == "uV":
            signal /= 1e6   # to V

        # todo: добавить проверку сигнала на соответствие channels_count, count_per_samples
        if not self._buffer_filled:
            if self.current_position + self._sig_datablock.counter_per_sample < self._signal_buffer.shape[1]:
                self._signal_buffer[:, self.current_position: self.current_position + self._sig_datablock.counter_per_sample] = signal
                self.current_position += self._sig_datablock.counter_per_sample
            else:
                offset = self._signal_buffer.shape[1] - self.current_position
                self._signal_buffer[:, self.current_position: ] = signal[:, :offset]
                signal = signal[:, offset:]
                self._buffer_filled = True

        if self._buffer_filled and signal.shape[1] != 0:
            self._signal_buffer = np.roll(self._signal_buffer, -signal.shape[1])
            self._signal_buffer[:, -signal.shape[1]:] = signal
            self._time_buffer += signal.shape[1] * (1 / self._sig_datablock.sample_rate)

        self.update_display = True

    def timerEvent(self, _, /):
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
            start_idx = end_idx - int(self._timebase * self._sig_datablock.sample_rate)

        visible_time = self._time_buffer[start_idx:end_idx]
        for ch in range(self._sig_datablock.number_channels):
            self.traces[ch].setData(visible_time, self._signal_buffer[ch, start_idx: end_idx])

            # for test
            v_min = self._signal_buffer[ch, start_idx:end_idx].min()
            v_max = self._signal_buffer[ch, start_idx:end_idx].max()

        # подстройка по оси времени
        if not self._buffer_filled and end_idx <= self._timebase * self._sig_datablock.sample_rate:
            self.setXRange(0, self._timebase, padding=0)
        else:
            current_time = visible_time[-1] if len(visible_time) > 0 else 0
            self.setXRange(current_time - self._timebase, current_time, padding=0)

        # self.setYRange(self.y_min, self.y_max)
        self.release_event_points()

        if self._y_min and self._y_max:
            self.setYRange(self._y_min, self._y_max, padding=0.1)

        self.update_display = False

    def release_event_points(self):
        """ отрисовка точек событий на графике"""
        if len(self.scatters.keys()) == 0:
            return

        for ev in self.scatters.keys():
            self.scatters[ev].addPoints(self.point_scatters[ev])
            self.point_scatters[ev] = list()    # сброс событий

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
        """ запуск потока по обработке очереди """
        while self._running:
            try:
                data = self._input_queue.get(False)
                self.process_input(data)
            except queue.Empty:
                pass
            except Exception as exc:
                pass

            time.sleep(0.001)

    def _transmit_data(self, data):
        """ передача данных в очередь обработки """
        try:
            self._input_queue.put(data, False)
        except:
            pass

class TempStreamViewer(pg.PlotWidget):
    """ Виджет отображения сигнала температуры """

    def __init__(self, left_label: str | None = None, units: str | None = None, *args, **kwargs):
        kwargs['axisItems'] = {'bottom': FormatterTimeAxisItem(orientation="bottom")}
        super().__init__(*args, **kwargs)

        self.setBackground((64,64,64))
        self.setEnabled(False)

        white_pen = pg.mkPen(color='w')
        font = QFont("Arial", 9)

        self._timebase = 600

        # отображение температуры с помощью графика рассеяния
        self.temp_scatter = ScatterPlotItem(pen=pg.mkPen((255,255,0)), brush=pg.mkBrush('y'))
        self.addItem(self.temp_scatter)

        # отображение текущего значения температуры в легенде
        self.legend_temp = LegendItem(labelTextSize="25pt", labelTextColor="white")
        self.legend_temp.setParentItem(self.graphicsItem())
        self.legend_temp.anchor(itemPos=(1, 0.5), parentPos=(1, 0.5))
        empty_sample = ItemSample(item=None)
        self.legend_temp.addItem(empty_sample, "--°C")

        self.setLabel("left", left_label, units=units, color="white") # "°C",
        self.setLabel("bottom", color="white") # "Время", units="s",
        for ax in ["bottom", "left"]:
            self.getAxis(ax).label.setFont(font)
            self.getAxis(ax).setPen(white_pen)
            self.getAxis(ax).setTickPen(white_pen)
            self.getAxis(ax).setTextPen(white_pen)
            self.getAxis(ax).setTickFont(font)

        self.setYRange(20, 45, padding=0)
        self.setXRange(0, self._timebase, padding=0)

        self.lines = []

    def set_temperature(self, t: float, value: float):
        """ установка температуры в график """
        line = self.plot([t, t], [0, value], pen=pg.mkPen("y", width=0.5))
        self.temp_scatter.addPoints([{'pos': (t, value)}])

        if self.legend_temp:
            self.legend_temp.clear()
            empty_sample = ItemSample(item=None)
            self.legend_temp.addItem(empty_sample, f"{value}°C")

        self.lines.append(line)

        # регулировка отображения
        if t < self._timebase:
            self.setXRange(0, self._timebase, padding=0)
        else:
            self.setXRange(t - self._timebase, t, padding=0)
        self.setYRange(20, 45, padding=0)

    def set_timebase(self, value: float):
        """ установка окна вывода графика """
        self._timebase = value

    def clear_plot(self):
        """ очистка графика при перезапуске """
        for line in self.lines:
            self.removeItem(line)
        self.temp_scatter.clear()
        self.lines.clear()

        self.legend_temp.clear()
        # self.legend_temp.addItem(self.temp_scatter, f"--°C")
        empty_sample = ItemSample(item=None)
        self.legend_temp.addItem(empty_sample, f"--°C")

        self.setYRange(20, 45, padding=0)
        self.setXRange(0, self._timebase, padding=0)

    # def disable_legend(self):
    #     """Отключение и удаление легенды с графика"""
    #     if self.legend_temp is not None:
    #         self.legend_temp.clear()
    #         self.removeItem(self.legend_temp)
    #         self.legend_temp = None

class FormatterTimeAxisItem(pg.AxisItem):
    """ формат mm:ss по оси x """
    def tickStrings(self, values, scale, spacing) -> list[str]:
        """ форматирование строки по оси времени """
        strings = []
        last_value = None
        for value in values:
            is_whole_second = abs(value - round(value)) < 1e-9  # для float
            if is_whole_second:
                minutes = int(value // 60)
                seconds = int(value % 60)
                tick_str = f"{minutes:02d}:{seconds:02d}"
                if tick_str != last_value:
                    strings.append(tick_str)
                    last_value = tick_str
            else:
                strings.append("")
        return strings