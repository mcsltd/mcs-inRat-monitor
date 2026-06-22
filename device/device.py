import asyncio
import logging
import time
from asyncio import AbstractEventLoop
from concurrent.futures import Future
from threading import Thread

import numpy as np
from PySide6.QtCore import QObject, Signal, Qt
from PySide6.QtWidgets import QMessageBox
from bleak import BLEDevice

from device.constants import Pkt
from device.enums import EnabledChannels, TypeSignal, EventType
from device.inrat import inRat, FIRMWARE_ACC_EXG, FIRMWARE_V0
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
            number_channels: int, channel_names: list, units: str, device_name: None | str = None
    ):
        self.type_signal: TypeSignal = type_signal
        self.number_channels: int = number_channels
        self.sample_rate: int = sample_rate
        self.sample_counter: int | None = None
        self.counter_per_sample: int = counter_per_sample
        self.channel_names: list[str] = channel_names
        self.signal: np.ndarray = np.zeros((self.number_channels, self.counter_per_sample), np.float32)
        self.units: str = units

        # события
        self.event_markers: list = list()
        self.type_events: list = list()

        self.device_name: str | None = device_name


class inRatDevice(QObject):

    signal_connected = Signal()
    signal_disconnected = Signal()
    signal_error = Signal(str)

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
        self._sig_datablock = SignalDatablock(type_signal=TypeSignal.ECG, sample_rate=500,
                                              counter_per_sample=Pkt.SamplesCountEcg,
                                              number_channels=Pkt.ChannelsCountEcg, channel_names=["ecg"], units="uV")
        self._receivers_sig = []
        # self._event_queue = asyncio.Queue()
        self._sig_queue = asyncio.Queue()

        # ресурсы для обработки показаний акселерометра
        self._work_acc: Thread | None = None
        self._acc_datablock = SignalDatablock(type_signal=TypeSignal.ACC, sample_rate=100,
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
        self._control_pane.checkBoxActivated.checkStateChanged.connect(self.on_state_activate_changed)

    def is_running(self) -> bool:
        return self._running

    @property
    def control_pane(self):
        return self._control_pane

    def add_receiver_data(self, receiver):
        """ добавление объекта-приёмник всех данных  """
        if self._running:
            receiver.start()
        if receiver not in self._receivers_data:
            self._receivers_data.append(receiver)
        else:
            logger.warning(f"Попытка дублировать {receiver} в приёмниках данных")
    def remove_receiver_data(self, receiver):
        """ удалить объект приёмника из коллекции """
        if receiver in self._receivers_data:
            self._receivers_data.remove(receiver)
        receiver.stop()

    def add_receiver_sig(self, receiver):
        """ добавить объект приёмника в коллекцию биосигналов """
        if self._running:
            receiver.start()

        if receiver not in self._receivers_sig:
            self._receivers_sig.append(receiver)
            receiver.update_params(params=self._sig_datablock)
        else:
            logger.warning(f"Попытка дублировать {receiver} в приёмниках сигналов ЭКГ/ЭМГ")
    def remove_receiver_sig(self, receiver):
        """ удалить объект приёмника биосигналов из коллекции """
        if receiver in self._receivers_sig:
            self._receivers_sig.remove(receiver)
        receiver.stop()

    def add_receiver_acc(self, receiver):
        """ добавить объект приёмника акселерометра в коллекцию """
        if self._running:
            receiver.start()
        if receiver not in self._receivers_acc:
            self._receivers_acc.append(receiver)
            receiver.update_params(params=self._acc_datablock)
        else:
            logger.warning(f"Попытка дублировать {receiver} в приёмниках акселерометра")

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
        try:
            future.result(timeout=10.0)
        except Exception as err:
            ...

        if self._inrat.is_connected:
            self._control_pane.state_connection()
            self.signal_connected.emit()

            if self._inrat.is_activated:
                self._control_pane.checkBoxActivated.setChecked(True)

            if self._acc_datablock:
                self._acc_datablock.device_name = self._inrat.name
            if self._sig_datablock:
                self._sig_datablock.device_name = self._inrat.name

            # настройка параметров inrat под версию firmware по умолчанию
            if self._inrat.firmware == FIRMWARE_V0:
                self._inrat.enabled_channels = EnabledChannels.ECG
                self._inrat.sample_rate = 500
                self._inrat.activity_threshold = 2

                self.signal_enable_sig.emit(True)

            else:
                if self._inrat.firmware not in FIRMWARE_ACC_EXG:
                    title = "Новая версия прошивки"
                    msg = f"Обнаружена новая версия прошивки {self._inrat.firmware}!"
                    QMessageBox.warning(None, title, msg, QMessageBox.StandardButton.Ok)

                self._inrat.enabled_channels = EnabledChannels.ECG | EnabledChannels.ACC_X | EnabledChannels.ACC_Z | EnabledChannels.ACC_Y
                self._inrat.sample_rate = 500
                self._inrat.activity_threshold = 2

                self.signal_enable_acc.emit(True)
                self.signal_enable_sig.emit(True)


        else:
            self._control_pane.state_disconnect()
            self.signal_disconnected.emit()
            msg = (f"Не удалось соединиться с {self._inrat.name}!\n"
                   f"Повторите попытку")
            self.signal_error.emit(msg)

    def process_disconnect(self):
        """ обработка соединения с inRat """
        future = asyncio.run_coroutine_threadsafe(self._inrat.disconnect(), self._loop)
        future.add_done_callback(self.on_device_disconnected)

    def on_device_disconnected(self, future: Future):
        """ обработка результата отсоединения от устройства """
        try:
            future.result(1.0)
        except Exception as exc:
            ...

        self.signal_disconnected.emit()

        if not self._inrat.is_connected:
            self._control_pane.state_disconnect()

        self.signal_enable_acc.emit(False)
        self.signal_enable_sig.emit(False)

    def start(self):
        """ запуск inRat на получение данных """
        while self._acc_queue and not self._acc_queue.empty():
                self._acc_queue.get_nowait()
        while self._sig_queue and not self._sig_queue.empty():
            self._sig_queue.get_nowait()

        try:
            self.process_start()
        except Exception as exc:
            logger.error(f"Exception: {exc}")
            return

        future = asyncio.run_coroutine_threadsafe(
            self._inrat.start_acquisition(
                signal_event_queue=self._sig_queue,
                acceleration_queue=self._acc_queue
            ), self._loop
        )
        future.add_done_callback(self.on_device_started)
        logger.debug("Запущена корутина на получение данных с inRat")

    def on_device_started(self, future: Future):
        """ обработка результата запуска устройства """
        try:
            if future.result(timeout=1.5):
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
            else:
                raise ValueError("...")
        except Exception as err:
            msg = (f"Возникла ошибка при запуске {self._inrat.name}\n"
                   f"Соединение будет сброшено")
            self.signal_error.emit(msg)
            self.process_disconnect()

    def process_start(self):
        """ обработка запуска устройства """
        self._control_pane.state_acquisition()

    def _worker_thread_sig(self):
        """ Рабочий поток получает данные из входной очереди биосигналов
            и помещает обработанные данные в выходную очередь
            переменная data, содержит:
            1) event: {"sample": int(event.Counter / Pkt.SamplesCountEcg), "counter": event.Counter,
                       "signal": event, "type": "ev"}
            2) signal: {"sample":smpl, "signal":signal, "type": "sig"}
        """
        while self._running:
            try:
                data = self._sig_queue.get_nowait()
            except asyncio.queues.QueueEmpty:
                data = None
            else:
                # logger.debug(f"Получены данные: {signal=}")
                self._sig_queue.task_done()

            if data:

                for receiver in self._receivers_sig:
                    receiver._transmit_data(data)

                for receiver in self._receivers_data:
                    receiver._transmit_data(data)

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

        # остановка классов-приёмников данных
        for receiver in self._receivers_acc:
            receiver.stop()
        for receiver in self._receivers_sig:
            receiver.stop()
        for receiver in self._receivers_data:
            receiver.stop()

        if self._work_acc:
            self._work_acc.join(1.5)
            self._work_acc = None

        if self._work_acc:
            self._work_acc.join(1.5)
            self._work_acc = None

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
                channel_names=[self._inrat.mode.value],  # list[str]
                units="V",
                device_name=self._inrat.name) # todo: check it

            # активация событий
            if bool(self._inrat.enabled_events & EventType.TEMP):
                self._sig_datablock.type_events.append("temp")
            if bool(self._inrat.enabled_events & EventType.ORIENTATION):
                self._sig_datablock.type_events.append("orientation")
            if bool(self._inrat.enabled_events & EventType.ACTIVITY):
                self._sig_datablock.type_events.append("activity")
            if bool(self._inrat.enabled_events & EventType.FREEFALL):
                self._sig_datablock.type_events.append("freefall")

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
                                                  units="G",
                                                  device_name=self._inrat.name)
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

    def on_state_activate_changed(self, state: Qt.CheckState):
        """ обработка активации/деактивации устройства """
        if state is Qt.CheckState.Checked:
            state = True
        else:
            state = False
        _ = asyncio.run_coroutine_threadsafe(self._inrat.activate(state), self._loop)
