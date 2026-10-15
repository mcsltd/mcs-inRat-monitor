import numpy as np
from scipy.signal import butter, lfilter, sosfilt

from detector.models import ConfigDetector




class RealTimeRPeakDetector:

    """ Класс детектора r-пиков"""

    def __init__(self, sampling_rat: float, config: ConfigDetector, init_sec = 2.0):
        """
        Детектор R пиков в реальном времени
        """
        self._config = config
        self._fs = float(sampling_rat)

        # полосовой бих-фильтр
        self._sos = butter(
            2, [self._config.low_freq, self._config.high_freq], fs=self._fs,
            btype="bandpass", output="sos")
        self._zi_bandpass = np.zeros((self._sos.shape[0], 2))

        # 5-точечный дифференциатор
        # y[n] = (2*x[n] + x[n-1] - x[n-3] - 2*x[n-4]) / 8
        self._diff_kernel = np.array([2.0, 1.0, 0.0, -1.0, -2.0]) / 8.0
        self._diff_buffer = np.zeros(len(self._diff_kernel))  # ring на 5 отсчётов

        # скользящее интегрирование
        self._integ_win = max(1, int(round(self._config.win_sec * self._fs)))
        self._integ_buffer = np.zeros(self._integ_win)
        self._integ_sum = 0.0
        self._integ_pos = 0

        # пороги и адаптация
        self._spki = 1e-3
        self._npki = 1e-4
        self._refractory = int(round(self._config.refractory_sec * self._fs))
        self._t_wave_win = int(round(self._config.twave_sec * self._fs))

        # глобальное состояние времени
        self._sample_count = 0
        self._last_qrs_idx = -self._refractory  # глобальный индекс последнего R

        # детекция пиков с задержкой в 1 отсчёт
        self._prev_integ = 0.0  # y[n-1] огибающей
        self._prev_prev_integ = 0.0  # y[n-2] огибающей
        self._pending_peak_idx = -1  # индекс кандидата в пик
        self._pending_peak_val = 0.0

        # фаза обучения
        self._init_samples = int(round(init_sec * self._fs))
        self._learn_peaks = []  # амплитуды пиков во время обучения
        self._learning = True

        # буферы для возврата к реальным r
        self._raw_buffer_len = int(round(0.4 * self._fs))  # ~400 мс истории
        self._raw_buffer = np.zeros(self._raw_buffer_len)
        self._raw_pos = 0

        # амплитуда последнего QRS
        self._last_qrs_val = 0.0

    def process_packet(self, packet) -> list:
        """
        обрабатывает пакет из 32 отсчётов,
        возвращает список абсолютных индексов r-пиков
        """
        packet = np.asarray(packet, dtype=float).ravel()
        detected = []

        # полосовой фильтр
        filtered, self._zi_bandpass = sosfilt(self._sos, packet, zi=self._zi_bandpass)

        for x in filtered:
            # дифферециатор
            self._diff_buffer = np.roll(self._diff_buffer, 1)
            self._diff_buffer[0] = x
            d = float(np.dot(self._diff_kernel, self._diff_buffer))

            # квадрат
            sq = d ** 2

            # скользящее интегрирование
            old = self._integ_buffer[self._integ_pos]
            self._integ_buffer[self._integ_pos] = sq
            self._integ_sum += sq - old
            self._integ_pos = (self._integ_pos + 1) % self._integ_win
            integ = self._integ_sum / self._integ_win

            # детекция пика
            if (self._prev_integ > self._prev_prev_integ
                    and self._prev_integ >= integ):
                peak_idx = self._sample_count - 1
                peak_val = self._prev_integ
                r = self._handle_peak(peak_idx, peak_val)
                if r is not None:
                    detected.append(r)

                # сдвиг истории огибающей
            self._prev_prev_integ = self._prev_integ
            self._prev_integ = integ
            self._sample_count += 1

        return detected

    def _handle_peak(self, peak_idx: int, peak_val: float):
        """
        Логика пороговой детекции для одного пика огибающей.
        Возвращает либо индекс R пика, либо None
        """
        # фаза обучения
        if self._learning:
            self._learn_peaks.append(peak_val)
            if self._sample_count >= self._init_samples:
                if self._learn_peaks:
                    self._spki = max(self._learn_peaks) / 3.0
                    self._npki = float(np.mean(self._learn_peaks)) / 2.0
                self._learning = False
            return None

        # пороги
        thr_i1 = self._npki + 0.25 * (self._spki - self._npki)
        thr_i2 = 0.5 * thr_i1

        # рефрактерность
        if peak_idx - self._last_qrs_idx < self._refractory:
            if peak_val < thr_i1:
                self._npki = 0.125 * peak_val + 0.875 * self._npki
            return None

        # правило T-зубца
        if self._last_qrs_idx >= 0:
            dt = peak_idx - self._last_qrs_idx
            if dt < self._t_wave_win and peak_val < 0.5 * self._last_qrs_val:
                self._npki = 0.125 * peak_val + 0.875 * self._npki
                return None

        # решение по порогам
        if peak_val > thr_i1:
            # QRS
            self._spki = 0.125 * peak_val + 0.875 * self._spki
            self._last_qrs_idx = peak_idx
            self._last_qrs_val = peak_val
            return peak_idx
        elif peak_val > thr_i2:
            # просто шум (обратный поиск не реализован)
            self._npki = 0.125 * peak_val + 0.875 * self._npki
            return None
        else:
            self._npki = 0.125 * peak_val + 0.875 * self._npki
            return None