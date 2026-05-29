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