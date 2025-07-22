import asyncio
import logging
import contextlib

from bleak import AdvertisementData, BLEDevice, BleakScanner

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
        template: str = NAME_TEMPLATE
) -> tuple[BLEDevice, AdvertisementData] | tuple[None, None]:
    """
    Find ble device on template.
    :param timeout: int
    :param template: str
    :return: BLEDevice, AdvertisementData
    """
    async with BleakScanner() as scanner:

        with contextlib.suppress(asyncio.TimeoutError):

            async with asyncio.timeout(timeout):

                async for device, advertisement in scanner.advertisement_data():

                    if device is not None and device.name is not None and device.name.startswith(template):
                        return device, advertisement
    return None, None


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