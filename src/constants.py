from dataclasses import dataclass
from enum import Enum, IntEnum
from functools import cached_property
from uuid import UUID


@dataclass(slots=True, frozen=True)
class Pkt:
    SamplesCountECG = 32
    ChannelsCountECG = 1

@dataclass(slots=True, frozen=True)
class Const:
    EcgResolution = (2.42 / 171.) / ((1 << 16) - 1)
    AccResolution = 4000.0 / ((1 << 16) - 1)


class Command(Enum):
    AcquisitionStart = 1
    AcquisitionStop = 2
    ConnectionClose = 3
    TurnOff = 4
    Activate = 5
    Deactivate = 6


class EventType(Enum):
    ButtonPress = 0
    Activity = 1
    Freefall = 2
    Orientation = 3
    Start = 4
    Charge = 5

UUID_TEMPLATE = "0000{:0>4x}-0000-1000-8000-00805f9b34fb"


class DeviceInformationService(IntEnum):
    MANUFACTURER_NAME = 0x2A29
    MODEL = 0x2A24
    SERIAL = 0x2A25
    FIRMWARE = 0x2A26
    HARDWARE = 0x2A27

    @cached_property
    def uuid(self) -> UUID:
        """Convert the ID to a full UUID and cache."""
        return UUID(UUID_TEMPLATE.format(self.value))

    def __str__(self) -> str:
        """Convert UUID to string value."""
        return str(self.uuid)

class DataRateEcg(Enum):
    HZ_500 = 0
    HZ_1000 = 1
    HZ_2000 = 2

class HighPassFilterEcg(Enum):
    HZ_500 = 0
    HZ_1000 = 1
    HZ_2000 = 2

class FullScaleAccelerometer(Enum):
    G_0 = 0
    G_1 = 1
    G_2 = 2
    G_3 = 3

class EnabledChannels(Enum):
    ENABLED_ECG = 1
    DISABLED_ECG = 0