import struct

import numpy as np

from device.constants import Pkt, Const


class Decoder:

    def decode_ecg(self, raw_data: bytearray):
        # read counter
        offset = 2
        counter = struct.unpack('<H', raw_data[:offset])[0]

        # read code
        code = struct.unpack('<I', raw_data[offset:offset + 4])[0]
        offset += 4

        # decode ecg
        ecg = np.zeros(Pkt.SamplesCountEcg, dtype=np.float64)
        prev = 0
        for i in range(Pkt.SamplesCountEcg):
            if (code >> i) & 0x1 == 0x0:
                ecg[i] = prev + int.from_bytes([raw_data[offset]], signed=True, byteorder="little")
                offset += 1

            if (code >> i) & 0x1 == 0x1:
                ecg[i] = struct.unpack("<h", raw_data[offset:offset + 2])[0]
                offset += 2

            prev = ecg[i]

        ecg *= Const.EcgResolution  # in V
        return counter, ecg