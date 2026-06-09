import hashlib

from cryptography.hazmat.primitives.ciphers import algorithms, modes, Cipher


def get_control_sum(data: bytes, key: bytearray) -> bytes:
    """ Вспомогательная функция получения контрольной суммы """
    hash = hashlib.sha256(data).digest()
    iv = bytes(128 // 8)
    # create encoder
    cipher = Cipher(
        algorithm=algorithms.AES(key), mode=modes.CBC(iv)
    )
    encryptor = cipher.encryptor()
    # encrypt
    sign = encryptor.update(hash) + encryptor.finalize()
    return sign


def get_orientation(value: int):
    if bool(value & 32):
        return "z+"
    if bool(value & 16):
        return "z-"
    if bool(value & 8):
        return "y+"
    if bool(value & 4):
        return "y-"
    if bool(value & 2):
        return "x+"
    if bool(value & 1):
        return "x-"
    return None
