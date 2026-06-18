import struct
import numpy as np

from device.constants import Pkt, Const


def decode_signal(raw_data: bytearray, gain: int) -> (int, np.ndarray):
    """ Декодирование сырых данных в сигнал exg  """
    # read counter
    offset = 2
    counter = struct.unpack('<H', raw_data[:offset])[0]

    # read code
    code = struct.unpack('<I', raw_data[offset:offset + 4])[0]
    offset += 4

    # decode ecg
    exg = np.zeros((Pkt.ChannelsCountEcg, Pkt.SamplesCountEcg), dtype=np.float64)
    prev = 0
    for i in range(Pkt.SamplesCountEcg):
        if (code >> i) & 0x1 == 0x0:
            exg[:,i] = prev + int.from_bytes([raw_data[offset]], signed=True, byteorder="little")
            offset += 1

        if (code >> i) & 0x1 == 0x1:
            exg[:,i] = struct.unpack("<h", raw_data[offset:offset + 2])[0]
            offset += 2

        prev = exg[:,i]
    exg *= Const.EcgResolution / gain
    return counter, exg

def decode_acceleration(raw_data, enabled_channels):
    """ декодирование ускорения """
    offset = 2
    counter = struct.unpack('<H', raw_data[:offset])[0]

    prevs = np.zeros(Pkt.ChannelsCountAcc, dtype=np.int32)
    acceleration = np.zeros((Pkt.ChannelsCountAcc, Pkt.SamplesCountAcc), dtype=np.int32)
    for i in range(Pkt.SamplesCountAcc):
        code = raw_data[offset]
        offset += 1

        for ch in range(Pkt.ChannelsCountAcc):
            if enabled_channels >> (ch + 1) & 0x1 == 1:

                if (code >> ch) & 0x1 == 0x0:
                    val = prevs[ch] + int.from_bytes([raw_data[offset]], signed=True, byteorder="little")
                    offset += 1

                if (code >> ch) & 0x1 == 0x1:
                    val = struct.unpack("<h", raw_data[offset:offset+2])[0]
                    offset += 2

            prevs[ch] = val
            acceleration[ch][i] = int(val * 4000 / 0xFFFF)

    return counter, acceleration