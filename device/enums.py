from enum import IntEnum, IntFlag, auto

class Mode(IntEnum):
    ECG = 0
    EEG = 1

class Command(IntEnum):
    AcquisitionStart = 1
    AcquisitionStop = 2
    ConnectionClose = 3
    TurnOff = 4
    Activate = 5
    Deactivate = 6

class ScaleAccelerometer(IntEnum):
    G_2 = 0
    G_4 = 1
    G_8 = 2
    G_16 = 3

class SampleRateEcg(IntEnum):
    HZ_500 = 0
    HZ_1000 = 1
    HZ_2000 = 2

class SampleRateEeg(IntEnum):
    HZ_250 = 3
    HZ_500 = 4

class EnabledChannels(IntFlag):
    NONE = 0
    ECG = auto()
    ACC_X = auto()
    ACC_Y = auto()
    ACC_Z = auto()

class EventType(IntFlag):
    NONE = 0
    BUTTON = auto()
    ACTIVITY = auto()
    FREEFALL = auto()
    ORIENTATION = auto()
    START = auto()
    TEMP = auto()
    ALL = BUTTON | ACTIVITY | FREEFALL | ORIENTATION | START | TEMP