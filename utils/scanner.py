import asyncio
import logging
import contextlib

from bleak import AdvertisementData, BLEDevice, BleakScanner

DEFAULT_TIMEOUT = 30

logger = logging.getLogger(__name__)
logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)-15s %(name)-8s %(levelname)s: %(message)s",
    )

async def find_device(
        timeout: int | None = None,
        event_stop: asyncio.Event | None = None,
) -> tuple[BLEDevice, AdvertisementData] | tuple[None, None]:
    async with BleakScanner() as scanner:
        with contextlib.suppress(asyncio.TimeoutError):
            async with asyncio.timeout(timeout):
                async for device, advertisement in scanner.advertisement_data():

                    # if event_stop.is_set():
                    #     break

                    if device is not None and device.name is not None and device.name.startswith("EMG-SENS"):
                        return device, advertisement
    return None, None

asyncio.run(find_device())