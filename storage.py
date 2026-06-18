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
from device.enums import EventType
from device.utils import get_orientation
from resources.frm_online_control_recording import Ui_FrmOnlineControlRecording

logger = logging.getLogger(__name__)


class DataStorage(QObject):

    """ Класс для сохранения сигналов с устройства в форматы EDF/WFDB
        # ToDo: обновление параметров под выбранную частоту
        # ToDo: сброс параметров при перезапуске модуля
        # ToDo: добавления нескольких каналов в signal_buffer
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._input_queue = Queue()
        self._recording = False

        # параметры записи биосигнала
        self._sig_datablock: None | SignalDatablock = None
        self._sig_filename = None
        self._sig_buffer = None
        self._sig_start_sample = None   # начальный семпл записи
        self._sig_current_sample = None
        self._sig_samples_written = 0    # количество записанных в буфер семплов

        # параметры записи акселерометра
        self._acc_datablock: None | SignalDatablock = None
        self._acc_filename = None
        self._acc_buffer = None
        self._acc_start_sample = None   # начальный семпл записи
        self._acc_current_sample = None
        self._acc_samples_written = 0    # количество записанных в буфер семплов

        self._ev_buffer = []

        self._max_timebase = 1200 # 20 минут

        # параметры записи
        self._format = "EDF"         # выбранный формат записи
        self._recording_start = None
        self._device_name = None

        # путь и названия файлов записи
        self._filename = None
        self._writedir = None
        self._selected_folder = "./data"
        os.makedirs(self._selected_folder, exist_ok=True)

        self._running = False
        self._work: Thread | None = None

        self._control_pane = FrmOnlineControlRecording(self)
        self._control_pane.pushButtonStartRecording.clicked.connect(self._prepare_recording)
        self._control_pane.pushButtonStopRecording.clicked.connect(self._close_recording)
        self._control_pane.pushButtonSelectSaveDir.clicked.connect(self.handle_select_save_location)

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

        self._running = False
        self._control_pane.set_disable()
        if self._work:
            self._work.join(5.0)
            self._work = None

    def update_params(self, params_sig: SignalDatablock | None, params_acc: SignalDatablock | None):
        """ обновление параметров записи сигналов """
        # обновление параметров записи для биосигналов
        self._sig_datablock = params_sig
        self._device_name = self._sig_datablock.device_name
        if params_sig:
            self._sig_filename = params_sig.type_signal.value
            self._sig_buffer = np.zeros((params_sig.number_channels, params_sig.sample_rate * self._max_timebase), dtype=np.float32)

            self._sig_start_sample = 0  # начальный семпл записи
            self._sig_current_sample = 0
            self._sig_samples_written = 0

        # обновление параметров записи для акселерометра
        self._acc_datablock = params_acc
        if params_acc:
            self._acc_filename = params_acc.type_signal.value
            self._acc_buffer = np.zeros((params_acc.number_channels, params_acc.sample_rate * self._max_timebase),
                                        dtype=np.float32)

            self._acc_start_sample = 0  # начальный семпл записи
            self._acc_current_sample = 0
            self._acc_samples_written = 0

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
        self._control_pane.pushButtonSelectSaveDir.setEnabled(False)

        now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self._writedir = f"{self._selected_folder}/{str(self._device_name)}/rec_{now}/"

    def _close_recording(self):
        """ остановка записи"""
        logger.debug(f"Остановка записи {DataStorage.__name__}")
        self._recording = False

        if self._format == "WFDB":
            logger.error(f"Формат WFDB не поддерживается!")
            pass

        if self._format == "EDF":
            os.makedirs(self._writedir, exist_ok=True)

            if self._sig_datablock:
                idx_start = 0
                idx_finish = self._sig_samples_written * self._sig_datablock.counter_per_sample
                signal = self._sig_buffer[:,idx_start:idx_finish]

                sig_start_datetime = datetime.datetime.fromtimestamp(self._sig_recording_start)
                self._save_to_edf(
                    sample_rate=self._sig_datablock.sample_rate,
                    number_channels=self._sig_datablock.number_channels,
                    signal=signal,
                    events=self._ev_buffer,
                    write_dir=self._writedir,
                    filename=self._sig_filename,
                    channel_names=self._sig_datablock.channel_names,
                    units=self._sig_datablock.units,
                    start_datetime=sig_start_datetime,
                    device_name=self._sig_datablock.device_name
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

        self._control_pane.pushButtonStartRecording.setEnabled(True)
        self._control_pane.pushButtonStopRecording.setEnabled(False)
        self._control_pane.pushButtonSelectSaveDir.setEnabled(True)

    def process_input(self, data: dict):
        """ сохранение данных в буфер
        # TODO: добавить обработку пропущенных семплов
        """
        if not self._recording:
            return data

        logger.debug(f"Получены данные для сохранения в {DataStorage.__name__}: {data=}")

        type = data["type"]
        if self._sig_datablock and type == "ev":
            self._process_input_ev(data)

        if self._sig_datablock and type == "sig":
            self._process_input_sig(data)

        if self._acc_datablock and type == "acc":
            self._process_input_acc(data)

        return data

    def _process_input_ev(self, data: dict):
        """ обработка входящий событий
        data: {"sample": int(event.Counter / Pkt.SamplesCountEcg), "counter": event.Counter, "signal": event, "type": "ev"}
        """
        event = data["signal"]
        t = (event.Counter - self._sig_start_sample * self._sig_datablock.counter_per_sample) / self._sig_datablock.sample_rate

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

    def _process_input_sig(self, data: dict) -> dict:
        """ обработка входящих биосигналов """
        sig, sample = data["signal"], data["sample"]

        if not self._sig_start_sample:
            self._sig_start_sample = sample
            self._sig_recording_start = time.time()

        idx_start = (sample - self._sig_start_sample) * self._sig_datablock.counter_per_sample
        idx_finish = (sample - self._sig_start_sample) * self._sig_datablock.counter_per_sample + self._sig_datablock.counter_per_sample

        # дошли до конца буфера? закрываем запись
        if idx_finish >= self._sig_buffer.shape[1]:
            self._close_recording()
            return data

        self._sig_buffer[:, idx_start:idx_finish] = sig
        self._sig_samples_written += 1
        return data

    def _process_input_acc(self, data: dict) -> dict:
        """ обработка входящих сигналов акселерометра """
        if data["type"] != "acc":
            return data

        acc, sample = data["signal"], data["sample"]
        if not self._acc_start_sample:
            self._acc_start_sample = sample
            self._acc_recording_start = time.time()

        idx_start = (sample - self._sig_start_sample) * self._acc_datablock.counter_per_sample
        idx_finish = (sample - self._sig_start_sample) * self._acc_datablock.counter_per_sample + self._acc_datablock.counter_per_sample

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