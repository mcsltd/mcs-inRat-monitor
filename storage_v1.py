import copy
import queue
import time
import numpy as np

from threading import Thread

from PySide6.QtCore import QObject

from device.device import SignalDatablock
from storage import FrmOnlineControlRecording


class Storage(QObject):

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
        self._write_dir = None
        self._filename = None
        self._selected_dir = None
        # exg params recording
        self._exg_param = None
        self._exg_buffer = None
        # acc params recording
        self._acc_param = None
        self._acc_buffer = None

        # ui panels
        self._control_pane = FrmOnlineControlRecording(self)
        self._control_pane.pushButtonStartRecording.clicked.connect(self._prepare_recording)
        self._control_pane.pushButtonStopRecording.clicked.connect(self._close_recording)

    @property
    def control_pane(self):
        return self._control_pane

    def start(self):
        """ запуск модуля """
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
        if self._exg_param and (data_type == "ev" or data_type == "sig"):
            self.__process_exg(data)
        if self._acc_param and data_type == "acc":
            self.__process_acc(data)

    def _transmit_data(self, data):
        """ передача данных в очередь для обработки """
        try:
            self._input_queue.put(data, False)
        except Exception as err:
            pass

    def update_params(
            self,
            params_exg: SignalDatablock | None = None,
            params_acc: SignalDatablock | None = None
    ):
        """ метод инициализации параметров записи """
        if params_acc:
            self._acc_param = copy.copy(params_acc)
            self._acc_buffer = np.zeros(
                (
                    self._acc_param.number_channels,
                    self._acc_param.sample_rate * self._sec_buffer_size
                ), dtype=np.float32
            )

        if params_exg:
            self._exg_param = copy.copy(params_exg)
            self._exg_buffer = np.zeros(
                (
                    self._exg_param.number_channels,
                    self._exg_param.sample_rate * self._sec_buffer_size),
                dtype=np.float32
            )

    def process_start(self):
        """ метод инициализации параметров перед стартом """
        pass

    def process_stop(self):
        """ метод очистки после остановки """
        pass

    def _close_recording(self):
        """ метод закрытия записи и сохранения данных """
        self._recording = False

        self._control_pane.pushButtonStartRecording.setEnabled(True)
        self._control_pane.pushButtonStopRecording.setEnabled(False)
        self._control_pane.pushButtonSelectSaveDir.setEnabled(True)

    def _prepare_recording(self):
        """ метод подготовки к записи """
        self._recording = True

        self._control_pane.pushButtonStopRecording.setEnabled(True)
        self._control_pane.pushButtonStartRecording.setEnabled(False)
        self._control_pane.pushButtonSelectSaveDir.setEnabled(False)
