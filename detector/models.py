from dataclasses import dataclass
from enum import Enum


class Subject(str, Enum):
    """ Объект исследования """
    HUMAN = "human"
    RAT = "rat"


@dataclass
class ConfigDetector:
    low_freq: int | float
    high_freq: int | float
    win_sec: int | float
    refractory_sec: int | float
    twave_sec: int | float = 0.15
    enabled: bool = False
    subject: Subject = Subject.HUMAN


CONFIG_HUMAN = ConfigDetector(
    low_freq=5, high_freq=15, win_sec=0.15, refractory_sec=0.2,
    twave_sec=0.15, subject=Subject.HUMAN)
CONFIG_RAT = ConfigDetector(
    low_freq=8, high_freq=30, win_sec=0.04, refractory_sec=0.08,
    twave_sec=0.12, subject=Subject.RAT)
