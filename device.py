import asyncio
import ctypes
import logging
import struct
from typing import Optional

import numpy as np
from bleak import BleakClient

from config import BLE_KEY
from constants import Command, DataRateEcg, FullScaleAccelerometer, EnabledChannels, \
    EventType, Const, Pkt, DeviceInformationService
from structure import Settings, Event
from utils.crypt import get_control_sum

logger = logging.getLogger(__name__)

class RatSens(BleakClient):

    UUID_CHARACTERISTIC_DEVICE_NAME = "00002a00-0000-1000-8000-00805f9b34fb"
    UUID_CHARACTERISTIC_DATA_ECG = "59573ef1-5389-575f-87d5-5f31fcdcba7b"
    UUID_CHARACTERISTIC_EVENT = "f553739f-9f1f-538d-a7d3-cd987b395eb5"
    UUID_CHARACTERISTIC_CONTROL = "7395ca15-5997-5a1b-a138-75a7a573b8e5"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.is_running = False

        # set lock
        self._connect_lock = asyncio.Lock()
        self._operation_lock = asyncio.Lock()

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

            info = {"name": None, "model": None, "serial": None, "status": "Connected"}
            name = await self.read_gatt_char(RatSens.UUID_CHARACTERISTIC_DEVICE_NAME)
            info["name"] = name.decode()
            model = await self.read_gatt_char(str(DeviceInformationService.MODEL))
            info["model"] = model.decode()
            sn = await self.read_gatt_char(str(DeviceInformationService.SERIAL))
            info["serial"] = sn.decode()

            return info

    async def get_ecg(self, ecg_queue: Optional[asyncio.Queue] = None):
        async def ecg_handler(_, raw_data: bytearray):
            nonlocal prev
            # logger.debug(f"get raw data: {raw_data}")

            offset = 2
            counter = struct.unpack('H', raw_data[:offset])[0]

            code = raw_data[offset]
            offset += 4

            ecg = np.zeros(Pkt.SamplesCountECG, dtype=np.float64)
            for i in range(Pkt.SamplesCountECG):

                if (code >> i) & 0x1 == 0x0:
                    ecg[i] = prev + int.from_bytes([raw_data[offset]], byteorder='little', signed=True)
                    offset += 1

                if (code >> i) & 0x1 == 0x1:
                    ecg[i] = int.from_bytes(raw_data[offset:offset + 2], byteorder='little', signed=True)
                    offset += 2

                prev = ecg[i]

            ecg *= 2.42 * 1e6 / 171 / 0xFFFF # in μV
            # ecg *= Const.EcgResolution

            # logger.debug(f"counter: {counter}; ecg: {ecg.tolist()}")
            if ecg_queue is not None:
                logger.debug("Put ecg in queue.")
                await ecg_queue.put({"counter": counter, "ecg": ecg})

        prev = 0
        await self.setup(
            cmd=Command.AcquisitionStart,
            settings=Settings(
                DataRateEcg=DataRateEcg.HZ_500.value,
                HighPassFilterEcg=0,
                FullScaleAccelerometer=FullScaleAccelerometer.G_0.value,
                EnabledChannels=EnabledChannels.ENABLED_ECG.value,
                EnabledEvents=0,
                ActivityThreshold=2
            )
        )
        self.is_running = True
        await self.start_notify(RatSens.UUID_CHARACTERISTIC_DATA_ECG, ecg_handler)


    async def get_event(self, event_queue: Optional[asyncio.Queue] = None):
        async def event_handler(_, raw_event):
            cnt = len(raw_event) // ctypes.sizeof(Event)

            idx_last = 0
            idx_next = idx_delta = ctypes.sizeof(Event)
            for i in range(cnt):
                ev: Event = Event.from_buffer(raw_event[idx_last:idx_next])

                ax = ev.Acceleration.X * Const.AccResolution
                ay = ev.Acceleration.Y * Const.AccResolution
                az = ev.Acceleration.Z * Const.AccResolution

                idx_last += idx_delta
                idx_next += idx_delta

                dict_ev = {
                    "Type": None, "Value": None, "Acceleration": None, "Number": None, "Counter": None, "Data": None
                }

                if ev.Type == EventType.ButtonPress.value:
                    dict_ev["Type"] = "ButtonPress"
                if ev.Type == EventType.Activity.value:
                    dict_ev["Type"] = "Activity"
                if ev.Type == EventType.Start.value:
                    dict_ev["Type"] = "Start"
                if ev.Type == EventType.Charge.value:
                    dict_ev["Type"] = "Charge"
                if ev.Type == EventType.Orientation.value:
                    dict_ev["Type"] = "Orientation"
                if ev.Type == EventType.Freefall.value:
                    dict_ev["Type"] = "Freefall"

                dict_ev["Acceleration"] = [ax, ay, az]
                dict_ev["Number"] = ev.Number
                dict_ev["Counter"] = ev.Counter
                dict_ev["Data"] = ev.Data
                dict_ev["Value"] = ev.Data

                if event_queue is not None:
                    await event_queue.put(dict_ev)

        await self.setup(
            cmd=Command.AcquisitionStart,
            settings=Settings(
                DataRateEcg=DataRateEcg.HZ_500.value,
                HighPassFilterEcg=0,
                FullScaleAccelerometer=FullScaleAccelerometer.G_0.value,
                EnabledChannels=EnabledChannels.DISABLED_ECG.value,
                EnabledEvents=63,
                ActivityThreshold=2
            )
        )
        await self.start_notify(RatSens.UUID_CHARACTERISTIC_EVENT, event_handler)

    async def stop(self):
        logger.debug("Set settings to the BLE device.")
        self.is_running = False
        await self.stop_notify(RatSens.UUID_CHARACTERISTIC_DATA_ECG) # need stop notify
        await self.setup(cmd=Command.AcquisitionStop)

    async def close(self):
        logger.debug("Close connection to the BLE device")
        await self.setup(cmd=Command.ConnectionClose)
        await self.disconnect()



async def main():
    from utils.scanner import find_device

    device, adv = await find_device()

    client = RatSens(device)
    await client.connect()

    # await client.get_event()
    await client.get_ecg()

    await asyncio.sleep(10)
    await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
