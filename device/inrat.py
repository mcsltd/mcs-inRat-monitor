import asyncio
import ctypes
import hashlib
import logging
import time

from cryptography.hazmat.primitives.ciphers import algorithms, modes, Cipher
from bleak import BleakClient, BleakCharacteristicNotFoundError

from device.constants import DeviceInformationService, Command, ScaleAccelerometer, SamplingRate, EnabledChannels, EventType
from device.decoder import decode_ecg
from device.structure import Settings, Status, Event

from config import BLE_KEY

logger = logging.getLogger(__name__)

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


class inRat:

    UUID_CHARACTERISTIC_DATA_ECG = "59573ef1-5389-575f-87d5-5f31fcdcba7b"
    UUID_CHARACTERISTIC_EVENT = "f553739f-9f1f-538d-a7d3-cd987b395eb5"
    UUID_CHARACTERISTIC_CONTROL = "7395ca15-5997-5a1b-a138-75a7a573b8e5"
    UUID_CHARACTERISTIC_STATUS = "c3571b1b-e17e-5195-9fd3-8119cb153187"

    def __init__(self, ble_device):
        self._client: BleakClient = BleakClient(ble_device)

        self._is_notifying: bool = False
        self._is_activated: bool = False
        self._name = ble_device.name
        self._model = None
        self._serial_number = None
        self._firmware = None
        self._hardware = None

    @property
    def is_connected(self) -> bool:
        return self._client.is_connected
    @property
    def is_activated(self) -> bool:
        return self._is_activated
    @property
    def address(self) -> str:
        return self._client.address
    @property
    def name(self) -> str | None:
        return self._name
    @property
    def serial_number(self) -> str | None:
        return self._serial_number
    @property
    def model(self) -> str | None:
        return self._model
    @property
    def hardware(self) -> str | None:
        return self._hardware
    @property
    def firmware(self) -> str | None:
        return self._firmware

    async def _get_device_info(self) -> (bool, str):
        """ Получение данных об устройстве """
        if not self._client.is_connected:
            logger.error(f"Потеряно соединение с {self.name}!")
            return True, f"Потеряно соединение с {self.name}!"

        try:
            sn = await self._client.read_gatt_char(str(DeviceInformationService.SERIAL))
            self._serial_number = sn.decode()
        except Exception as error:
            return False, f"Не удалось прочитать серийный номер. Ошибка: {error}"

        try:
            fw = await self._client.read_gatt_char(str(DeviceInformationService.FIRMWARE))
            self._firmware = fw.decode()
        except Exception as error:
            return False, f"Не удалось прочитать версию прошивки. Ошибка: {error}"

        try:
            hw = await self._client.read_gatt_char(str(DeviceInformationService.HARDWARE))
            self._hardware = hw.decode()
        except Exception as error:
            return False, f"Не удалось прочитать версию аппаратуры. Ошибка: {error}"

        try:
            md = await self._client.read_gatt_char(str(DeviceInformationService.MODEL))
            self._model = md.decode()
        except Exception as error:
            return False, f"Не удалось прочитать модель устройсва. Ошибка: {error}"

        logger.info(
            f"Получена информация об устройстве: {self.name}\n"
            f" - sn: {self.serial_number}\n"
            f" - model: {self.model}\n"
            f" - firmware: {self.firmware}\n"
            f" - hardware: {self.hardware}\n"
        )
        return True, "Ok!"

    async def get_status(self) -> None | Status:
        """ Получение статуса устройства и другой информации """
        raw_bytes = await self._client.read_gatt_char(self.UUID_CHARACTERISTIC_STATUS)
        status = Status.from_buffer(raw_bytes)

        logger.info(
            f"Прочитана структура Status для устройства {self.name}:\n"
            f" Activated = {status.Activated}\n"
            f" Vddio = {status.Vddio} мВ\n"
            f" Usage:\n"
            f"      PowerOnCount = {status.Usage.PowerOnCount}\n"
            f"      AdvertisingSeconds = {status.Usage.AdvertisingSeconds} c.\n"
            f"      ConnectionSeconds = {status.Usage.ConnectionSeconds} c.\n"
            f"      DataSendSeconds = {status.Usage.DataSendSeconds} c.")

        return status

    async def connect(self, wait: float=10.0) -> (bool, str):
        """ метод соединения с устройством и получения статуса и данных от устройства """
        if self.is_connected:
            logger.warning(f"Устройство {self.address} уже подключено")
            return True, "Ok"

        # соединение
        try:
            await asyncio.wait_for(self._client.connect(), wait)
            logger.info(f"Подключение к {self.name} прошло успешно")
        except TimeoutError:
            logger.error(f"Истекло время подключения к {self.name}")
            return False, f"Истекло время подключения к {self.name}"
        except Exception as error:
            return False, f"Возникла ошибка во время подключения к {self.name}. Ошибка: {error}"

        # получение информации об устройстве
        res, msg = await self._get_device_info()
        if not res:
            return False, msg

        return True, "Ok!"


    async def disconnect(self) -> (bool, str):
        """ метод отключения inRat """
        msg = None
        # передача команды закрытия соединения inRat
        try:
            await self.setup(Command.ConnectionClose)
        except Exception as err:
            msg = f"Возникла ошибка во время передачи команды ConnectionClose. Ошибка: {err}"

        # ToDo: добавить отписку от сервисов

        # отсоединение (в любом случае)
        try:
            await self._client.disconnect()
            msg = "Ok!"
        except Exception as err:
            if msg:
                msg += f"\n{err}Возникла ошибка закрытия {self.name}. Ошибка: {err}"
            else:
                msg = f"Возникла ошибка закрытия {self.name}. Ошибка: {err}"
            return False, msg

        return True, msg

    async def setup(self, cmd: Command, settings: Settings | bytes = b''):
        """ Настройка устройства """
        if not self.is_connected:
            logger.error(f"Потеряно соединение с {self.name}!")
            return False, f"Потеряно соединение с {self.name}!"

        data = cmd.value.to_bytes() + bytes(settings)
        data += get_control_sum(data=data, key=BLE_KEY)
        await self._client.write_gatt_char(char_specifier=self.UUID_CHARACTERISTIC_CONTROL, data=data)

    async def start_acquisition(self, data_queue) -> (bool, str):
        """ Запуск inRat на регистрацию сигнала и событий """

        async def event_handler(sender, data: bytearray):
            event_size = ctypes.sizeof(Event)
            cnt = int(len(data) / event_size)

            logger.debug(f"Получено событий: {cnt}")
            for idx in range(cnt):
                event = Event.from_buffer(data[idx: (idx + 1) * event_size])
                await data_queue.put({"type": "event", "counter": event.Counter, "event": event})

        async def signal_handler(sender, data: bytearray):
            # print(f"{sender=}, {data=}")
            time_received = time.time()
            cnt, sig = decode_ecg(data)
            await data_queue.put({"type": "signal", "start_time": time_received, "counter": cnt, "signal": sig})

        settings = Settings(
            DataRateEcg=SamplingRate.HZ_500, HighPassFilterEcg=0, FullScaleAccelerometer=ScaleAccelerometer.G_2,
            EnabledChannels=EnabledChannels.ECG,
            EnabledEvents=EventType.BUTTON | EventType.ACTIVITY | EventType.FREEFALL | EventType.ORIENTATION | EventType.START | EventType.TEMP,
            ActivityThreshold=1
        )
        res = True

        if not self.is_connected:
            return False, f"потеряно соединение с {self.name}!"

        try:
            await self.setup(Command.AcquisitionStart, settings)
        except:
            return False, f"Не удалось {self.name} передать команду Command.AcquisitionStart "

        try:
            await self._client.start_notify(self.UUID_CHARACTERISTIC_DATA_ECG, signal_handler)
            if not self._is_notifying:
                self._is_notifying = True
        except BleakCharacteristicNotFoundError:
            return False, f"Не удалось подписаться на сервис: {self.UUID_CHARACTERISTIC_DATA_ECG}"
        try:
            await self._client.start_notify(self.UUID_CHARACTERISTIC_EVENT, event_handler)
            if not self._is_notifying:
                self._is_notifying = True
        except BleakCharacteristicNotFoundError:
            return False, f"Не удалось подписаться на сервис: {self.UUID_CHARACTERISTIC_EVENT}"

        return res, "Ok"

    async def stop_acquisition(self) -> None:
        """ Остановка inRat на регистрацию сигнала и событий """
        await self.setup(Command.AcquisitionStop)
        try:
            await self._client.stop_notify(self.UUID_CHARACTERISTIC_DATA_ECG)
        except Exception as exc:
            logger.debug(f"Возникла ошибка описки от сервиса рассылки сигналов:\n{exc}")

        try:
            await self._client.stop_notify(self.UUID_CHARACTERISTIC_EVENT)
        except Exception as exc:
            logger.debug(f"Возникла ошибка описки от сервиса рассылки событий:\n{exc}")

