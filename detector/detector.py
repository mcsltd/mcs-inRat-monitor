import numpy as np
from scipy.signal import butter, lfilter


class RealTimeQRSDetector:

    def __init__(
            self,
            sampling_rate: int,
            buffer_duration_sec: float,
            low_cutoff: float = 15.0,
            high_cutoff: float = 50.0,
            refractory_period_sec: float = 0.07,
            algorithmic_delay_sec: float = 0.04,
            threshold_coefficient: float = 0.5
    ):
        """
        Универсальный Real-Time детектор R-пиков.

        :param sampling_rate: Частота дискретизации сигнала (Гц). Например: 500, 1000, 2000.
        :param buffer_duration_sec: Размер кольцевого буфера для визуализации/анализа в секундах.
        :param low_cutoff: Нижняя граница полосового фильтра (Гц). (Человек: 5.0, Крыса: 15.0)
        :param high_cutoff: Верхняя граница полосового фильтра (Гц). (Человек: 15.0, Крыса: 50.0)
        :param refractory_period_sec: Минимальное время между двумя R-пиками (сек). (Человек: 0.2, Крыса: 0.07)
        :param algorithmic_delay_sec: Искусственная задержка окна анализа (сек). Нужна, чтобы успеть
                                      зафиксировать спад R-волны. (Человек: 0.12, Крыса: 0.04)
        :param threshold_coefficient: Коэффициент жесткости порога (0.0 - 1.0). Чем выше, тем строже отбор пиков.
        """
        self._fs = sampling_rate
        self._buffer_size = int(sampling_rate * buffer_duration_sec)

        self._raw_buffer = np.zeros(self._buffer_size)
        self._filtered_buffer = np.zeros(self._buffer_size)

        # полосовой фильтр 15-50 Гц для резких пиков
        self._b, self._a = butter(N=2, Wn=[low_cutoff, high_cutoff], btype="bandpass", fs=self._fs)
        self._filter_zi = np.zeros(max(len(self._a), len(self._b)) - 1)

        # уменьшенная задержка для алгоритма - 40 мс для крысы
        self._delay_samples = int(algorithmic_delay_sec * self._fs)
        self._min_rr_samples = int(refractory_period_sec * self._fs)
        self._threshold_coef = threshold_coefficient

        # переменные состояния детектора
        self._last_peak_global_idx = -self._min_rr_samples
        self._threshold = 0.0
        self._total_samples = 0
        self._last_peak_abs_idx = -self._min_rr_samples

    def process_packet(self, packet) -> list:
        n_samples = len(packet)
        if n_samples == 0:
            return []

        self._total_samples += n_samples  # абсолютный счётчик

        # сдвиг буферов и запись нового пакета
        self._raw_buffer = np.roll(self._raw_buffer, -n_samples)
        self._raw_buffer[-n_samples:] = packet

        filtered_packet, self._filter_zi = lfilter(
            self._b, self._a, packet, zi=self._filter_zi
        )

        self._filtered_buffer = np.roll(self._filtered_buffer, -n_samples)
        self._filtered_buffer[-n_samples:] = filtered_packet

        start_idx = self._buffer_size - n_samples - self._delay_samples
        end_idx = self._buffer_size - self._delay_samples

        if start_idx < 1:  # нужно хотя бы по одному соседу с каждой стороны
            return []

        # захватываем на 1 отсчёт шире для проверки локальных максимумов
        zone_start = max(0, start_idx - 1)
        zone_end = min(self._buffer_size, end_idx + 1)
        analysis_zone = self._filtered_buffer[zone_start:zone_end]
        abs_zone = np.abs(analysis_zone)

        # обновление порога по модулю
        recent_history_samples = min(int(self._fs * 0.5), self._buffer_size)
        current_max = np.max(np.abs(self._filtered_buffer[-recent_history_samples:]))
        if current_max > 0:
            self._threshold = self._threshold_coef * current_max + (1 - self._threshold_coef) * self._threshold

        found_peaks = []

        if len(abs_zone) > 2:
            local_max_mask = (abs_zone[1:-1] > abs_zone[:-2]) & (abs_zone[1:-1] > abs_zone[2:])
            local_max_indices = np.where(local_max_mask)[0] + 1  # индексы в abs_zone

            for idx in local_max_indices:
                buffer_idx = zone_start + idx
                # проверяем, что пик внутри целевой зоны [start_idx, end_idx)
                if buffer_idx < start_idx or buffer_idx >= end_idx:
                    continue

                val = abs_zone[idx]
                if val > self._threshold:
                    abs_idx = self._total_samples - self._buffer_size + buffer_idx
                    if abs_idx - self._last_peak_abs_idx > self._min_rr_samples:
                        found_peaks.append(buffer_idx)
                        self._last_peak_abs_idx = abs_idx

        return found_peaks