from dataclasses import dataclass

@dataclass
class ConfigDetector:
    low_freq: int | float
    high_freq: int | float
    win_sec: int | float
    refractory_sec: int| float
