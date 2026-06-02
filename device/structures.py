import ctypes


class Settings(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("DataRateEcgEeg", ctypes.c_uint8), # ECG(0-500, 1-1000, 2-2000) EEG(0-250, 1-500)
        ("HPFandGain", ctypes.c_uint8),
        ("FullScaleAccelerometer", ctypes.c_uint8),
        ("EnabledChannels", ctypes.c_uint8),
        ("EnabledEvents", ctypes.c_uint16),
        ("ActivityThreshold", ctypes.c_uint16),
    ]


class Acceleration(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("X", ctypes.c_int16),
        ("Y", ctypes.c_int16),
        ("Z", ctypes.c_int16)
    ]


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



class Usage(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("PowerOnCount", ctypes.c_uint32),
        ("AdvertisingSeconds", ctypes.c_uint32),
        ("ConnectionSeconds", ctypes.c_uint32),
        ("DataSendSeconds", ctypes.c_uint32)
    ]

class Status(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("Activated", ctypes.c_uint16),
        ("Vddio", ctypes.c_uint16),
        ("Usage", Usage)
    ]
