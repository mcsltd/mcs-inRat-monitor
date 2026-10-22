from dataclasses import dataclass, field

from device.enums import TypeSignal


@dataclass
class ExgConfig:
    """ Описание параметров сигнала Exg """
    type_signal: TypeSignal # eeg, ecg
    hpf: float
    sample_rate: int | float
    gain: int

@dataclass
class AccConfig:
    """ Описание параметров сигнала Acc """
    type_signal: TypeSignal # acc
    sample_rate: int | float
    scale: float


@dataclass
class EventConfig:
    """ структура настроек типов рег. событий """
    type_events: list[str]
    threshold: int

@dataclass
class DeviceConfig:
    """ структура хранения настроек устройства """
    activated: bool
    events: EventConfig
    signals: list[ExgConfig | AccConfig] = field(default_factory=list)

@dataclass
class DeviceProperty:
    """ структура описания свойств inRat """
    name: str
    serial: str
    model: str
    hardware: str
    firmware: str

@dataclass
class DeviceUsage:
    """ информация об использовании устройства """
    power_on_count: int
    advertising_sec: int
    connection_sec: int
    data_sec: int