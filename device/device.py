import asyncio
import logging
import time
from asyncio import AbstractEventLoop
from concurrent.futures import Future
from threading import Thread

import numpy as np
from PySide6.QtCore import QObject, Signal
from bleak import BLEDevice

from device.constants import Pkt
from device.enums import EnabledChannels, TypeSignal
from device.inrat import inRat, FIRMWARE_V1, FIRMWARE_V0
from device.ui.config_dialog import DlgConfigDevice
from device.ui.control_pane import FrmControlPane

logger = logging.getLogger(__name__)


class SignalDatablock:
    """
        класс, описывающий структуру передаваемого сигнала
        используется для настройки всех модулей
    """
    def __init__(
            self,
            type_signal: TypeSignal, sample_rate: int, counter_per_sample: int,
            number_channels: int, channel_names: list, units: str
    ):
        self.type_signal: TypeSignal = type_signal
        self.number_channels = number_channels
        self.sample_rate = sample_rate
        self.sample_counter = None
        self.counter_per_sample = counter_per_sample
        self.channel_names = channel_names
        self.signal = np.zeros((self.number_channels, self.counter_per_sample), np.float32)
        self.units = units

class inRatDevice(QObject):

    signal_connected = Signal()
    signal_disconnected = Signal()

    signal_enable_sig = Signal(bool)
    signal_enable_acc = Signal(bool)

    """ класс для работы с inRat """

    def __init__(self, loop: asyncio.AbstractEventLoop | None = None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._loop: AbstractEventLoop = loop
        self._inrat: inRat | None = None

        # очередь для передачи всех данных с устройства
        self._receivers_data = []

        # ресурсы для обработки событий и биосигналов
        self._work_sig: Thread | None = None
        self._sig_datablock = SignalDatablock(type_signal=TypeSignal.ECG,
                                              sample_rate=500,
                                              counter_per_sample=Pkt.SamplesCountEcg,
                                              number_channels=Pkt.ChannelsCountEcg,
                                              channel_names=["ecg"],
                                              units="V")
        self._receivers_sig = []
        self._event_queue = None
        self._sig_queue = asyncio.Queue()

        # ресурсы для обработки показаний акселерометра
        self._work_acc: Thread | None = None
        self._acc_datablock = SignalDatablock(type_signal=TypeSignal.ACC,
                                              sample_rate=100,
                                              counter_per_sample=Pkt.SamplesCountAcc,
                                              number_channels=Pkt.ChannelsCountAcc,
                                              channel_names=["acc_x", "acc_y", "acc_z"],
                                              units="mg")
        self._receivers_acc = []
        self._acc_queue = asyncio.Queue()

        # флаг выполнения рабочего потока
        self._running: bool = False

        # фрейм для управления устройством
        self._control_pane = FrmControlPane()
        self._control_pane.pushButtonStart.clicked.connect(self.start)
        self._control_pane.pushButtonStop.clicked.connect(self.stop)
        self._control_pane.pushButtonConfig.clicked.connect(self.on_config_clicked)

    @property
    def control_pane(self):
        return self._control_pane

    def add_receiver_data(self, receiver):
        """ добавление объекта-приёмник всех данных  """
        if self._running:
            receiver.start()
        self._receivers_data.append(receiver)

    def remove_receiver_data(self, receiver):
        """ удалить объект приёмника из коллекции """
        if receiver in self._receivers_data:
            self._receivers_data.remove(receiver)
        receiver.stop()

    def add_receiver_sig(self, receiver):
        """ добавить объект приёмника в коллекцию биосигналов """
        if self._running:
            receiver.start()
        self._receivers_sig.append(receiver)

    def remove_receiver_sig(self, receiver):
        """ удалить объект приёмника биосигналов из коллекции """
        if receiver in self._receivers_sig:
            self._receivers_sig.remove(receiver)
        receiver.stop()

    def add_receiver_acc(self, receiver):
        """ добавить объект приёмника акселерометра в коллекцию """
        if self._running:
            receiver.start()
        self._receivers_acc.append(receiver)

    def remove_receiver_acc(self, receiver):
        """ удалить объект приёмника из коллекции акселерометра """
        if receiver in self._receivers_acc:
            self._receivers_acc.remove(receiver)
        receiver.stop()

    def process_connect(self, device: BLEDevice):
        """ обработка соединения с inRat """
        self._inrat = inRat(ble_device=device)
        future = asyncio.run_coroutine_threadsafe(self._inrat.connect(), self._loop)
        future.add_done_callback(self.on_device_connected)

    def on_device_connected(self, future: Future):
        """ обработка результата соединения с устройством """
        if self._inrat.is_connected:
            self._control_pane.state_connection()
            self.signal_connected.emit()

            # настройка параметров inrat под версию firmware
            if self._inrat.firmware == FIRMWARE_V0:
                self._inrat.enabled_channels = EnabledChannels.ECG
                self._inrat.sample_rate = 500
                self._inrat.activity_threshold = 2

                self.signal_enable_sig.emit(True)

            if self._inrat.firmware == FIRMWARE_V1:
                self._inrat.enabled_channels = EnabledChannels.ECG | EnabledChannels.ACC_X | EnabledChannels.ACC_Z | EnabledChannels.ACC_Y
                self._inrat.sample_rate = 500
                self._inrat.activity_threshold = 2

                self.signal_enable_acc.emit(True)
                self.signal_enable_sig.emit(True)

        else:
            self._control_pane.state_disconnect()

    def process_disconnect(self):
        """ обработка соединения с inRat """
        future = asyncio.run_coroutine_threadsafe(self._inrat.disconnect(), self._loop)
        self.signal_disconnected.emit()
        self._control_pane.state_disconnect()

        self.signal_enable_acc.emit(False)
        self.signal_enable_sig.emit(False)

    def process_start(self):
        """ обработка запуска устройства """
        self._control_pane.state_acquisition()

    def start(self):
        """ запуск inRat на получение данных """
        try:
            self.process_start()
        except Exception as exc:
            logger.error(f"Exception: {exc}")
            return

        future = asyncio.run_coroutine_threadsafe(
            self._inrat.start_acquisition(signal_queue=self._sig_queue, acceleration_queue=self._acc_queue), self._loop
        )

        for receiver in self._receivers_sig:
            receiver.update_params(self._sig_datablock)
            receiver.start()
        for receiver in self._receivers_acc:
            receiver.update_params(self._acc_datablock)
            receiver.start()
        for receiver in self._receivers_data:
            receiver.update_params(params_acc=self._acc_datablock, params_sig=self._sig_datablock)
            receiver.start()

        if not self._running:
            self._running = True
            self._work_sig = Thread(target=self._worker_thread_sig)
            self._work_acc = Thread(target=self._worker_thread_acc)
            self._work_sig.start()
            self._work_acc.start()

        logger.debug("Запущен поток обработки приёма и обработки данных с inRat")

    def _worker_thread_sig(self):
        """ Рабочий поток получает данные из входной очереди биосигналов
            и помещает обработанные данные в выходную очередь """
        while self._running:
            try:
                signal = self._sig_queue.get_nowait()
            except asyncio.queues.QueueEmpty:
                signal = None
            else:
                # logger.debug(f"Получены данные: {signal=}")
                self._sig_queue.task_done()

            if signal:
                for receiver in self._receivers_sig:
                    receiver._transmit_data(signal)

                for receiver in self._receivers_data:
                    receiver._transmit_data(signal)

            time.sleep(0.001)

    def _worker_thread_acc(self):
        """ Рабочий поток получает данные из входной очереди акселерометра
                    и помещает обработанные данные в выходную очередь """
        while self._running:
            try:
                acc = self._acc_queue.get_nowait()
            except asyncio.queues.QueueEmpty:
                acc = None
            else:
                # logger.debug(f"Получены данные: {signal=}")
                self._acc_queue.task_done()

            if acc:
                for receiver in self._receivers_acc:
                    receiver._transmit_data(acc)

                for receiver in self._receivers_data:
                    receiver._transmit_data(acc)

            time.sleep(0.001)

    def stop(self):
        """ остановка получения данных с inRat """
        future = asyncio.run_coroutine_threadsafe(self._inrat.stop_acquisition(), self._loop)

        self._running = False
        if self._work_acc:
            self._work_acc.join(1.5)
            self._work_acc = None

        if self._work_acc:
            self._work_acc.join(1.5)
            self._work_acc = None

        for receiver in self._receivers_acc:
            receiver.stop()

        for receiver in self._receivers_sig:
            receiver.stop()

        for receiver in self._receivers_data:
            receiver.stop()

        self.process_stop()
        logger.debug("Поток обработки приёма и обработки данных с inRat остановлен")

    def process_stop(self):
        """ обработка остановки устройства """
        self._control_pane.state_connection()

    def on_config_clicked(self):
        """ обработка нажатия окна конфигураций """
        dlg = DlgConfigDevice(self._inrat)
        dlg.exec()

        # активация экг/ээг
        if bool(self._inrat.enabled_channels & EnabledChannels.ECG):
            self.signal_enable_sig.emit(True)

            self._sig_datablock = SignalDatablock(
                type_signal=self._inrat.mode,
                sample_rate=self._inrat.sample_rate,
                counter_per_sample=Pkt.SamplesCountEcg,
                number_channels=Pkt.ChannelsCountEcg,
                channel_names=[self._inrat.mode.name],  # list[str]
                units="V") # todo: check it
        else:
            self.signal_enable_sig.emit(False)
            self._sig_datablock = None

        # активация акселерометра
        if (
                bool(self._inrat.enabled_channels & EnabledChannels.ACC_X) and
                bool(self._inrat.enabled_channels & EnabledChannels.ACC_Y) and
                bool(self._inrat.enabled_channels & EnabledChannels.ACC_Z)
        ):
            self.signal_enable_acc.emit(True)
            self._acc_datablock = SignalDatablock(type_signal=TypeSignal.ACC,
                                                  sample_rate=100,
                                                  counter_per_sample=Pkt.SamplesCountAcc,
                                                  number_channels=Pkt.ChannelsCountAcc,
                                                  channel_names=["acc_x", "acc_y", "acc_z"],
                                                  units="mg")
        else:
            self.signal_enable_acc.emit(False)
            self._acc_datablock = None

        # обновление параметров
        for receiver in self._receivers_sig:
            receiver.update_params(self._sig_datablock)
        for receiver in self._receivers_acc:
            receiver.update_params(self._acc_datablock)
        for receiver in self._receivers_data:
            receiver.update_params(params_acc=self._acc_datablock, params_sig=self._sig_datablock)