import ctypes


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
        ("Activated", ctypes.c_uint16), # 0 - not activated, 1 - activated
        ("Vddio", ctypes.c_uint16),     # what is it?
        ("Usage", Usage)
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

class Acceleration(ctypes.Structure):
    _pack_ = 1  # remove offset
    _fields_ = [
        ("X", ctypes.c_int16),
        ("Y", ctypes.c_int16),
        ("Z", ctypes.c_int16)
    ]

class Event(ctypes.Structure):
    _pack_ = 1 # remove offset
    _fields_ = [
        ("Type", ctypes.c_uint8),
        ("Value", ctypes.c_uint8),
        ("Acceleration", Acceleration),
        ("Number", ctypes.c_uint32),
        ("Counter", ctypes.c_uint32),
        ("Data", ctypes.c_int32),
    ]