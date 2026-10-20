import numpy as np


def copy_packet(data: dict) -> dict:
    """ копия пакета данных для передачи между потоками/приёмниками.

    Замена copy.deepcopy в горячем пути: numpy-сигнал копируется,
    остальные поля (скаляры, enum-события) передаются общими ссылками.
    """
    signal = data.get("signal")
    if isinstance(signal, np.ndarray):
        return {**data, "signal": signal.copy()}
    return dict(data)
