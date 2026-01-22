import logging
from asyncio import AbstractEventLoop

from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QFrame
from bleak import BleakClient, BLEDevice

from device import InRat
from resources.frm_online_device import Ui_FrmDevice

logger = logging.getLogger(__name__)

class Device(QObject):

    signal_disconnected = Signal()
    signal_acquisition = Signal()

    def __init__(self, loop: AbstractEventLoop, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._loop = loop
        self._inrat: InRat | None = None
        self._control_panel: OnlineControlPanel = OnlineControlPanel(device=self)

    def set_device(self, device: BLEDevice):
        """ Открытие устройства """
        self._inrat = BleakClient(device)
        self._control_panel.set_device(device)

    @property
    def control_panel(self):
        return self._control_panel

    def reset(self):
        """ Сброс соединения с подключенным устройством и уведомление об этом главного окна"""
        self.signal_disconnected.emit()
        # ToDo: disconnect inrat and stop notifying
        self._inrat = None
        self._control_panel.reset()


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