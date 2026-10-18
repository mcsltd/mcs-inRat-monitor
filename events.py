from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from device.models import DeviceProperty


@dataclass
class DeviceEvent:
    type: str   # connected, disconnected, acquisition, connection lost
    desc: str


@dataclass
class DevicePropertyEvent:
    property: "DeviceProperty"

