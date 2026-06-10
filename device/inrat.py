import asyncio
import ctypes
import logging
from enum import IntEnum
from functools import cached_property
from uuid import UUID

from bleak import BLEDevice, BleakClient

from device.constants import Pkt
from device.decoders import decode_signal, decode_acceleration
from device.enums import EnabledChannels, SampleRateEcg, SampleRateEeg, Mode, EventType, Command, ScaleAccelerometer, \
    TypeSignal
from device.structures import Event, Settings
from device.utils import get_control_sum
from config import BLE_KEY

from device.structures import Status

# версии программного обеспечения
FIRMWARE_V0 = "1.0.260317"
FIRMWARE_V1 = "1.0.260527" # "1.0.260603"

logger = logging.getLogger(__name__)

class inRat:

    UUID_CHARACTERISTIC_CONTROL = "7395ca15-5997-5a1b-a138-75a7a573b8e5"
    UUID_CHARACTERISTIC_ECG_EEG = "59573ef1-5389-575f-87d5-5f31fcdcba7b"
    UUID_CHARACTERISTIC_EVENT = "f553739f-9f1f-538d-a7d3-cd987b395eb5"
    UUID_CHARACTERISTIC_ACC = "aae8a15e-db13-53fd-9efc-1fab1717aee5"
    UUID_CHARACTERISTIC_STATUS = "c3571b1b-e17e-5195-9fd3-8119cb153187"

    UUID_TEMPLATE = "0000{:0>4x}-0000-1000-8000-00805f9b34fb"
    class inRatCharacteristic(IntEnum):
        MANUFACTURER_NAME = 0x2A29
        MODEL = 0x2A24
        SERIAL = 0x2A25
        FIRMWARE = 0x2A26
        HARDWARE = 0x2A27

        @cached_property
        def uuid(self) -> UUID:
            """Convert the ID to a full UUID and cache."""
            return UUID(inRat.UUID_TEMPLATE.format(self.value))

        def __str__(self) -> str:
            """Convert UUID to string value."""
            return str(self.uuid)

    def __init__(self, ble_device: BLEDevice):
        self._client: BleakClient = BleakClient(ble_device)
        self._activated: bool = False

        # information
        self._name: None | str = ble_device.name
        self._manufacturer: None | str = None
        self._model: None | str = None
        self._serial: None | str = None
        self._firmware: None | str = None
        self._hardware: None | str = None

        # settings
        self._mode = Mode.ECG
        self._sample_rate = SampleRateEcg.HZ_500
        self._hpf_and_gain = 0 # todo: what is this?
        self._full_scale_accelerometer = ScaleAccelerometer.G_2
        self._enabled_events = EventType.NONE
        self._activity_threshold = 2
        self._enabled_channels = EnabledChannels.ECG

    @property
    def mode(self):
        if self._mode is Mode.ECG:
            return TypeSignal.ECG
        if self._mode is Mode.EEG:
            return TypeSignal.EEG
        return None
    @mode.setter
    def mode(self, value: TypeSignal):
        if value is TypeSignal.ECG:
            self._mode = Mode.ECG
        if value is TypeSignal.EEG:
            self._mode = Mode.EEG

    @property
    def sample_rate(self):
        if self._sample_rate is SampleRateEcg.HZ_500:
            return 500
        if self._sample_rate is SampleRateEcg.HZ_1000:
            return 1000
        if self._sample_rate is SampleRateEcg.HZ_2000:
            return 2000
        if self._sample_rate is SampleRateEeg.HZ_250:
            return 250
        if self._sample_rate is SampleRateEeg.HZ_500:
            return 500
        return None
    @sample_rate.setter
    def sample_rate(self, value: float | int) -> None:
        if self._mode is Mode.ECG:
            if value == 500:
                self._sample_rate = SampleRateEcg.HZ_500
            elif value == 1000:
                self._sample_rate = SampleRateEcg.HZ_1000
            elif value == 2000:
                self._sample_rate = SampleRateEcg.HZ_2000
            else:
                raise ValueError(f"В режиме съема ЭКГ не поддерживается частота {value}")

        if self._mode is Mode.EEG:
            if value == 250:
                self._sample_rate = SampleRateEeg.HZ_250
            elif value == 500:
                self._sample_rate = SampleRateEeg.HZ_250
            else:
                raise ValueError(f"В режиме съема ЭЭГ не поддерживается частота {value}")
    @property
    def enabled_events(self) -> EventType:
        return self._enabled_events
    @enabled_events.setter
    def enabled_events(self, events: EventType | int) -> None:
        self._enabled_events = EventType(events)
    @property
    def full_scale_accelerometer(self) -> int | None:
        if self._full_scale_accelerometer == ScaleAccelerometer.G_2:
            return 2
        elif self._full_scale_accelerometer == ScaleAccelerometer.G_4:
            return 4
        elif self._full_scale_accelerometer == ScaleAccelerometer.G_8:
            return 8
        elif self._full_scale_accelerometer == ScaleAccelerometer.G_16:
            return 16
        raise ValueError("Масштаб акселерометра не установлен!")
    @full_scale_accelerometer.setter
    def full_scale_accelerometer(self, value: int):
        if value == 2:
            self._full_scale_accelerometer = ScaleAccelerometer.G_2
            return
        elif value == 4:
            self._full_scale_accelerometer = ScaleAccelerometer.G_4
            return
        elif value == 8:
            self._full_scale_accelerometer = ScaleAccelerometer.G_8
            return
        elif value == 16:
            self._full_scale_accelerometer = ScaleAccelerometer.G_16
            return
        raise ValueError("Не поддерживается масштаб акселерометра")
    @property
    def activity_threshold(self) -> int:
        return self._activity_threshold
    @activity_threshold.setter
    def activity_threshold(self, value: int) -> None:
        if 0 <= value <= 10:
            self._activity_threshold = value
            return
        raise ValueError(f"Порог активности: {self._activity_threshold} не поддерживается")
    @property
    def enabled_channels(self):
        return self._enabled_channels
    @enabled_channels.setter
    def enabled_channels(self, value: EnabledChannels | int):
        self._enabled_channels = value

    @property
    def name(self) -> str | None:
        return self._name
    @property
    def manufacturer(self) -> str | None:
        return self._manufacturer
    @property
    def model(self) -> str | None:
        return self._model
    @property
    def serial(self) -> str | None:
        return self._serial
    @property
    def hardware(self) -> str | None:
        return self._hardware
    @property
    def firmware(self) -> str | None:
        return self._firmware

    @property
    def is_connected(self) -> bool:
        return self._client.is_connected
    @property
    def is_activated(self) -> bool:
        return self._activated

    async def _get_device_info(self) -> None:
        """ чтение свойств подключенного устройства """
        self._serial = await self._read_info(self.inRatCharacteristic.SERIAL)
        self._model = await self._read_info(self.inRatCharacteristic.MODEL)
        self._manufacturer = await self._read_info(self.inRatCharacteristic.MANUFACTURER_NAME)
        self._firmware = await self._read_info(self.inRatCharacteristic.FIRMWARE)
        self._hardware = await self._read_info(self.inRatCharacteristic.HARDWARE)
        # logger.info(f"{self._name}; manufacturer: {self._manufacturer}; serial: {self._serial}; model: {self._model}; firmware: {self._firmware}; hardware: {self._firmware};")

    async def _read_info(self, characteristic: inRatCharacteristic) -> str:
        """ чтение свойств устройства"""
        rawdata = await self._client.read_gatt_char(str(characteristic))
        data = rawdata.decode()
        return data

    async def _get_device_status(self):
        """ получение состояния устройства """
        rawdata = await self._client.read_gatt_char(self.UUID_CHARACTERISTIC_STATUS)
        status = Status.from_buffer(rawdata)
        self._activated = status.Activated

    def _get_settings(self) -> Settings:
        settings = Settings(
            DataRateEcgEeg=self._sample_rate,
            HPFandGain=self._hpf_and_gain,
            FullScaleAccelerometer=self._full_scale_accelerometer,
            EnabledChannels=self._enabled_channels,
            EnabledEvents=self._enabled_events,
            ActivityThreshold=self._activity_threshold
        )
        return settings

    async def setup(self, cmd, settings: Settings | bytes = b''):
        """ передача команд на inRat """
        data = cmd.to_bytes() + bytes(settings)
        data += get_control_sum(data, BLE_KEY)
        await self._client.write_gatt_char(self.UUID_CHARACTERISTIC_CONTROL, data)

    async def connect(self, wait: float = 10.0):
        """ открытие устройства """
        if self.is_connected:
            logger.warning(f"{self.name} уже открыто!")
            return
        try:
            await asyncio.wait_for(self._client.connect(), timeout=wait)
            await self._get_device_info()
            # set_default_setting_from_firmware(self)
            await self._get_device_status()
            logger.info(f"{self.name}: открыто соединение")
        except Exception as err:
            logger.error(f"{self.name}: во время соединения возникла ошибка - {err}")
            await self.disconnect()

    async def activate(self, state: bool):
        """ изменение активации устройства"""
        try:
            if state:
                await self.setup(cmd=Command.Activate)
                logger.debug(f"{self.name}: передана команда Activate ")
            else:
                await self.setup(cmd=Command.Deactivate)
                logger.debug(f"{self.name}: передана команда Deactivate ")
        except Exception as err:
            logger.error(f"{self.name}: ошибка передачи команды Activate/Deactivate - {err}")


    async def start_acquisition(
            self,
            # event_queue: asyncio.Queue| None = None,
            signal_event_queue: asyncio.Queue| None = None,
            acceleration_queue: asyncio.Queue| None = None
    ):
        """ запуск на получение данных """
        async def event_handler(sender, data: bytearray):
            event_size = ctypes.sizeof(Event)
            cnt = int(len(data) / event_size)
            for idx in range(cnt):
                event = Event.from_buffer(data[idx * event_size: (idx + 1) * event_size])
                await signal_event_queue.put({
                    "sample": int(event.Counter / Pkt.SamplesCountEcg),
                    "counter": event.Counter, "signal": event, "type": "ev"})

        async def signal_handler(sender, data):
            smpl, signal = decode_signal(data)
            await signal_event_queue.put({"sample":smpl, "signal":signal, "type": "sig"}) # "counter" -> "samples"

        async def acceleration_handler(sender, data):
            smpl, accel = decode_acceleration(data, self._enabled_channels)
            await acceleration_queue.put({"sample":smpl, "signal":accel, "type": "acc"})  # "counter" -> "samples"

        settings = self._get_settings()
        try:
            await self.setup(Command.AcquisitionStart, settings)
        except Exception as err:
            logger.error(f"{self.name}: ошибка передачи команды AcquisitionStart - {err}")

        if signal_event_queue:
            await self._client.start_notify(self.UUID_CHARACTERISTIC_ECG_EEG, signal_handler)
            await self._client.start_notify(self.UUID_CHARACTERISTIC_EVENT, event_handler)
            logger.info(f"{self.name}: подписка на сервисы UUID_CHARACTERISTIC_ECG_EEG, UUID_CHARACTERISTIC_EVENT")


        if acceleration_queue and self._firmware == FIRMWARE_V1:
            await self._client.start_notify(self.UUID_CHARACTERISTIC_ACC, acceleration_handler)
            logger.info(f"{self.name}: подписка на сервисы UUID_CHARACTERISTIC_ACC")


    async def stop_acquisition(self):
        """ остановка получения данных """
        try:
            await self.setup(Command.AcquisitionStop)
            logger.info(f"{self.name}: остановлено (сmd: stop)")
        except Exception as exc:
            ...

        try:
            await self._client.stop_notify(self.UUID_CHARACTERISTIC_ECG_EEG)
            logger.info(f"{self.name}: отписка от сервиса UUID_CHARACTERISTIC_ECG_EEG")
        except Exception as exc:
            ...

        try:
            await self._client.stop_notify(self.UUID_CHARACTERISTIC_ACC)
            logger.info(f"{self.name}: отписка от сервиса UUID_CHARACTERISTIC_ECG_EEG")
        except Exception as exc:
            ...

        try:
            await self._client.stop_notify(self.UUID_CHARACTERISTIC_EVENT)
            logger.info(f"{self.name}: отписка от сервиса UUID_CHARACTERISTIC_EVENT")
        except Exception as exc:
            ...

    async def disconnect(self):
        """ закрытие соединения с устройством """
        try:
            await self.stop_acquisition()
        except Exception as exc:
            ...

        try:
            await self.setup(Command.ConnectionClose)
            logger.info(f"{self.name}: закрыто (cmd: close)")
        except Exception as exc:
            ...

        try:
            await self._client.disconnect()
            logger.info(f"{self.name}: закрыть (bleak: disconnect)")
        except Exception as exc:
            ...
