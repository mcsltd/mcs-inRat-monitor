from dataclasses import dataclass, field


@dataclass
class ExgConfig:
    """ Описание параметров сигнала Exg """
    type_signal: str # eeg, ecg
    hpf: float
    sample_rate: int | float
    gain: int

@dataclass
class AccConfig:
    """ Описание параметров сигнала Acc """
    type_signal: str # acc
    sample_rate: int | float
    scale: float


@dataclass
class EventsConfig:
    """ структура настроек типов рег. событий """
    type_events: list[str]
    threshold: int

@dataclass
class DeviceConfig:
    """ структура хранения настроек устройства """
    activated: bool
    events: EventsConfig
    signals: list[ExgConfig | AccConfig] = field(default_factory=list)

@dataclass
class DeviceProperty:
    """ структура описания свойств inRat """
    name: str
    serial: str
    model: str
    hardware: str
    firmware: str