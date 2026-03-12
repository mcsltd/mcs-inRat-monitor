import ctypes
from dataclasses import dataclass

from device.constants import EventType


class Settings(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("DataRateEcg", ctypes.c_uint8),
        ("HighPassFilterEcg", ctypes.c_uint8),
        ("FullScaleAccelerometer", ctypes.c_uint8),
        ("EnabledChannels", ctypes.c_uint8),
        ("EnabledEvents", ctypes.c_uint16),
        ("ActivityThreshold", ctypes.c_uint16),
    ]

class Usage(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("PowerOnCount", ctypes.c_uint32),
        ("AdvertisingSeconds", ctypes.c_uint32),
        ("ConnectionSeconds", ctypes.c_uint32),
        ("DataSendSeconds", ctypes.c_uint32),
    ]

class Status(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("Activated", ctypes.c_uint16),
        ("Vddio", ctypes.c_uint16),
        ("Usage", Usage)
    ]


@dataclass
class AccelerationData:
    x: int
    y: int
    z: int

class Acceleration(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("X", ctypes.c_int16),
        ("Y", ctypes.c_int16),
        ("Z", ctypes.c_int16)
    ]
    def to_dataclass(self) -> AccelerationData:
        return AccelerationData(x=self.X, y=self.Y, z=self.Z)

@dataclass
class EventData:
    type: str
    value: int
    acceleration: AccelerationData
    number: int
    counter: int
    data: int


class Event(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("Type", ctypes.c_uint8),
        ("Value", ctypes.c_uint8),
        ("Acceleration", Acceleration),
        ("Number", ctypes.c_uint32),
        ("Counter", ctypes.c_uint32),
        ("Data", ctypes.c_int32),
    ]

    def get_event_type(self):
        if self.Type == EventType.BUTTON.bit_length():
            return "Button"
        if self.Type == EventType.ACTIVITY.bit_length():
            return "Activity"
        if self.Type == EventType.FREEFALL.bit_length():
            return "Freefall"
        if self.Type == EventType.ORIENTATION.bit_length():
            return "Orientation"
        if self.Type == EventType.START.bit_length():
            return "Start"
        if self.Type == EventType.TEMP.bit_length():
            return "Temp"
        return None

    def to_dataclass(self):
        return EventData(
            type=self.get_event_type(),
            value=self.Value,
            acceleration=self.Acceleration.to_dataclass(),
            number=self.Number,
            counter=self.Counter,
            data=self.Data
        )


