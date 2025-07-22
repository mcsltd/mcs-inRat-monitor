from dataclasses import dataclass
from enum import Enum


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


# ToDo: lower case
class EventType(Enum):
    BUTTON = 0
    ACTIVITY = 1
    FREEFALL = 2
    ORIENTATION = 3
    START = 4
    CHARGE = 5


