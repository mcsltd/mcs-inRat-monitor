import logging
import struct
import numpy as np

from constants import Pkt, Const

logger = logging.getLogger(__name__)

class Decoder:
    def __init__(self):
        self.prev = 0
        self.last_counter = 0
        self.errors_count = 0

    def reset(self):
        self.prev = 0
        self.last_counter = 0
        self.errors_count = 0

    def decode(self, raw_data: bytearray) -> (int, np.ndarray):
        """
        Decode signal.
        :param raw_data: bytearray
        :return: (int, np.ndarray)
        """
        # read counter
        offset = 2
        counter = struct.unpack('<H', raw_data[:offset])[0]

        if counter == 1:
            self.reset()

        # check counter errors
        if self.last_counter + 1 != counter:
            self.errors_count += 1
            logger.debug(f"Error: last counter - {self.last_counter}, current counter - {counter}; errors - {self.errors_count}")
        self.last_counter = counter

        # read code
        code = struct.unpack('<I', raw_data[offset:offset + 4])[0]
        offset += 4

        # decode ecg
        ecg = np.zeros(Pkt.SamplesCountECG, dtype=np.float64)
        for i in range(Pkt.SamplesCountECG):
            if (code >> i) & 0x1 == 0x0:
                ecg[i] = self.prev + int.from_bytes([raw_data[offset]], signed=True, byteorder="little")
                offset += 1

            if (code >> i) & 0x1 == 0x1:
                ecg[i] = struct.unpack("<h", raw_data[offset:offset + 2])[0]
                offset += 2

            self.prev = ecg[i]

        ecg *= Const.EcgResolution # in V
        return counter, ecg
