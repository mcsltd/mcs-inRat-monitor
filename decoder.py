import ctypes
import struct
import numpy as np

from constants import Pkt, Const
from structure import Event, EventData


def decode_ecg(raw_data: bytearray) -> (int, np.ndarray):
    """ Декодирование сырых данных в сигнал ЭКГ """
    # read counter
    offset = 2
    counter = struct.unpack('<H', raw_data[:offset])[0]

    # read code
    code = struct.unpack('<I', raw_data[offset:offset + 4])[0]
    offset += 4

    # decode ecg
    ecg = np.zeros(Pkt.SamplesCountECG, dtype=np.float64)
    prev = 0
    for i in range(Pkt.SamplesCountECG):
        if (code >> i) & 0x1 == 0x0:
            ecg[i] = prev + int.from_bytes([raw_data[offset]], signed=True, byteorder="little")
            offset += 1

        if (code >> i) & 0x1 == 0x1:
            ecg[i] = struct.unpack("<h", raw_data[offset:offset + 2])[0]
            offset += 2

        prev = ecg[i]
    # ecg *= Const.EcgResolution * 1e6
    ecg *= Const.EcgResolution # in V
    return counter, ecg

def decode_event(raw_data):
    """ декодирование событий """
    event_size = ctypes.sizeof(Event)
    cnt = int(len(raw_data) / event_size)
    for idx in range(cnt):
        offset = idx * event_size
        event = Event.from_buffer(raw_data[offset: offset + event_size]).to_dataclass()
        yield event