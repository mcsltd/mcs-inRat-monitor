import csv
import datetime
import logging
import os.path
import time
from queue import Queue
from threading import Thread

import numpy as np
import wfdb
from PySide6.QtCore import QObject

from pyedflib import EdfWriter
from typing import Optional


logger = logging.getLogger(__name__)

class Storage:
    def __init__(self, path_to_save: str, fs: int):
        self.ecg = np.array([])
        self.buffer_temp = []
        self.buffer_activity = []

        self.is_recording = None

        self.path_to_save = os.path.abspath(path_to_save)
        self.fs = fs

        self._device_name = None
        self._format = "WFDB" # default format
        self.start_time: Optional[datetime.datetime] = None

    def set_format(self, frmt):
        """
        Change format save file.
        :param frmt: str - name of select format
        """
        logger.debug(f"Change format: {self._format} -> {frmt}")
        self._format = frmt

    def set_save_dir(self, path: str):
        """ Save record in save dir. Raise error if dir is not exists. """
        if os.path.isdir(path):
            self.path_to_save = path
        else:
            raise ValueError("Dir is not exists!")

    def set_device_name(self, name):
        self._device_name = name

    def get_file_name(self):
        str_st: str = str(self.start_time.date()) + "_" + str(self.start_time.time().replace(microsecond=0))
        for _ in range(str_st.count(":")): str_st = str_st.replace(":", "-")

        dur = int(self.ecg.shape[0] / self.fs)
        filename = f"{str_st}_dur-{dur}"
        return filename

    def save(self):
        """ Save in select format """
        logger.debug(f"ECG buffer size: {self.ecg.shape}")

        if self.ecg.shape[0] == 0:
            return

        # write_dir = f"{self.path_to_save}\\{self._device_name}\\{self.start_time.date()}\\{self._format.lower()}"
        # write_dir = f"{self.path_to_save}\\{self._device_name}\\{self._format.lower()}\\"

        filename = self.get_file_name()
        write_dir = f"{self.path_to_save}\\{self._device_name}\\{filename}"

        # create dir for saving files with selected format
        os.makedirs(write_dir, exist_ok=True)

        try:
            if self._format == "WFDB":
                filename = "ecg"
                self._to_wfdb(record_name=filename, write_dir=write_dir)
        except Exception as err:
            logger.error(f"Ошибка сохранения в WFDB: {err=}")

        try:
            if self._format == "EDF":
                filename = "ecg"
                self._to_edf(f"{write_dir}\\{filename}.edf")
        except Exception as err:
            logger.error(f"Ошибка сохранения в EDF: {err=}")

        try:
            if len(self.buffer_temp) != 0:
                filename_csv = f"{write_dir}\\temperature.csv"
                self.to_csv(data=self.buffer_temp, filednames=list(self.buffer_temp[0].keys()), filepath=filename_csv)
        except Exception as err:
            logger.error(f"Ошибка сохранения температуры в CSV: {err=}")

        try:
            if len(self.buffer_activity) != 0:
                filename_csv = f"{write_dir}\\activity.csv"
                self.to_csv(data=self.buffer_activity, filednames=list(self.buffer_activity[0].keys()), filepath=filename_csv)
        except Exception as err:
            logger.error(f"Ошибка сохранения активности в CSV: {err=}")

        self.ecg = np.array([])
        self.buffer_temp = []
        self.buffer_activity = []
        self.start_time = None
        self.is_recording = False


    def _to_wfdb(
            self, record_name: str, write_dir: str, sig_name:list[str]=["ECG"], units: list[str] = ["V"],
    ):
        """
        Save data in wfdb format.
        """
        logger.debug("Save ecg in WFDB format.")
        wfdb.io.wrsamp(
            record_name=record_name,
            fs=self.fs, units=units, p_signal=self.ecg[np.newaxis].T,
            sig_name=sig_name, write_dir=write_dir, base_datetime=self.start_time
        )

    def _to_edf(
            self,
            filename: str,
            units: str = "V",
            sig_name: str = "ECG",
    ):
        """
        Save data in edf format.
        """
        logger.debug("Save ecg in EDF format.")
        writer = EdfWriter(n_channels=1, file_name=filename)
        self.ecg = np.round(self.ecg, decimals=6)

        margin = 0.15

        # Проверяем, есть ли ненулевой сигнал
        signal_max = np.max(self.ecg)
        signal_min = np.min(self.ecg)

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

        # Дополнительная проверка на равенство min и max
        if np.allclose(physical_max, physical_min):
            # Расширяем диапазон
            physical_max = physical_max + 1.0
            physical_min = physical_min - 1.0

        channel_info = {
            'label': sig_name,
            'dimension': units,
            'sample_frequency': self.fs,
            'physical_max': physical_max,
            'physical_min': physical_min,
            'digital_max': 32767,
            'digital_min': -32768,
        }

        writer.setSignalHeader(0, channel_info)
        writer.setEquipment("None" if self._device_name is None else self._device_name)
        writer.writeSamples(self.ecg[np.newaxis])
        writer.close()

    def __call__(self, ecg):
        if self.ecg.shape[0] == 0:
            self.start_time = datetime.datetime.now()
        self.ecg = np.append(self.ecg, ecg)

    def process_temperature(self, ev_temp):
        try:
            self.buffer_temp.append({"time_sec": int(ev_temp.counter / self.fs), "temp_celsius": round(ev_temp.data / 1000, 1)})
        except Exception as err:
            logger.error(f"Ошибка добавления в буфер температуры: {err}")

    def process_activity(self, ev_activity):
        try:
            self.buffer_activity.append({"time_sec": ev_activity.counter / self.fs, "description": ev_activity.type})
        except Exception as err:
            logger.error(f"Ошибка добавления в буфер активности: {err}")

    def to_csv(self, data: list[dict], filednames: list[str], filepath: str) -> None:
        try:
            with open(filepath, "w", newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=filednames)
                writer.writeheader()
                writer.writerows(data)
            logger.info(f"Данные успешно сохранены в {filepath}")
        except Exception as err:
            logger.info(f"Возникла ошибка при сохранении в {filepath}: {err}")



