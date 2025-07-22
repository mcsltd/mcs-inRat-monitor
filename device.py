import asyncio
import ctypes
import logging
import struct

import numpy as np
from bleak import BleakClient

from config import BLE_KEY
from constants import Command, DeviceInformationService, DataRateEcg, FullScaleAccelerometer, EnabledChannels, \
    EventType, Const, Pkt
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

    async def setup(self, cmd: Command, settings):
        data = cmd.value.to_bytes() + bytes(settings)
        data += get_control_sum(data=data, key=BLE_KEY)
        await self.write_gatt_char(char_specifier=RatSens.UUID_CHARACTERISTIC_CONTROL, data=data)

    async def get_device_name(self):
        name = await self.read_gatt_char(RatSens.UUID_CHARACTERISTIC_DEVICE_NAME)
        return name

    async def get_ecg(self):
        async def ecg_handler(_, raw_data: bytearray):
            nonlocal prev

            offset = 2
            counter = struct.unpack('H', raw_data[:offset])[0]
            code = raw_data[offset]

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
        await self.start_notify(RatSens.UUID_CHARACTERISTIC_DATA_ECG, ecg_handler)

    async def get_event(self):
        def event_handler(_, raw_event):
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
                print(dict_ev)

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


async def main():
    from utils.scanner import find_device

    device, adv = await find_device()

    client = RatSens(device)
    await client.connect()

    # await client.get_event()
    # await client.get_ecg()

    await asyncio.sleep(10)
    await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
