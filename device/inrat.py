import asyncio
import ctypes
import hashlib
import logging

from cryptography.hazmat.primitives.ciphers import algorithms, modes, Cipher
from bleak import BleakClient, BleakScanner

from device.constants import DeviceInformationService, Command, ScaleAccelerometer, SamplingRate, EnabledChannels, EventType
from device.decoder import Decoder
from device.structure import Settings, Status, Event

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

BLE_KEY = bytearray([0x9F, 0xD7, 0x01, 0x17, 0x73, 0x5D, 0x75, 0x8C, 0x19, 0x59, 0x7C, 0x7E, 0x9D, 0x1E, 0x57, 0x3E])

class InRat:

    UUID_CHARACTERISTIC_DATA_ECG = "59573ef1-5389-575f-87d5-5f31fcdcba7b"
    UUID_CHARACTERISTIC_EVENT = "f553739f-9f1f-538d-a7d3-cd987b395eb5"
    UUID_CHARACTERISTIC_CONTROL = "7395ca15-5997-5a1b-a138-75a7a573b8e5"
    UUID_CHARACTERISTIC_STATUS = "c3571b1b-e17e-5195-9fd3-8119cb153187"

    def __init__(self, ble_device):
        self._client: BleakClient = BleakClient(ble_device)

        self._name = ble_device.name
        self._model = None
        self._serial_number = None
        self._firmware = None
        self._hardware = None

    @property
    def is_connected(self) -> bool:
        return self._client.is_connected
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

    async def _get_device_info(self) -> None:
        """ Получение данных об устройстве """
        sn = await self._client.read_gatt_char(str(DeviceInformationService.SERIAL))
        self._serial_number = sn.decode()
        fw = await self._client.read_gatt_char(str(DeviceInformationService.FIRMWARE))
        self._firmware = fw.decode()
        hw = await self._client.read_gatt_char(str(DeviceInformationService.HARDWARE))
        self._hardware = hw.decode()
        md = await self._client.read_gatt_char(str(DeviceInformationService.MODEL))
        self._model = md.decode()
        logger.info(
            f"Получена информация об устройстве: {self.name}\n"
            f" - sn: {self.serial_number}\n"
            f" - model: {self.model}\n"
            f" - firmware: {self.firmware}\n"
            f" - hardware: {self.hardware}\n"
        )

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

    async def connect(self, timeout: int=10) -> bool:
        """ Попытка соединения с обнаруженным устройством """
        res = True
        if self.is_connected:
            logger.warning(f"Устройство {self.address} уже подключено")
            return res

        try:
            await asyncio.wait_for(self._client.connect(), timeout)
            await self._get_device_info()
            logger.info(f"Устройство {self.name} подключено")
        except asyncio.TimeoutError:
            res = False
            logger.info(f"Устройство {self.name} не было найдено")

        except Exception as exp:
            res = False

        return res

    async def disconnect(self) -> bool:
        """ Отсоединение от устройства """
        res = True
        if not self.is_connected:
            return res

        try:
            logger.info(f"Устройство {self.name} отключено")
            await self._client.disconnect()
            res = True
        except Exception:
            res = False
        return res

    async def setup(self, cmd: Command, settings: Settings | bytes = b''):
        """ Настройка устройства """
        data = cmd.value.to_bytes() + bytes(settings)
        data += get_control_sum(data=data, key=BLE_KEY)

        await self._client.write_gatt_char(char_specifier=InRat.UUID_CHARACTERISTIC_CONTROL, data=data)

    async def start_acquisition(self, settings: Settings):
        """ Запуск устройства на получение данных """
        async def event_handler(_, raw_data: bytearray):
            cnt = int(len(raw_data) / ctypes.sizeof(Event))
            logger.debug(f"Получено событий: {cnt}")
            for idx in range(cnt):
                event = Event.from_buffer(raw_data)
                logger.debug("Получено событие:\n"
                    f" {event.Type=}\n"
                    f" {event.Value=}\n"
                    f" Acceleration:\n"
                    f"      {event.Acceleration.X=} {event.Acceleration.Y=} {event.Acceleration.Z=}\n"
                    f" {event.Number=}\n"
                    f" {event.Counter=}\n"
                    f" {event.Data=}"
                )
            await asyncio.sleep(0.001)

        async def ecg_handler(_, raw_data: bytearray):
            counter, signal = decoder.decode_ecg(raw_data)
            logger.debug(f"Получен сигнал ЭКГ: {counter}; значение сигнала: {signal}")
            await asyncio.sleep(0.001)

        decoder = Decoder()
        await self.setup(cmd=Command.AcquisitionStart, settings=settings)
        await self._client.start_notify(self.UUID_CHARACTERISTIC_DATA_ECG, ecg_handler)
        await self._client.start_notify(self.UUID_CHARACTERISTIC_EVENT, event_handler)
        logger.debug(f"{self.name} запущено для получения событий и записи ЭКГ!")


    async def stop_acquisition(self):
        await self.setup(cmd=Command.AcquisitionStop)
        await self._client.stop_notify(self.UUID_CHARACTERISTIC_DATA_ECG)
        await self._client.stop_notify(self.UUID_CHARACTERISTIC_EVENT)
        logger.debug(f"{self.name} остановлено!")

async def main():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)-15s %(name)-8s %(levelname)s: %(message)s",
    )

    device = await BleakScanner.find_device_by_name(name="inRat-1-1021")
    print(f"{device=}")

    if device is not None:
        inrat = InRat(ble_device=device)

        await inrat.connect()
        print(f"Состояние соединения с InRat: {inrat.is_connected}")
        await asyncio.sleep(15)

        settings = Settings(
            DataRateEcg=SamplingRate.HZ_500.value,
            HighPassFilterEcg=0,
            FullScaleAccelerometer=ScaleAccelerometer.G_2.value,
            EnabledChannels=EnabledChannels.ECG,
            EnabledEvents=EventType.BUTTON | EventType.ACTIVITY | EventType.FREEFALL | EventType.ORIENTATION | EventType.START | EventType.TEMP,
            ActivityThreshold=1
        )

        await inrat.start_acquisition(settings=settings)
        await asyncio.sleep(30)
        await inrat.stop_acquisition()

        await inrat.disconnect()
    else:
        print("Устройство не найдено")

if __name__ == "__main__":
    asyncio.run(main())
