import asyncio
import copy
import datetime
import logging
from asyncio import AbstractEventLoop, Queue, Event
from concurrent.futures import Future

import numpy as np
from PySide6.QtCore import QObject, Signal, QAbstractTableModel
from PySide6.QtWidgets import QFrame
from bleak import BLEDevice

from device.constants import SamplingRate, EventType, ScaleAccelerometer, EnabledChannels, Pkt
from device.structure import Settings
from resources.frm_inrat_configuration import Ui_FrmInRatConfig
from widget import WaitingDialog

from device import InRat
from resources.frm_online_device import Ui_FrmDevice

logger = logging.getLogger(__name__)

class Device(QObject):

    signal_disconnected = Signal()
    signal_acquisition = Signal()

    signal_data_accepted = Signal(object)
    signal_event_accepted = Signal(object)

    signal_show_dialog = Signal()
    signal_close_dialog = Signal()

    def __init__(self, loop: AbstractEventLoop, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # build queue
        self.ecg_queue = asyncio.Queue()

        self._loop = loop
        self._in_rat: InRat | None = None
        self._control_panel: OnlineControlPanel = OnlineControlPanel(device=self)
        self._config_panel: DeviceConfigurationPane = DeviceConfigurationPane()

        self._acquisition_queue = Queue()
        self._acquisition_event = Event()

        self._future_connection: None | Future = None
        self._future_acquisition: None | Future = None

        # signal
        self.ecg_block = EcgDataBlock()

        # waiting dialog window
        self.dlg_waiting_connection = WaitingDialog()
        self.signal_show_dialog.connect(self.dlg_waiting_connection.show)
        self.signal_close_dialog.connect(self.dlg_waiting_connection.close)

        self._control_panel.pushButtonStart.clicked.connect(self.process_start)
        self._control_panel.pushButtonStop.clicked.connect(self.process_stop)

    def set_device(self, device: BLEDevice):
        """ Открытие устройства """
        logger.debug(f"Открытие устройства: {device.name}")
        self._future_connection = asyncio.run_coroutine_threadsafe(self.process_connect(device), self._loop)

    async def process_connect(self, device: BLEDevice):
        """ Соединение и открытие устройства """
        self.signal_show_dialog.emit()

        self._in_rat = InRat(device)
        retry = 0
        while retry < 3:
            logger.debug(f"Попытка подключения {retry}")
            retry += 1
            if await self._in_rat.connect():
                break

        if self._in_rat.is_connected:
            self._control_panel.set_device(device)
        else:
            self._in_rat = None
            self.signal_disconnected.emit()

        self.signal_close_dialog.emit()

    def process_start(self):
        """ Запуск устройства на получение данных """
        settings = Settings(DataRateEcg=self.config_panel.sampling_rate.value, HighPassFilterEcg=0,
                            FullScaleAccelerometer=self.config_panel.accelerometer_scale.value, EnabledChannels=EnabledChannels.ECG,
                            EnabledEvents=EventType.START.value, ActivityThreshold=self.config_panel.activity_threshold,)

        self._future_acquisition = asyncio.run_coroutine_threadsafe(
            self._in_rat.start_acquisition(settings, self._acquisition_queue), self._loop
        )
        self._acquisition_event.set()
        future = asyncio.run_coroutine_threadsafe(self.process_acquisition(), self._loop)

        self._control_panel.pushButtonStart.setEnabled(False)
        self._control_panel.pushButtonStop.setEnabled(True)

    async def process_acquisition(self):
        """ Обработка очереди с данными. Очередь заполняется в методе start_acquisition класса InRat """

        while self._acquisition_event.is_set():

            data = await self._acquisition_queue.get()
            self._acquisition_queue.task_done()

            if data["type"] == "ecg":
                self.ecg_block.sample_rate = 500
                self.ecg_block.ecg_signal = data["data"]
                datablock = copy.copy(self.ecg_block)
                self.signal_data_accepted.emit(datablock)

    def process_stop(self):
        """ Остановка получения данных с устройства """
        self._future_acquisition.cancel()

        future = asyncio.run_coroutine_threadsafe(self._in_rat.stop_acquisition(), self._loop)
        self._acquisition_event.clear()

        self._control_panel.pushButtonStart.setEnabled(True)
        self._control_panel.pushButtonStop.setEnabled(False)
        self._future_connection = None

    @property
    def control_panel(self):
        return self._control_panel

    @property
    def config_panel(self):
        return self._config_panel

    def reset(self):
        """ Сброс соединения с подключенным устройством и уведомление об этом главного окна"""
        future = asyncio.run_coroutine_threadsafe(self._in_rat.disconnect(), self._loop)

        self._in_rat = None
        self._control_panel.reset()
        self.signal_disconnected.emit()


class OnlineControlPanel(QFrame, Ui_FrmDevice):

    def __init__(self, device: Device, *args, **kwargs):
        super().__init__(parent=None, *args, **kwargs)
        self.setupUi(self)

        self._device = device
        self.pushButtonDisconnect.clicked.connect(self._device.reset)

    def set_device(self, device: BLEDevice):
        """ Активация окна управления inRat """
        self.groupBox.setTitle(device.name)
        self.pushButtonStart.setEnabled(True)
        self.pushButtonDisconnect.setEnabled(True)

    def reset(self):
        """ Возврат окна управления в начальное состояние """
        self.groupBox.setTitle("inRat")
        self.pushButtonStart.setEnabled(False)
        self.pushButtonStop.setEnabled(False)
        self.pushButtonDisconnect.setEnabled(False)


class DeviceConfigurationPane(QFrame, Ui_FrmInRatConfig):
    signal_config_changed = Signal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)

        self._set_scale_accelerometer()
        self._set_sampling_rate()
        self._set_activity_threshold()

    @property
    def sampling_rate(self):
        return self.comboBoxSamplingRate.currentData()
    @property
    def accelerometer_scale(self):
        return self.comboBoxScaleAcc.currentData()
    @property
    def activity_threshold(self):
        return self.comboBoxActivityThreshold.currentData()

    def _set_scale_accelerometer(self):
        items = [("±2", ScaleAccelerometer.G_2), ("±4", ScaleAccelerometer.G_4),
                 ("±8", ScaleAccelerometer.G_8), ("±16", ScaleAccelerometer.G_16)]
        for item in items:
            self.comboBoxScaleAcc.addItem(*item)

    def _set_sampling_rate(self):
        items = [("500", SamplingRate.HZ_500), ("1000", SamplingRate.HZ_1000), ("2000", SamplingRate.HZ_1000)]
        for item in items:
            self.comboBoxSamplingRate.addItem(*item)

    def _set_activity_threshold(self):
        items = [(f"{i}", i) for i in range(1, 10)]
        for item in items:
            self.comboBoxActivityThreshold.addItem(*item)


class EcgDataBlock:
    def __init__(self, ecg=1):
        self.sample_counter = 0
        self.sample_rate = 500.0
        self.block_time = datetime.datetime.now()
        self.ecg_signal = np.zeros((ecg, Pkt.SamplesCountEcg))

