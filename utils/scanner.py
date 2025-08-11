import asyncio
import logging
import contextlib
from typing import Any, AsyncGenerator

from bleak import AdvertisementData, BLEDevice, BleakScanner, BleakClient


DEFAULT_TIMEOUT = 30

# NAME_TEMPLATE = "EMG-SENS"
NAME_TEMPLATE = "inRat"

logger = logging.getLogger(__name__)
logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)-15s %(name)-8s %(levelname)s: %(message)s",
    )

async def find_device(
        timeout: int | None = None,
        template: str = NAME_TEMPLATE,
        event_stop_scanning: asyncio.Event = None
) -> tuple[BLEDevice, AdvertisementData] | tuple[None, None]:
    """
    Find ble device on template.
    :param event_stop_find:
    :param timeout: int
    :param template: str
    :return: BLEDevice, AdvertisementData
    """
    async with BleakScanner() as scanner:
        with contextlib.suppress(asyncio.TimeoutError):
            async with asyncio.timeout(timeout):
                async for device, advertisement in scanner.advertisement_data():
                    # stop scanning
                    if event_stop_scanning is not None and event_stop_scanning.is_set():
                        return None, None
                    if device is not None and device.name is not None and device.name.startswith(template):
                        return device, advertisement
    return None, None


async def get_device_name(
        template: str = NAME_TEMPLATE
) -> AsyncGenerator[tuple[BLEDevice, AdvertisementData] | tuple[BLEDevice | None, AdvertisementData], Any]:
    """
    Generator, gives device names corresponding to a template
    :param template:
    :return:
    """
    async with BleakScanner() as scanner:
        with contextlib.suppress(asyncio.TimeoutError):
            async for device, advertisement in scanner.advertisement_data():
                if device is not None and device.name is not None and device.name.startswith(template):
                    yield device, advertisement
    yield device, advertisement


async def discover(
        wait: int = 3,
) -> list[tuple[BLEDevice, AdvertisementData]]:
    """
    Discover ble devices in network.
    :param wait: int
    :return: (BLEDevice, AdvertisementData)
    """
    async with BleakScanner() as scanner:
        await asyncio.sleep(wait)
        return [(d,a) for (d,a) in scanner.discovered_devices_and_advertisement_data.values()]

if __name__ == "__main__":
    # asyncio.run(find_device())
    asyncio.run(discover())