class DataStorage(QObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._input_queue = Queue()
        self._signal_buffer = np.zeros(144_000_000, dtype=np.float32) # 20 минут на максимальной частоте

        self._recording = False

        # параметры записи
        self._format = None         # выбранный формат записи
        self._sample_rate = None    # частота записи
        self._samples_count = None  # количество отсчётов в семпле
        self._samples_written = 0    # количество записанных в буфер семплов
        self._start_sample = None   # начальный семпл записи
        self._current_sample = None
        self._recording_start = None

        # путь и названия файлов записи
        self._file_name = None
        self._write_dir = None

        self._running = False
        self._work: Thread | None = None

    def start(self):
        """ запуск записи данных """
        if not self._running:
            self._running = True
            self._work = Thread(target=self._worker_thread)
            self._work.start()

    def _worker_thread(self):
        """ Рабочий поток получает данные из входной очереди
            и помещает обработанные данные в выходную очередь """
        while self._running:
            # обработка очереди данных
            try:
                data = self._input_queue.get(False)
                self.process_input(data)
            except Exception as exc:
                pass

    def stop(self):
        """ остановка записи данных """
        self._running = False
        if self._work:
            self._work.join(5.0)
            self._work = None

    def set_recording_params(self, sample_rate: int, frmt: str, samples_count: int):
        """ установка параметров записи"""
        self._sample_rate = sample_rate
        self._format = frmt
        self._samples_count = samples_count

    def process_event(self, event):
        """ обработка событий """
        if event == "StartRecording":
            self._prepare_recording()
        if event == "StopRecording":
            self._close_recording()

    def _prepare_recording(self):
        """ подготовка и запись данных """
        self._recording = True

    def _close_recording(self):
        """ остановка записи"""
        self._recording = False

        idx_start = 0
        idx_finish = self._samples_written * self._samples_count
        signal = self._signal_buffer[idx_start:idx_finish]

        if self._format == "WFDB":
            # self._save_to_wfdb(signal)
            pass

        if self._format == "EDF":
            self._save_to_edf(signal)

    def process_input(self, data: dict):
        """ сохранение данных в буфер
        # TODO: добавить обработку пропущенных семплов
        """
        if not self._running:
            return data

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

    def _save_to_edf(self, signal: np.ndarray):
        """ сохранение сигнала в edf файл """
        writer = EdfWriter(n_channels=1, file_name="some_signal")
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