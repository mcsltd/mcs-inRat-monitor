import csv
import datetime
import logging
import os.path
import time
from queue import Queue
from threading import Thread

import numpy as np
import wfdb
from PySide6.QtCore import QObject, QTimer
from PySide6.QtWidgets import QFrame

from pyedflib import EdfWriter
from typing import Optional

from resources.frm_online_control_recording import Ui_FrmOnlineControlRecording

logger = logging.getLogger(__name__)


class DataStorage(QObject):

    """ Класс для сохранения сигналов с устройства в форматы EDF/WFDB"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._input_queue = Queue()
        self._signal_buffer = np.zeros(144_000_000, dtype=np.float32) # 20 минут на 2000 Гц на одном канале

        self._recording = False

        # параметры записи
        self._format = None         # выбранный формат записи
        self._sample_rate = None    # частота записи
        self._samples_count = None  # количество отсчётов в семпле
        self._samples_written = 0    # количество записанных в буфер семплов
        self._start_sample = None   # начальный семпл записи
        self._current_sample = None
        self._recording_start = None
        self._device_name = None

        # путь и названия файлов записи
        self._filename = None
        self._writedir = None

        self._running = False
        self._work: Thread | None = None

        self._control_pane = FrmOnlineControlRecording(self)
        self._control_pane.pushButtonStartRecording.clicked.connect(self._prepare_recording)
        self._control_pane.pushButtonStopRecording.clicked.connect(self._close_recording)


    @property
    def control_pane(self):
        return self._control_pane

    def start(self):
        """ запуск записи данных """
        self._control_pane.set_enable()
        if not self._running:
            self._running = True
            self._work = Thread(target=self._worker_thread)
            self._work.start()

    def _worker_thread(self):
        """ Рабочий поток получает данные из входной очереди
            и помещает обработанные данные в выходную очередь """
        logger.debug(f"Запуск рабочего потока для {DataStorage.__name__}")
        while self._running:
            # обработка очереди данных
            try:
                data = self._input_queue.get(False)
                self.process_input(data)
            except Exception as exc:
                ...

            time.sleep(0.001)

    def stop(self):
        """ остановка записи данных """
        logger.debug(f"Остановка рабочего потока для {DataStorage.__name__}")

        self._running = False
        self._control_pane.set_disable()
        if self._work:
            self._work.join(5.0)
            self._work = None

    def set_recording_params(self, sample_rate: int, frmt: str, samples_count: int, device_name: str):
        """ установка параметров записи """
        self._sample_rate = sample_rate
        self._format = frmt
        self._samples_count = samples_count
        self._device_name = device_name

    def process_event(self, event):
        """ обработка событий """
        if event == "StartRecording":
            self._prepare_recording()
        if event == "StopRecording":
            self._close_recording()

    def _prepare_recording(self):
        """ подготовка и запись данных """
        logger.debug(f"Подготовка для начала записи {DataStorage.__name__}")
        self._recording = True
        self._control_pane.pushButtonStopRecording.setEnabled(True)
        self._control_pane.pushButtonStartRecording.setEnabled(False)

        now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self._writedir = f"./data/{str(self._device_name)}/rec_{now}/"
        self._filename = "ecg"

    def _close_recording(self):
        """ остановка записи"""
        logger.debug(f"Остановка записи {DataStorage.__name__}")
        self._recording = False

        idx_start = 0
        idx_finish = self._samples_written * self._samples_count
        signal = self._signal_buffer[idx_start:idx_finish]

        if self._format == "WFDB":
            # self._save_to_wfdb(signal)
            pass

        if self._format == "EDF":
            os.makedirs(self._writedir, exist_ok=True)
            self._save_to_edf(signal=signal, write_dir=self._writedir, filename=self._filename)

        self._control_pane.pushButtonStartRecording.setEnabled(True)
        self._control_pane.pushButtonStopRecording.setEnabled(False)

    def process_input(self, data: dict):
        """ сохранение данных в буфер
        # TODO: добавить обработку пропущенных семплов
        """
        if not self._recording:
            return data

        logger.debug(f"Получены данные для сохранения в {DataStorage.__name__}: {data=}")

        sample = data["counter"]
        signal = data["signal"]

        if not self._start_sample:
            self._start_sample = sample
            self._recording_start = time.time()

        idx_start = (sample - self._start_sample) * self._samples_count
        idx_finish = (sample - self._start_sample) * self._samples_count + len(signal)

        # дошли до конца буфера?
        if idx_finish >= len(self._signal_buffer):
            self._close_recording()
            return data

        self._signal_buffer[idx_start:idx_finish] = signal
        self._samples_written += 1

        return data

    def _save_to_edf(self, signal: np.ndarray, write_dir: str, filename: str):
        """ сохранение сигнала в edf файл """
        path_to_save = f"{write_dir}/{filename}.edf"
        writer = EdfWriter(n_channels=1, file_name=path_to_save)
        signal = np.round(signal, decimals=6)
        margin = 0.15

        # Проверяем, есть ли ненулевой сигнал
        signal_max = np.max(signal)
        signal_min = np.min(signal)

        # Если сигнал нулевой или все значения близки к нулю
        if np.allclose(signal_max, 0.0) and np.allclose(signal_min, 0.0):
            # Устанавливаем небольшой ненулевой диапазон
            physical_max = 1.0  # или другое подходящее значение
            physical_min = -1.0
        else:
            # Обрабатываем нормальный случай
            if signal_max > 0:
                physical_max = np.round(signal_max * (1 + margin), decimals=3)
            else:
                physical_max = np.round(signal_max * (1 - margin), decimals=3)

            if signal_min > 0:
                physical_min = np.round(signal_min * (1 - margin), decimals=3)
            else:
                physical_min = np.round(signal_min * (1 + margin), decimals=3)

        if np.allclose(physical_max, physical_min):
            physical_max = physical_max + 1.0
            physical_min = physical_min - 1.0

        channel_info = {
            'label': "signal",
            'dimension': "V",
            'sample_frequency': self._sample_rate,
            'physical_max': physical_max,
            'physical_min': physical_min,
            'digital_max': 32767,
            'digital_min': -32768,
        }

        writer.setSignalHeader(0, channel_info)
        writer.writeSamples(signal[np.newaxis])
        writer.close()


def to_str_mmss(seconds) -> str:
    str_mm_ss = f"{int(seconds // 60):02d}:{seconds % 60:02d}"
    return str_mm_ss

def to_str_hhmmss(seconds) -> str:
    str_mm_ss = f"{int(seconds // 60):02d}:{seconds % 60:02d}"
    return str_mm_ss

class FrmOnlineControlRecording(QFrame, Ui_FrmOnlineControlRecording):

    def __init__(self, module, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.module = module

        self._timer = 0
        self.startTimer(1000)

    def set_enable(self):
        self.pushButtonStartRecording.setEnabled(True)
        self.pushButtonStopRecording.setEnabled(False)
        self.comboBoxFormat.setEnabled(True)

    def set_disable(self):
        self.pushButtonStartRecording.setEnabled(False)
        self.pushButtonStopRecording.setEnabled(False)
        self.comboBoxFormat.setEnabled(False)

    def timerEvent(self, event, /):
        if self.module._recording:
            self._timer += 1
        else:
            self._timer = 0
        self.labelRecordingTime.setText(to_str_mmss(self._timer))