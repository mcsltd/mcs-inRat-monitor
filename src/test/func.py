import struct
import numpy as np

from src.constants import Pkt, Const
from src.decoder import Decoder


def read_file(filename: str = "./data_decoder/test.txt") -> np.ndarray:
    signal = np.array([], dtype=int)
    with open(filename, "r") as file:
        for line in file.readlines():
            signal = np.append(signal, int(line.split()[1]))
    return signal


def read_binary_file(binary_filename: str = "./data_decoder/test.bin"):
    with open(binary_filename, "rb") as binary_file:
        raw_data = binary_file.read()
    return raw_data

def decode_raw_data(raw_data: bytes):
    offset = 0

    while offset != len(raw_data):
        last_offset = offset

        # read counter
        offset += 2
        counter = struct.unpack('<H', raw_data[last_offset:offset])[0]

        # read code
        code = struct.unpack('<I', raw_data[offset:offset + 4])[0]
        offset += 4

        # calc size of bytes ecg
        for i in range(Pkt.SamplesCountECG):
            if (code >> i) & 0x1 == 0x0:
                offset += 1

            if (code >> i) & 0x1 == 0x1:
                offset += 2

        yield bytearray(raw_data[last_offset:offset])


def test_decoder():
    test_signal = np.array([], dtype=int)
    decoder = Decoder()

    raw_data = read_binary_file()
    for raw_batch in decode_raw_data(raw_data):
        test_signal = np.append(test_signal, decoder.decode(raw_batch)[1])

    etalon_signal = read_file() * Const.EcgResolution # in V

    assert np.array_equal(test_signal, etalon_signal)

test_decoder()