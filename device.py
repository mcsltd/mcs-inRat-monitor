import asyncio
import ctypes
import logging
import hashlib

from typing import Optional
from bleak import BleakClient

from cryptography.hazmat.primitives.ciphers import algorithms, modes, Cipher


from config import BLE_KEY
from constants import Command, DataRateEcg, FullScaleAccelerometer, EnabledChannels, \
    EventType, Const, DeviceInformationService
from decoder import decode_ecg, decode_event
from structure import Settings, Event, Status, StatusData


def get_control_sum(data: bytes, key: bytearray) -> bytes:
    hash = hashlib.sha256(data).digest()
    iv = bytes(128 // 8)
    # create encoder
    cipher = Cipher(
        algorithm=algorithms.AES(key), mode=modes.CBC(iv)
    )
    encryptor = cipher.encryptor()
    # encrypt
    sign = encryptor.update(hash) + encryptor.finalize()
    return sign

logger = logging.getLogger(__name__)

class RatSens(BleakClient):

    UUID_CHARACTERISTIC_DEVICE_NAME = "00002a00-0000-1000-8000-00805f9b34fb"
    UUID_CHARACTERISTIC_DATA_ECG = "59573ef1-5389-575f-87d5-5f31fcdcba7b"
    UUID_CHARACTERISTIC_EVENT = "f553739f-9f1f-538d-a7d3-cd987b395eb5"
    UUID_CHARACTERISTIC_CONTROL = "7395ca15-5997-5a1b-a138-75a7a573b8e5"
    UUID_CHARACTERISTIC_STATUS = "c3571b1b-e17e-5195-9fd3-8119cb153187"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.name = args[0].name
        self.is_running = False
        self._is_activated = False

        # set lock
        self._connect_lock = asyncio.Lock()
        self._operation_lock = asyncio.Lock()

    @property
    def is_activated(self):
        return self._is_activated

    def _check_operation_lock(self) -> None:
        """ Check and print message if lock occupied. """
        if self._operation_lock.locked():
            logger.debug("Operation already in progress... Waiting for it to complete.")

    async def setup(self, cmd: Command, settings: Optional[Settings] = None):
        logger.debug("Set settings to the BLE device.")
        self._check_operation_lock()

        async with self._operation_lock:
            if settings is None:
                settings = b''
            data = cmd.value.to_bytes() + bytes(settings)
            data += get_control_sum(data=data, key=BLE_KEY)
            await self.write_gatt_char(char_specifier=RatSens.UUID_CHARACTERISTIC_CONTROL, data=data)

    async def get_device_information(self):
        logger.debug("Get device information.")
        self._check_operation_lock()

        async with self._operation_lock:
            info = dict.fromkeys(["name", "model", "serial", "status", "firmware", "hardware"])
            info = {"name": None, "model": None, "serial": None, "status": "Connected"}
            name = await self.read_gatt_char(RatSens.UUID_CHARACTERISTIC_DEVICE_NAME)
            info["name"] = name.decode()
            model = await self.read_gatt_char(str(DeviceInformationService.MODEL))
            info["model"] = model.decode()
            sn = await self.read_gatt_char(str(DeviceInformationService.SERIAL))
            info["serial"] = sn.decode()
            firmware = await self.read_gatt_char(str(DeviceInformationService.FIRMWARE))
            info["firmware"] = firmware.decode()
            hardware = await self.read_gatt_char(str(DeviceInformationService.HARDWARE))
            info["hardware"] = hardware.decode()

            return info

    async def start_acquisition(
            self,
            ecg_queue: asyncio.Queue,
            event_queue: asyncio.Queue
    ) -> bool:
        """ запуск устройства на получение сигнала и событий"""
        async def ecg_handler(_, raw_data: bytearray):
            counter, ecg = decode_ecg(raw_data)
            ecg *= 1e6  # in μV

            if ecg_queue is not None:
                logger.debug("Put ecg in queue.")
                await ecg_queue.put({"counter": counter, "ecg": ecg})

        async def event_handler(_, raw_data: bytearray):
            event = decode_event(raw_data)
            await event_queue.put(event)

        if not self.is_connected:
            return False

        try:
            await self.setup(
                cmd=Command.AcquisitionStart,
                settings=Settings(
                    DataRateEcg=DataRateEcg.HZ_500.value, HighPassFilterEcg=0,
                    FullScaleAccelerometer=FullScaleAccelerometer.G_0.value,
                    EnabledChannels=EnabledChannels.ENABLED_ECG.value,
                    EnabledEvents=EventType.START,
                    ActivityThreshold=2
                )
            )
            self.is_running = True
        except Exception as err:
            logger.debug(f"Возникла ошибка при запуске на регистрацию ЭКГ и событий: {err}")
            return False

        await self.start_notify(RatSens.UUID_CHARACTERISTIC_DATA_ECG, ecg_handler)
        await self.start_notify(RatSens.UUID_CHARACTERISTIC_EVENT, event_handler)
        return True

    async def get_status(self) -> None | StatusData:
        """ Получение данных из структуры Status """
        if not self.is_connected:
            return None
        byte_status = await self.read_gatt_char(self.UUID_CHARACTERISTIC_STATUS)
        status = Status.from_buffer(byte_status)
        self._is_activated = (status.Activated == 1)
        status = status.to_dataclass()
        return status

    async def activate(self):
        """ активация устройства """
        await self.setup(cmd=Command.Activate)

    async def deactivate(self):
        """ деактивация устройства """
        await self.setup(cmd=Command.Deactivate)

    async def stop(self):
        logger.debug("Set settings to the BLE device.")
        self.is_running = False
        await self.stop_notify(RatSens.UUID_CHARACTERISTIC_DATA_ECG) # need stop notify
        await self.setup(cmd=Command.AcquisitionStop)

    async def close(self):
        logger.debug("Close connection to the BLE device")
        self.is_running = False
        await self.setup(cmd=Command.ConnectionClose)
        await self.disconnect()

    async def turn_off(self, time=1):
        logger.debug("Turn off device")
        self._check_operation_lock()

        self.is_running = False

        if self.is_running:
            await self.stop()

        async with self._operation_lock:
            data = Command.TurnOff.value.to_bytes() + bytes(time)
            data += get_control_sum(data=data, key=BLE_KEY)
            await self.write_gatt_char(char_specifier=RatSens.UUID_CHARACTERISTIC_CONTROL, data=data)

        try:
            await self.disconnect()
        except Exception:
            ...



if __name__ == "__main__":
    asyncio.run(main())
