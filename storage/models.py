from dataclasses import dataclass


@dataclass
class StorageConfig:
    """ параметры записи данных в файл """
    write_dir: str | None
    duration_min: int
