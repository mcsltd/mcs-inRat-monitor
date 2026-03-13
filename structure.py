import ctypes
from dataclasses import dataclass

from constants import EventType


class Usage(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("PowerOnCount", ctypes.c_uint32),
        ("AdvertisingSeconds", ctypes.c_uint32),
        ("ConnectionSeconds", ctypes.c_uint32),
        ("DataSendSeconds", ctypes.c_uint32),
    ]


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


@dataclass
class AccelerationData:
    x: int
    y: int
    z: int

class Acceleration(ctypes.Structure):
    _pack_ = 1  # remove offset
    _fields_ = [
        ("X", ctypes.c_int16),
        ("Y", ctypes.c_int16),
        ("Z", ctypes.c_int16)
    ]

    def to_dataclass(self):
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


@dataclass
class UsageData:
    power_on_count: int
    advertising_seconds: int
    connection_seconds: int
    data_send_seconds: int

    def __str__(self):
        return (f"Использование: PowerOnCount={self.power_on_count}; AdvertisingSeconds={self.advertising_seconds}; "
                f"ConnectionSeconds={self.connection_seconds}; DataSendSeconds={self.data_send_seconds}")

@dataclass
class StatusData:
    activated: bool
    vddio: int
    usage: UsageData

    def __str__(self):
        return f"Статус: Activated={self.activated}; Vddio={self.vddio}; {str(self.usage)}"

class Status(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("Activated", ctypes.c_uint16),
        ("Vddio", ctypes.c_uint16),
        ("Usage", Usage)
    ]
    def to_dataclass(self) -> StatusData:
        return StatusData(
            activated= self.Activated == 1,
            vddio=self.Vddio,
            usage = UsageData(
                power_on_count=self.Usage.PowerOnCount,
                advertising_seconds=self.Usage.AdvertisingSeconds,
                connection_seconds=self.Usage.ConnectionSeconds,
                data_send_seconds=self.Usage.DataSendSeconds
              )
        )