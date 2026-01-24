import asyncio
import logging
from asyncio import AbstractEventLoop, Queue, Event
from concurrent.futures import Future

from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QFrame
from bleak import BLEDevice

from device.constants import SamplingRate, EventType, ScaleAccelerometer, EnabledChannels
from device.structure import Settings
from widget import WaitingDialog

from device import InRat
from resources.frm_online_device import Ui_FrmDevice

logger = logging.getLogger(__name__)

class Device(QObject):

    signal_disconnected = Signal()
    signal_acquisition = Signal()

    signal_data_accepted = Signal(object)
    signal_event_accepted = Signal(object)

    def __init__(self, loop: AbstractEventLoop, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._loop = loop
        self._in_rat: InRat | None = None
        self._control_panel: OnlineControlPanel = OnlineControlPanel(device=self)

        self._acquisition_queue = Queue()
        self._acquisition_event = Event()

        self._future_connection: None | Future = None
        self._future_acquisition: None | Future = None

        self._control_panel.pushButtonStart.clicked.connect(self.process_start)
        self._control_panel.pushButtonStop.clicked.connect(self.process_stop)

    def set_device(self, device: BLEDevice):
        """ Открытие устройства """
        self._future_connection = asyncio.run_coroutine_threadsafe(self.process_connect(device), self._loop)

    async def process_connect(self, device: BLEDevice):
        """ Соединение и открытие устройства """
        dlg = WaitingDialog()
        dlg.show()

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

        dlg.close()

    def process_start(self):
        """ Запуск устройства на получение данных """
        default_settings = Settings(
            DataRateEcg=SamplingRate.HZ_500.value, HighPassFilterEcg=0, FullScaleAccelerometer=ScaleAccelerometer.G_2.value,
            EnabledChannels=EnabledChannels.ECG.value, EnabledEvents=EventType.START, ActivityThreshold=1
        )

        self._future_acquisition = asyncio.run_coroutine_threadsafe(
            self._in_rat.start_acquisition(default_settings, self._acquisition_queue), self._loop
        )
        self._acquisition_event.set()
        future = asyncio.run_coroutine_threadsafe(self.process_acquisition(), self._loop)

        self._control_panel.pushButtonStart.setEnabled(False)
        self._control_panel.pushButtonStop.setEnabled(True)

    async def process_acquisition(self):
        """ Обработка очереди с данными. Очередь заполняется в методе start_acquisition класса InRat """
        while self._acquisition_event.is_set():
            print(f"Состояние: {self._future_acquisition.running()=}")
            data = await self._acquisition_queue.get()
            self._acquisition_queue.task_done()

            if data["type"] == "ecg":
                self.signal_data_accepted.emit(data["data"])

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