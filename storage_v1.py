import copy
import datetime
import logging
import os
import queue
import time
import numpy as np

from threading import Thread, Lock
from PySide6.QtCore import QObject
from PySide6.QtWidgets import QFileDialog
from pyedflib import EdfWriter

from device.constants import Const
from device.device import SignalDatablock
from device.enums import EventType
from device.utils import get_orientation
from storage import FrmOnlineControlRecording

logger = logging.getLogger(__name__)

class Storage(QObject):
    """ класс для сохранения данных с устройства в EDF файл """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._input_queue = queue.Queue()

        self._recording = False
        self._running = False
        self._worker = None

        # general recording params
        self._recording_start_time = None
        self._sec_buffer_size = 1200
        # self._sec_buffer_size = 60  # for test
        self._format = "edf"
        self._device_name = None
        self._object_name = None
        self._write_dir = None
        self._filename = None
        self._selected_dir = None
        self._cnt_file = 0
        # exg params recording
        self._exg_param = None
        self._exg_buffer = None
        self._exg_start_sample = None
        # acc params recording
        self._acc_param = None
        self._acc_buffer = None
        self._acc_start_sample = None
        # event buffer
        self._ev_buffer = []

        self._thlock_save = Lock()

        # ui panels
        self._control_pane = FrmOnlineControlRecording(self)
        self._control_pane.pushButtonStartRecording.clicked.connect(self._prepare_recording)
        self._control_pane.pushButtonStopRecording.clicked.connect(self._close_recording)
        self._control_pane.pushButtonSelectSaveDir.clicked.connect(self._on_select_save_folder_clicked)

    @property
    def control_pane(self):
        return self._control_pane

    def _on_select_save_folder_clicked(self):
        """ выбор места сохранения для записей edf """
        write_dir = QFileDialog.getExistingDirectory(
            None,
            "Выберите папку для сохранения записей",
            self._write_dir,
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks,
        )

        if write_dir is None:
            logger.info("Не выбрана директория сохранения edf файлов")
            return
        self._write_dir = rf"{write_dir}"

    def start(self):
        """ запуск модуля """
        logger.debug(f"{self.__class__}: запуск модуля")
        while not self._input_queue.empty():
            self._input_queue.get_nowait()

        try:
            self.process_start()
        except Exception as err:
            return

        if not self._running:
            self._running = True
            self._worker = Thread(target=self._worker_thread)
            self._worker.start()

    def stop(self):
        """ остановка модуля """
        logger.debug(f"{self.__class__}: остановка модуля")
        self._recording = False
        self._running = False
        if self._worker:
            self._worker.join(1.0)
            self._worker = None

        try:
            self.process_stop()
        except Exception as err:
            pass

    def _worker_thread(self):
        """ запуск рабочего потока """
        logger.debug(f"{self.__class__}: запуск потока по обработке очереди")
        while self._running:
            try:
                data = self._input_queue.get(False)
                self.process_input(data)
            except queue.Empty:
                data = None

            time.sleep(0.001)

    def process_input(self, data):
        """ обработка входящих данных """
        data_type = data["type"]

        if not self._recording:
            return

        if self._exg_param:
            if data_type == "sig":
                self.__process_exg(data)
            if data_type == "ev":
                self.__process_ev(data)

        if self._acc_param and data_type == "acc":
            self.__process_acc(data)

    def _transmit_data(self, data):
        """ передача данных в очередь для обработки """
        try:
            self._input_queue.put(data, False)
        except Exception as err:
            logger.error(f"{self.__class__}: ошибка передачи данных в очередь - {err}")

    def update_params(
            self,
            params_exg: SignalDatablock | None = None,
            params_acc: SignalDatablock | None = None
    ):
        """ метод инициализации параметров записи """
        logger.debug(f"{self.__class__}: установка параметров записи")
        if params_acc:
            self._acc_param = copy.copy(params_acc)
            self._device_name = self._acc_param.device_name
            self._acc_start_sample = None
            self._acc_buffer = np.zeros(
                (
                    self._acc_param.number_channels,
                    self._acc_param.sample_rate * self._sec_buffer_size
                ), dtype=np.float32
            )

        if params_exg:
            self._exg_param = copy.copy(params_exg)
            self._device_name = self._exg_param.device_name
            self._exg_start_sample = None
            self._exg_buffer = np.zeros(
                (
                    self._exg_param.number_channels,
                    self._exg_param.sample_rate * self._sec_buffer_size),
                dtype=np.float32
            )

    def process_start(self):
        """ метод инициализации параметров перед стартом """
        self._control_pane.set_enable()
        self._control_pane.set_file_count(self._cnt_file)
        self._control_pane.timebase = self._sec_buffer_size

    def process_stop(self):
        """ метод очистки после остановки """
        if self._recording:
            self._close_recording()

        self._control_pane.set_disable()

    def _prepare_recording(self):
        """ метод подготовки к записи """
        logger.debug(f"{self.__class__}: открытие на запись")

        if self._write_dir is None:
            self._control_pane.pushButtonSelectSaveDir.click()

        self._recording = True
        self._recording_start_time = datetime.datetime.now()

        self._control_pane.pushButtonStopRecording.setEnabled(True)
        self._control_pane.pushButtonStartRecording.setEnabled(False)
        self._control_pane.pushButtonSelectSaveDir.setEnabled(False)

    def _close_recording(self):
        """ метод закрытия записи и сохранения данных """
        logger.debug(f"{self.__class__}: закрытие записи")
        self._recording = False

        self.__process_signals_for_save()

        self._control_pane.pushButtonStartRecording.setEnabled(True)
        self._control_pane.pushButtonStopRecording.setEnabled(False)
        self._control_pane.pushButtonSelectSaveDir.setEnabled(True)

    def __process_signals_for_save(self, ):
        """ обработка сигналов для сохранения в edf """
        # todo отделить обработку от сохранения
        acc_signal, exg_signal = None, None

        if self._acc_param:
            idx_finish = (self._acc_last_sample - self._acc_start_sample) * self._acc_param.counter_per_sample
            length_acc_sec = self._acc_buffer[:, :idx_finish].shape[1] / self._acc_param.sample_rate
            acc_signal = self._acc_buffer[:, :idx_finish]

            self._acc_buffer = np.zeros(
                (self._acc_param.number_channels, self._acc_param.sample_rate * self._sec_buffer_size),
                dtype=np.float32
            )
            self._acc_start_sample = None
            logger.debug(f"Буфер acc очищен, было записано сигнала - {length_acc_sec} сек.")

        if self._exg_param:
            idx_finish = (self._exg_last_sample - self._exg_start_sample) * self._exg_param.counter_per_sample
            length_exg_sec = self._exg_buffer[:, :idx_finish].shape[1] / self._exg_param.sample_rate
            exg_signal = self._exg_buffer[:, :idx_finish]

            self._exg_buffer = np.zeros(
                (self._exg_param.number_channels, self._exg_param.sample_rate * self._sec_buffer_size),
                dtype=np.float32
            )
            self._exg_start_sample = None
            logger.debug(f"Буфер exg очищен, было записано сигнала - {length_exg_sec} сек.")

        # заполнение пропущенных отсчётов acc
        if self._exg_param and self._acc_param:
            record_dur = exg_signal.shape[1] / self._exg_param.sample_rate
            lost = int(record_dur * self._acc_param.sample_rate - acc_signal.shape[1])
            logger.debug(f"Сигнал acc отстал на {lost} отсчётов; {lost / self._acc_param.sample_rate} c.")
            acc_signal = self.interpolate_missing_samples(acc_signal, lost)

        # todo заполнение acc по времени записи
        ev = self._ev_buffer.copy()
        self.save_signals_to_edf(acc=acc_signal, exg=exg_signal, ev=ev)
        self._ev_buffer = []

    def __process_exg(self, data: dict):
        """ сохранение сигнала exg в буфер """
        sig, sample = data["signal"], data["sample"]
        if self._exg_start_sample is None:
            self._exg_start_sample = sample

        idx_start = (sample - self._exg_start_sample) * self._exg_param.counter_per_sample
        idx_finish = (sample - self._exg_start_sample) * self._exg_param.counter_per_sample + self._exg_param.counter_per_sample
        if idx_finish >= self._exg_buffer.shape[1]:
            remain_cnt_exg = idx_finish - self._exg_buffer.shape[1]
            self.__switch_to_new_edf()  # переключение на запись в новый edf файл
            logger.debug(f"{self.__class__}: потеряно отсчётов exg при записи - {remain_cnt_exg}")
        else:
            self._exg_buffer[:, idx_start:idx_finish] = sig
            self._exg_last_sample = sample

    def __process_acc(self, data: dict):
        """ сохранение сигнала acc в буфер """
        acc, sample = data["signal"], data["sample"]
        if self._acc_start_sample is None:
            self._acc_start_sample = sample

        idx_start = (sample - self._acc_start_sample) * self._acc_param.counter_per_sample
        idx_finish = (sample - self._acc_start_sample) * self._acc_param.counter_per_sample + self._acc_param.counter_per_sample
        if idx_finish >= self._acc_buffer.shape[1]:
            remain_cnt_acc = idx_finish - self._acc_buffer.shape[1]
            logger.debug(f"{self.__class__}: потеряно отсчётов acc при записи - {remain_cnt_acc}")
            self.__switch_to_new_edf()  # переключение на запись в новый edf файл
        else:
            self._acc_buffer[:, idx_start:idx_finish] = acc
            self._acc_last_sample = sample

    def __process_ev(self, data: dict):
        """ сохранение сигнала exg в буфер """
        event = data["signal"]
        t, ann = None, None
        if event.Type == EventType.FREEFALL.bit_length() - 1:
            t = (event.Counter - self._exg_start_sample * self._exg_param.counter_per_sample) / self._exg_param.sample_rate
            ann = "F"
        elif event.Type == EventType.ACTIVITY.bit_length() - 1:
            t = (event.Counter - self._exg_start_sample * self._exg_param.counter_per_sample) / self._exg_param.sample_rate
            ax = int(Const.AccResolution * event.Acceleration.X)
            ay = int(Const.AccResolution * event.Acceleration.Y)
            az = int(Const.AccResolution * event.Acceleration.Z)
            ann = f"A {ax} {ay} {az}"
        elif event.Type == EventType.ORIENTATION.bit_length() - 1:
            t = (event.Counter - self._exg_start_sample * self._exg_param.counter_per_sample) / self._exg_param.sample_rate
            axis = get_orientation(event.Value)
            ann = f"O {axis}"
        elif event.Type == EventType.TEMP.bit_length() - 1:
            t = (event.Counter - self._exg_start_sample * self._exg_param.counter_per_sample) / self._exg_param.sample_rate
            ann = f"T {round(event.Data / 1000, 1)}"

        if t and ann:
            self._ev_buffer.append((t, ann))

    def save_signals_to_edf(
            self,
            acc: None | np.ndarray = None,
            exg: None | np.ndarray = None,
            ev: None | list[tuple] = None
    ):
        """ сохранение сигналов в edf файл """
        channels_info, signals = [], []
        channel_template = dict.fromkeys(
            [
                'label', 'dimension', 'sample_frequency', 'physical_max', 'physical_min', 'digital_max', 'digital_min'
            ], None
        )
        total_channels = 0
        filename = ""

        if self._acc_param:
            filename += f"{self._acc_param.type_signal.value}_"
            total_channels += self._acc_param.number_channels
            for idx_ch in range(self._acc_param.number_channels):
                info = channel_template.copy()
                info["digital_min"], info["digital_max"] = -32768, 32767
                info["physical_min"], info["physical_max"] = acc[idx_ch,:].min(), acc[idx_ch,:].max()
                info["label"] = self._acc_param.channel_names[idx_ch]
                info["dimension"] = self._acc_param.units
                info["sample_frequency"] = self._acc_param.sample_rate
                channels_info.append(info.copy())
                signals.append(acc[idx_ch, :])
        if self._exg_param:
            filename += f"{self._exg_param.type_signal.value}_"
            total_channels += self._exg_param.number_channels
            for idx_ch in range(self._exg_param.number_channels):
                info = channel_template.copy()
                info["digital_min"], info["digital_max"] = -32768, 32767
                info["physical_min"], info["physical_max"] = exg[idx_ch,:].min(), exg[idx_ch,:].max()
                info["label"] = self._exg_param.channel_names[idx_ch]
                info["dimension"] = self._exg_param.units
                info["sample_frequency"] = self._exg_param.sample_rate
                channels_info.append(info.copy())
                signals.append(exg[idx_ch, :])


        path_to_save = rf"{self._write_dir}\{self._device_name}"
        os.makedirs(path_to_save, exist_ok=True)

        start_time = self._recording_start_time.strftime("%H_%M_%S")
        file_name = f"{path_to_save}/{filename}{start_time}_{self._cnt_file:03d}.edf"
        writer = EdfWriter(n_channels=total_channels, file_name=file_name)

        if self._device_name:
            writer.setEquipment(self._device_name)
        if self._object_name:
            writer.setPatientName(self._object_name)
        if self._recording_start_time:
            writer.setStartdatetime(self._recording_start_time)
        for idx_ch in range(total_channels):
            writer.setSignalHeader(idx_ch, channels_info[idx_ch])
        writer.writeSamples(signals)

        if ev:
            for t, ann in self._ev_buffer:
                writer.writeAnnotation(onset_in_seconds=t, duration_in_seconds=0, description=ann)

        writer.close()

    def __switch_to_new_edf(self):
        """ переключение записи на новый файл при заполнении одного из буферов"""
        self._thlock_save.acquire()
        self._close_recording()
        self._prepare_recording()
        self._thlock_save.release()

        # увеличение счётчика записи
        self._cnt_file += 1
        self._control_pane.set_file_count(self._cnt_file)

    @staticmethod
    def interpolate_missing_samples(signal: np.ndarray, lost_samples: int) -> np.ndarray:
        """
        Вставляет lost_samples отсчетов в сигнал, разделяя его на lost_samples частей.
        Вставленные отсчёты - среднее от отсчётов слева и справа
        """
        logger.debug(f"Вставка в acc пропущенных отсчётов - {lost_samples}")

        if lost_samples <= 0:
            return signal.copy()

        n_channels, length = signal.shape
        part_size = length // lost_samples  # части на которые делится сигнал
        remainder = length % lost_samples  # остаток
        result_size = length + lost_samples
        recovery_signal = np.zeros((n_channels, result_size), dtype=signal.dtype)

        # позиции для вставки
        # массив размеров частей
        sizes = np.full(lost_samples, part_size, dtype=int)
        sizes[:remainder] += 1

        # вычисление cumulative суммы для позиций
        cumsum = np.cumsum(sizes)
        insert_positions = cumsum + np.arange(lost_samples) - 1

        # маска для исходных позиций
        mask = np.ones(result_size, dtype=bool)
        mask[insert_positions] = False
        # заполнение отсчётов
        recovery_signal[:, mask] = signal
        # расчёт индексов в исходном сигнале для вставок
        signal_indices = insert_positions - np.arange(lost_samples) - 1
        #  массив левых и правых индексов
        left_idx = signal_indices - 1
        right_idx = signal_indices
        # корректировка границы
        left_idx = np.clip(left_idx, 0, length - 1)
        right_idx = np.clip(right_idx, 0, length - 1)
        # первая вставка
        first_mask = (signal_indices == 0)
        # последняя вставка
        last_mask = (signal_indices == length - 1)

        # заполнение
        for ch in range(n_channels):
            # заполнение вставок средним соседних
            recovery_signal[ch, insert_positions] = (signal[ch, left_idx] + signal[ch, right_idx]) / 2
            # корректировка вставок
            if np.any(first_mask):
                recovery_signal[ch, insert_positions[first_mask]] = (signal[ch, 0] + signal[ch, 1]) / 2
            # последняя вставка
            if np.any(last_mask):
                recovery_signal[ch, insert_positions[last_mask]] = (signal[ch, -2] + signal[ch, -1]) / 2
        return recovery_signal