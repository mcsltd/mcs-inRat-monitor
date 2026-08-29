import copy
import logging
import queue
import time
import numpy as np

from threading import Thread
from PySide6.QtCore import QObject
from pyedflib import EdfWriter

from device.device import SignalDatablock
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
        self._sec_buffer_size = 1200 # 20 minute
        self._format = "edf"
        self._device_name = None
        self._object_name = None
        self._write_dir = None
        self._filename = None
        self._selected_dir = None
        # exg params recording
        self._exg_param = None
        self._exg_buffer = None
        self._exg_start_sample = None
        # acc params recording
        self._acc_param = None
        self._acc_buffer = None
        self._acc_start_sample = None

        # ui panels
        self._control_pane = FrmOnlineControlRecording(self)
        self._control_pane.pushButtonStartRecording.clicked.connect(self._prepare_recording)
        self._control_pane.pushButtonStopRecording.clicked.connect(self._close_recording)

    @property
    def control_pane(self):
        return self._control_pane

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
            self._acc_start_sample = None
            self._acc_buffer = np.zeros(
                (
                    self._acc_param.number_channels,
                    self._acc_param.sample_rate * self._sec_buffer_size
                ), dtype=np.float32
            )

        if params_exg:
            self._exg_param = copy.copy(params_exg)
            self._acc_start_sample = None
            self._exg_buffer = np.zeros(
                (
                    self._exg_param.number_channels,
                    self._exg_param.sample_rate * self._sec_buffer_size),
                dtype=np.float32
            )

    def process_start(self):
        """ метод инициализации параметров перед стартом """
        self._control_pane.set_enable()

    def process_stop(self):
        """ метод очистки после остановки """
        if self._recording:
            self._close_recording()

        self._control_pane.set_disable()

    def _close_recording(self):
        """ метод закрытия записи и сохранения данных """
        logger.debug(f"{self.__class__}: закрытие записи")
        self._recording = False
        acc_signal, exg_signal = None, None

        if self._acc_param:
            idx_finish = (self._acc_last_sample - self._acc_start_sample) * self._acc_param.counter_per_sample
            length_acc_sec = self._acc_buffer[:,:idx_finish].shape[1] / self._acc_param.sample_rate
            acc_signal = self._acc_buffer[:,:idx_finish]

            self._acc_buffer = np.zeros(
                (self._acc_param.number_channels, self._acc_param.sample_rate * self._sec_buffer_size),
                dtype=np.float32
            )
            self._acc_start_sample = None
            logger.debug(f"Буфер acc очищен, было записано сигнала - {length_acc_sec} сек.")

        if self._exg_param:
            idx_finish = (self._exg_last_sample - self._exg_start_sample) * self._exg_param.counter_per_sample
            length_exg_sec = self._exg_buffer[:, :idx_finish].shape[1] / self._exg_param.sample_rate
            exg_signal = self._exg_buffer[:,:idx_finish]

            self._exg_buffer = np.zeros(
                (self._exg_param.number_channels, self._exg_param.sample_rate * self._sec_buffer_size),
                dtype=np.float32
            )
            self._exg_start_sample = None
            logger.debug(f"Буфер exg очищен, было записано сигнала - {length_exg_sec} сек.")

        self.save_signals_to_edf(acc=acc_signal, exg=exg_signal)

        self._control_pane.pushButtonStartRecording.setEnabled(True)
        self._control_pane.pushButtonStopRecording.setEnabled(False)
        self._control_pane.pushButtonSelectSaveDir.setEnabled(True)

    def _prepare_recording(self):
        """ метод подготовки к записи """
        logger.debug(f"{self.__class__}: открытие на запись")
        self._recording = True

        self._control_pane.pushButtonStopRecording.setEnabled(True)
        self._control_pane.pushButtonStartRecording.setEnabled(False)
        self._control_pane.pushButtonSelectSaveDir.setEnabled(False)

    def __process_exg(self, data: dict):
        """ сохранение сигнала exg в буфер """
        sig, sample = data["signal"], data["sample"]
        if self._exg_start_sample is None:
            self._exg_start_sample = sample

        idx_start = (sample - self._exg_start_sample) * self._exg_param.counter_per_sample
        idx_finish = (sample - self._exg_start_sample) * self._exg_param.counter_per_sample + self._exg_param.counter_per_sample
        if idx_finish >= self._exg_buffer.shape[1]:
            self._close_recording()

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
            self._close_recording()

        self._acc_buffer[:, idx_start:idx_finish] = acc
        self._acc_last_sample = sample

    def __process_ev(self, data: dict):
        """ сохранение сигнала exg в буффер """
        # print(f"{data}")
        pass

    def save_signals_to_edf(self, acc: None | np.ndarray = None, exg: None | np.ndarray = None):
        """ сохранение сигналов в edf файл """
        channels_info = []
        channel_template = dict.fromkeys(
            [
                'label', 'dimension', 'sample_frequency', 'physical_max', 'physical_min', 'digital_max', 'digital_min'
            ], None
        )
        total_channels = 0
        signals = []

        if self._acc_param:
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
            # signals.append(exg)

        # file_name = self._write_dir + f"{self._filename}.edf"
        file_name = "./data/test.edf"
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
        writer.close()
