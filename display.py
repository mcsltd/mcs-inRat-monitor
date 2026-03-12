import queue
import threading
import time

import numpy as np

from pyqtgraph import PlotWidget, PlotDataItem
from device.device import ECG_DataBlock


class inRatDisplay(PlotWidget):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.plot_ecg: PlotDataItem = self.plot()

        # настройки подписи к графикам
        self.setLabel("left", "V")
        self.setLabel("bottom", "t (с)")

        self.ecg = ECG_DataBlock()

        self.offset = 0
        self.timebase = 10.0  # in seconds
        self.dt_x = 1 / self.ecg.sample_rate
        self.x_values = np.arange(0.0, self.timebase, self.dt_x)
        self.ecg_buffer = np.zeros(len(self.x_values))
        self.max_size_buffer = len(self.ecg_buffer)

        self._running = False
        self._work = None
        self._input_queue = queue.Queue()

        self.setXRange(0.0, self.timebase, padding=0.0)
        self.setMenuEnabled(False)
        self.setMouseEnabled(False, False)

    def start(self):
        """ запуск обработки очереди """
        while not self._input_queue.empty():
            self._input_queue.get_nowait()

        if not self._running:
            self._running = True
            self._work = threading.Thread(target=self._worker_thread)
            self._work.start()

    def process_input(self, datablock: ECG_DataBlock):
        """ обработка входящего блока данных """
        self.ecg = datablock
        self.set_display()

    def set_display(self):
        """ отображение ЭКГ на графике """
        offset = len(self.ecg.ecg_channels)
        if self.offset + offset < len(self.ecg_buffer):
            self.ecg_buffer[self.offset:self.offset+offset] = self.ecg.ecg_channels
            self.offset += offset
        else:
            self.ecg_buffer[:self.max_size_buffer - offset] = self.ecg_buffer[offset:] # отсекаем старую часть
            self.ecg_buffer[self.max_size_buffer - offset:] = self.ecg.ecg_channels # добавляем новую часть сигнала

        self.plot_ecg.setData(self.x_values, self.ecg_buffer)
        self.replot()

    def process_output(self):
        """ обработка остановки """
        return None

    def process_stop(self):
        """ обработка остановки """
        self.clear()
        self.plot_ecg: PlotDataItem = self.plot()

        self.offset = 0
        self.dt_x = 1 / self.ecg.sample_rate
        self.x_values = np.arange(0.0, self.timebase, self.dt_x)
        self.ecg_buffer = np.zeros(len(self.x_values))

    def _transmit_data(self, data):
        """ получение данных от класса inrat"""
        self._input_queue.put(data, False)

    def _worker_thread(self):
        """ запуск цикла на обработку и получение данных """
        while self._running:
            try:
                data = self._input_queue.get(block=False)
                self.process_input(data)
            except:
                pass

            try:
                data = self.process_output()
            except:
                pass

            time.sleep(0.001)

    def stop(self):
        """ остановка """
        self._running = False
        if self._work:
            self._work.join(1.0)
            self._work = None
        self.process_stop()
