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
from PySide6.QtWidgets import QFrame, QFileDialog

from pyedflib import EdfWriter
from typing import Optional

from device.constants import Const
from device.device import SignalDatablock
from device.enums import EventType, TypeSignal
from device.utils import get_orientation
from resources.frm_online_control_recording import Ui_FrmOnlineControlRecording

logger = logging.getLogger(__name__)


class DataStorage(QObject):

    """
    Класс для сохранения сигналов с устройства в форматы EDF
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._input_queue = Queue()

        # параметры записи биосигнала
        self._exg_writer: None | EdfWriter = None
        self._exg_datablock: None | SignalDatablock = None
        self._exg_filename = None
        self._exg_buffer = None
        self._exg_buffer_stream = None
        self._exg_start_sample = None   # начальный семпл записи
        self._exg_current_sample = None
        self._exg_samples_written = 0    # количество записанных в буфер семплов
        self._exg_recording_start = None
        self._idx_start_exg = None
        self._idx_finish_exg = None

        # параметры записи акселерометра
        self._acc_writer: None | EdfWriter = None
        self._acc_datablock: None | SignalDatablock = None
        self._acc_filename = None
        self._acc_buffer = None
        self._acc_buffer_stream = None
        self._acc_start_sample = None   # начальный семпл записи
        self._acc_current_sample = None
        self._acc_samples_written = 0    # количество записанных в буфер семплов
        self._acc_recording_start = None
        self._idx_start_acc = None
        self._idx_finish_acc = None

        self._ev_buffer = []
        self._buffer_dur = 1
        self._max_timebase = 1200

        # параметры записи
        self._format = "EDF"         # выбранный формат записи
        self._recording_start = None
        self._device_name = None

        # путь и названия файлов записи
        self._filename = None
        self._writedir = None
        self._selected_folder = None # "./data"
        # os.makedirs(self._selected_folder, exist_ok=True)

        self._recording = False # флаг начала записи
        self._running = False
        self._work: Thread | None = None

        self._control_pane = FrmOnlineControlRecording(self)
        self._control_pane.pushButtonStartRecording.clicked.connect(self._prepare_recording)
        self._control_pane.pushButtonStopRecording.clicked.connect(self._close_recording)
        self._control_pane.pushButtonSelectSaveDir.clicked.connect(self.handle_select_save_location)

    def create_edf_writer(self, param: SignalDatablock | None) -> None:
        """ создание edf writer для указанного типа сигнала """
        # todo обработка исключений
        if not param:
            return

        if not self._writedir:
            raise ValueError("Не указана директория сохранения файлов")

        os.makedirs(self._writedir, exist_ok=True)

        path_to_save = f"{self._writedir}/{param.type_signal.value}_test.edf"
        writer = EdfWriter(n_channels=param.number_channels, file_name=path_to_save)

        for idx_ch in range(param.number_channels):
            channel_info = {
                'label': param.type_signal.value,
                'dimension': param.units,
                'sample_frequency': param.sample_rate,
                'physical_max': param.physical_max, 'physical_min': param.physical_min,
                'digital_max': 32767, 'digital_min': -32768
            }
            writer.setSignalHeader(idx_ch, channel_info)

        record_start = datetime.datetime.now()
        # setup
        writer.set_number_of_annotation_signals(number_of_annotations=64)
        writer.setEquipment(param.device_name)
        writer.setStartdatetime(record_start)

        if param.type_signal == TypeSignal.ECG or param.type_signal == TypeSignal.EEG:
            self._exg_writer = writer
            self._exg_recording_start = record_start
        elif param.type_signal == TypeSignal.ACC:
            self._acc_writer = writer
            self._acc_recording_start = record_start
        else:
            raise ValueError(f"Неизвестный тип сигнала {param.type_signal}")

        logger.debug(f"Инициализирован указатель на файл для записи сигнала {param.type_signal}")

    def handle_select_save_location(self):
        """ выбор место сохранения записей """

        selected_folder = QFileDialog.getExistingDirectory(
            None,
            "Выберите папку для сохранения записей",
            self._selected_folder,
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks,  # несколько опций
        )

        if selected_folder:
            self._selected_folder = selected_folder

    @property
    def control_pane(self):
        return self._control_pane

    def start(self):
        """ запуск записи данных """
        while not self._input_queue.empty():
            self._input_queue.get_nowait()

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

        self._recording = False
        self._running = False
        self._control_pane.set_disable()
        if self._work:
            self._work.join(5.0)
            self._work = None

    def update_params(self, params_exg: SignalDatablock | None, params_acc: SignalDatablock | None):
        """ обновление параметров записи сигналов """
        # обновление параметров записи для биосигналов
        self._exg_datablock = params_exg

        if params_exg:
            self._exg_filename = params_exg.type_signal.value
            self._exg_buffer = np.zeros((params_exg.number_channels, params_exg.sample_rate * self._max_timebase), dtype=np.float32)
            self._exg_buffer_stream = np.zeros((params_exg.number_channels, params_exg.sample_rate * self._buffer_dur),
                                        dtype=np.float32)

            self._exg_start_sample = 0  # начальный семпл записи
            self._exg_current_sample = 0
            self._exg_samples_written = 0

        # обновление параметров записи для акселерометра
        self._acc_datablock = params_acc
        if params_acc:
            self._acc_filename = params_acc.type_signal.value
            self._acc_buffer = np.zeros((params_acc.number_channels, params_acc.sample_rate * self._max_timebase),
                                        dtype=np.float32)
            self._acc_buffer_stream = np.zeros((params_acc.number_channels, params_acc.sample_rate * self._buffer_dur),
                                        dtype=np.float32)

            self._acc_start_sample = 0  # начальный семпл записи
            self._acc_current_sample = 0
            self._acc_samples_written = 0

        if params_exg:
            self._device_name = self._exg_datablock.device_name
        elif params_acc:
            self._device_name = self._acc_datablock.device_name

    def _prepare_recording(self):
        """ подготовка и запись данных """
        logger.debug(f"Подготовка для начала записи {DataStorage.__name__}")
        if not self._selected_folder:
            self.handle_select_save_location()

        now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self._writedir = f"{self._selected_folder}/{str(self._device_name)}/rec_{now}/"

        self.create_edf_writer(param=self._exg_datablock)
        self.create_edf_writer(param=self._acc_datablock)

        self._recording = True
        self._control_pane.pushButtonStopRecording.setEnabled(True)
        self._control_pane.pushButtonStartRecording.setEnabled(False)
        self._control_pane.pushButtonSelectSaveDir.setEnabled(False)

    def _close_recording(self):
        """ остановка записи"""
        logger.debug(f"Остановка записи {DataStorage.__name__}")
        self._recording = False

        if self._format == "WFDB":
            logger.error(f"Формат WFDB не поддерживается!")
            pass

        if self._format == "EDF":
            os.makedirs(self._writedir, exist_ok=True)

            if self._exg_datablock:
                idx_start = 0
                idx_finish = self._exg_samples_written * self._exg_datablock.counter_per_sample
                signal = self._exg_buffer[:,idx_start:idx_finish]

                sig_start_datetime = datetime.datetime.fromtimestamp(self._exg_recording_start)
                self._save_to_edf(
                    sample_rate=self._exg_datablock.sample_rate,
                    number_channels=self._exg_datablock.number_channels,
                    signal=signal,
                    events=self._ev_buffer,
                    write_dir=self._writedir,
                    filename=self._exg_filename,
                    channel_names=self._exg_datablock.channel_names,
                    units=self._exg_datablock.units,
                    start_datetime=sig_start_datetime,
                    device_name=self._exg_datablock.device_name
                )

            if self._acc_datablock:
                idx_start = 0
                idx_finish = self._acc_samples_written * self._acc_datablock.counter_per_sample
                acc_signal = self._acc_buffer[:,idx_start:idx_finish]

                acc_start_datetime = datetime.datetime.fromtimestamp(self._acc_recording_start)
                self._save_to_edf(
                    sample_rate=self._acc_datablock.sample_rate,
                    number_channels=self._acc_datablock.number_channels,
                    signal=acc_signal,
                    write_dir=self._writedir,
                    filename=self._acc_filename,
                    channel_names=self._acc_datablock.channel_names,
                    units=self._acc_datablock.units,
                    start_datetime=acc_start_datetime,
                    device_name=self._acc_datablock.device_name
                )

        if self._exg_writer:
            self._exg_writer.close()
            self._exg_writer = None

        if self._acc_writer:
            self._acc_writer.close()
            self._acc_writer = None

        self._control_pane.pushButtonStartRecording.setEnabled(True)
        self._control_pane.pushButtonStopRecording.setEnabled(False)
        self._control_pane.pushButtonSelectSaveDir.setEnabled(True)

    def process_input(self, data: dict):
        """ сохранение данных в буфер
        # TODO: добавить обработку пропущенных семплов
        """
        if not self._recording:
            return data

        # logger.debug(f"Получены данные для сохранения в {DataStorage.__name__}: {data=}")

        type = data["type"]
        if self._exg_datablock and type == "ev":
            # self._process_input_ev(data)
            self._process_input_ev_stream(data)

        if self._exg_datablock and type == "sig":
            self._process_input_exg(data)
            self._process_input_exg_stream(data)

        if self._acc_datablock and type == "acc":
            self._process_input_acc(data)
            self._process_input_acc_stream(data)

        return data

    def _process_input_exg_stream(self, data: dict):
        """ обработка exg сигнала """
        exg: np.ndarray = data["signal"]
        sample: int = data["sample"]

        # инициализация индексов
        if not self._idx_start_exg:
            self._idx_start_exg = 0
            self._idx_finish_exg = exg.shape[1]

        buffer_width = self._exg_buffer_stream.shape[1]

        # проверка на заполнение буфера
        if self._idx_finish_exg >= buffer_width:
            remaining_space = buffer_width - self._idx_start_exg
            self._exg_buffer_stream[:, self._idx_start_exg:] = exg[:, :remaining_space]  # заполнение буфера до конца

            self._exg_writer.writeSamples(self._exg_buffer_stream)

            remaining_data = exg.shape[1] - remaining_space
            if remaining_data > 0:
                self._exg_buffer_stream[:, :remaining_data] = exg[:, remaining_space:]
            self._idx_start_exg = remaining_data
            self._idx_finish_exg = remaining_data + exg.shape[1]

        else:
            self._exg_buffer_stream[:, self._idx_start_exg:self._idx_finish_exg] = exg
            self._idx_start_exg += exg.shape[1]
            self._idx_finish_exg += exg.shape[1]

        return data

    def _process_input_acc_stream(self, data: dict):
        """ обработка acc """
        acc: np.ndarray = data["signal"]
        sample: int = data["sample"]

        # инициализация индексов
        if not self._idx_start_acc:
            self._idx_start_acc = 0
            self._idx_finish_acc = acc.shape[1]

        buffer_width = self._acc_buffer_stream.shape[1]

        # проверка на заполнение буфера
        if self._idx_finish_acc >= buffer_width:
            remaining_space = buffer_width - self._idx_start_acc
            self._acc_buffer_stream[:, self._idx_start_acc:] = acc[:, :remaining_space]  # заполнение буфера до конца

            self._exg_writer.writeSamples(self._acc_buffer_stream)

            remaining_data = acc.shape[1] - remaining_space
            if remaining_data > 0:
                self._acc_buffer_stream[:, :remaining_data] = acc[:, remaining_space:]
            self._idx_start_exg = remaining_data
            self._idx_finish_exg = remaining_data + acc.shape[1]

        else:
            self._acc_buffer_stream[:, self._idx_start_exg:self._idx_finish_exg] = acc
            self._idx_start_exg += acc.shape[1]
            self._idx_finish_exg += acc.shape[1]

        return data

    def _process_input_ev(self, data: dict):
        """ обработка входящий событий
        data: {"sample": int(event.Counter / Pkt.SamplesCountEcg), "counter": event.Counter, "signal": event, "type": "ev"}
        """
        event = data["signal"]
        t = (event.Counter - self._exg_start_sample * self._exg_datablock.counter_per_sample) / self._exg_datablock.sample_rate

        if event.Type == EventType.FREEFALL.bit_length() - 1:
            ann = "F"
        elif event.Type == EventType.ACTIVITY.bit_length() - 1:
            ax = int(Const.AccResolution * event.Acceleration.X)
            ay = int(Const.AccResolution * event.Acceleration.Y)
            az = int(Const.AccResolution * event.Acceleration.Z)
            ann = f"A {ax} {ay} {az}"
        elif event.Type == EventType.ORIENTATION.bit_length() - 1:
            axis = get_orientation(event.Value)
            ann = f"O {axis}"
        elif event.Type == EventType.TEMP.bit_length() - 1:
            ann = f"T {round(event.Data / 1000, 1)}"
        else:
            return data

        self._ev_buffer.append((t, ann))
        return data

    def _process_input_ev_stream(self, data: dict):
        """ запись событий в потоке в edf файл"""
        event = data["signal"]
        t = (event.Counter - self._exg_start_sample * self._exg_datablock.counter_per_sample) / self._exg_datablock.sample_rate

        ann = "None"
        if event.Type == EventType.FREEFALL.bit_length() - 1:
            ann = "F"
        elif event.Type == EventType.ACTIVITY.bit_length() - 1:
            ax = int(Const.AccResolution * event.Acceleration.X)
            ay = int(Const.AccResolution * event.Acceleration.Y)
            az = int(Const.AccResolution * event.Acceleration.Z)
            ann = f"A {ax} {ay} {az}"
        elif event.Type == EventType.ORIENTATION.bit_length() - 1:
            axis = get_orientation(event.Value)
            ann = f"O {axis}"
        elif event.Type == EventType.TEMP.bit_length() - 1:
            ann = f"T {round(event.Data / 1000, 1)}"

        self._exg_writer.writeAnnotation(description=ann, onset_in_seconds=t, duration_in_seconds=0)

    def _process_input_exg(self, data: dict) -> dict:
        """ обработка входящих биосигналов """
        sig, sample = data["signal"], data["sample"]

        if not self._exg_start_sample:
            self._exg_start_sample = sample
            self._exg_recording_start = time.time()

        idx_start = (sample - self._exg_start_sample) * self._exg_datablock.counter_per_sample
        idx_finish = (sample - self._exg_start_sample) * self._exg_datablock.counter_per_sample + self._exg_datablock.counter_per_sample

        # дошли до конца буфера? закрываем запись
        if idx_finish >= self._exg_buffer.shape[1]:
            self._close_recording()
            return data

        self._exg_buffer[:, idx_start:idx_finish] = sig
        self._exg_samples_written += 1
        return data

    def _process_input_acc(self, data: dict) -> dict:
        """ обработка входящих сигналов акселерометра """
        if data["type"] != "acc":
            return data

        acc, sample = data["signal"], data["sample"]
        if not self._acc_start_sample:
            self._acc_start_sample = sample
            self._acc_recording_start = time.time()

        idx_start = (sample - self._acc_start_sample) * self._acc_datablock.counter_per_sample
        idx_finish = (sample - self._acc_start_sample) * self._acc_datablock.counter_per_sample + self._acc_datablock.counter_per_sample

        # дошли до конца буфера?
        if idx_finish >= self._acc_buffer.shape[1]:
            self._close_recording()
            return data

        self._acc_buffer[:, idx_start:idx_finish] = acc
        self._acc_samples_written += 1
        return data

    def _transmit_data(self, data):
        """ принять данные и положить в очередь на обработку """
        try:
            self._input_queue.put(data, False)
        except:
            ...

    def _save_to_edf(
            self,
            sample_rate: int,
            number_channels: int,
            signal: np.ndarray,
            units: str,
            write_dir: str,
            filename: str,
            channel_names: list,
            start_datetime: datetime.datetime,
            events: list | None = None,
            device_name: str | None = None
    ):
        """ сохранение сигнала в edf файл """
        path_to_save = f"{write_dir}/{filename}.edf"
        writer = EdfWriter(n_channels=number_channels, file_name=path_to_save)
        writer.set_number_of_annotation_signals(number_of_annotations=64)

        if units == "V":
            signal = np.round(signal * 1e6, decimals=3) # to uV
            units = "uV"
        else:
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

        if events:
            for data in events:
                if len(data) == 2:
                    t, ann = data[0], data[1]
                    writer.writeAnnotation(onset_in_seconds=t, description=ann, duration_in_seconds=0)

        headers = []
        for ch in range(number_channels):
            channel_info = {
                'label': channel_names[ch],
                'dimension': units,
                'sample_frequency': sample_rate,
                'physical_max': physical_max,
                'physical_min': physical_min,
                'digital_max': 32767,
                'digital_min': -32768,
            }
            headers.append(channel_info)

        if device_name:
            writer.setEquipment(device_name)
        writer.setStartdatetime(start_datetime)
        writer.setSignalHeaders(headers)
        writer.writeSamples(signal)
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
        self.pushButtonSelectSaveDir.setEnabled(True)
        self.pushButtonStartRecording.setEnabled(True)
        self.pushButtonStopRecording.setEnabled(False)

    def set_disable(self):
        self.pushButtonSelectSaveDir.setEnabled(False)
        self.pushButtonStartRecording.setEnabled(False)
        self.pushButtonStopRecording.setEnabled(False)

    def timerEvent(self, event, /):
        if self.module._recording:
            self._timer += 1
        else:
            self._timer = 0
        self.labelRecordingTime.setText(to_str_mmss(self._timer))