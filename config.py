import os

from dotenv import load_dotenv

load_dotenv()

def parse_ble_key(key: str):
    """
    Сonvert string to bytearray to interact with ble devices.
    :param key: str
    :return: bytearray
    """
    hex_str = key.strip()
    hex_values = [x.strip().replace("0x", "") for x in hex_str.split(",")]
    return bytearray([int(b, 16) for b in hex_values])


BLE_KEY = parse_ble_key(os.getenv("INRAT"))
DATA_PATH = r".\data"

if not os.path.exists(DATA_PATH):
    os.mkdir(DATA_PATH)