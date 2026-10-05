from dataclasses import dataclass


@dataclass
class DeviceEvent:
    type: str   # connected, disconnected, acquisition, connection lost
    desc: str

