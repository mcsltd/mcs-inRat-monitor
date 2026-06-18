from dataclasses import dataclass
from enum import IntEnum
from functools import cached_property
from uuid import UUID

UUID_TEMPLATE = "0000{:0>4x}-0000-1000-8000-00805f9b34fb"
class inRatCharacteristic(IntEnum):

    MANUFACTURER_NAME = 0x2A29
    MODEL = 0x2A24
    SERIAL = 0x2A25
    FIRMWARE = 0x2A26
    HARDWARE = 0x2A27

    @cached_property
    def uuid(self) -> UUID:
        """Convert the ID to a full UUID and cache."""
        return UUID(UUID_TEMPLATE.format(self.value))

    def __str__(self) -> str:
        """Convert UUID to string value."""
        return str(self.uuid)


@dataclass(slots=True, frozen=True)
class Const:
    EcgResolution = (2.42 / 171.) / 0xFFFF
    AccResolution = 4000.0 / ((1 << 16) - 1)

@dataclass(slots=True, frozen=True)
class Pkt:
    SamplesCountEcg = 32
    ChannelsCountEcg = 1
    SamplesCountAcc = 8
    ChannelsCountAcc = 3