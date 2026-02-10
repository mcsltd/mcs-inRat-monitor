from dataclasses import dataclass
from enum import IntEnum, Enum, IntFlag, auto
from functools import cached_property
from uuid import UUID


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

class Command(Enum):
    AcquisitionStart = 1
    AcquisitionStop = 2
    ConnectionClose = 3
    TurnOff = 4
    Activate = 5
    Deactivate = 6

@dataclass(slots=True, frozen=True)
class Pkt:
    SamplesCountEcg = 32
    ChannelsCountEcg = 1

@dataclass(slots=True, frozen=True)
class Const:
    EcgResolution = (2.42 / 171.) / ((1 << 16) - 1)
    AccResolution = 4000.0 / ((1 << 16) - 1)

class ScaleAccelerometer(Enum):
    G_2 = 0
    G_4 = 1
    G_8 = 2
    G_16 = 3

class EventType(IntFlag):
    BUTTON = 0
    ACTIVITY = auto()
    FREEFALL = auto()
    ORIENTATION = auto()
    START = auto()
    TEMP = auto()

class SamplingRate(Enum):
    HZ_500 = 0
    HZ_1000 = 1
    HZ_2000 = 2

class EnabledChannels(IntFlag):
    ECG = 1
