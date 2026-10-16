import time

from PySide6.QtCore import QTimer
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QFrame

from storage.res.frm_info_rec import Ui_FrmInfoRecording


class FrmInfoRecording(QFrame, Ui_FrmInfoRecording):
    """ индикация о ведущейся записи """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)

        self.pushButton.setFixedSize(25, 25)
        self.labelFileCnt.setMinimumWidth(
            self.labelFileCnt.fontMetrics().horizontalAdvance("000")
        )

        self._icon = QIcon(":/images/record.png")

        self._start_time: float | None = None
        self._limit_sec: int = 0
        self._file_cnt: int = 0
        self._blink_on: bool = True

        self._timer = QTimer(self)
        self._timer.setInterval(1000)
        self._timer.timeout.connect(self._update_time)

        self._blink_timer = QTimer(self)
        self._blink_timer.setInterval(500)
        self._blink_timer.timeout.connect(self._toggle_blink)

        self._update_file_label()
        self.setVisible(False)

    def start(self, limit_sec: int):
        """ старт записи: показать индикатор и запустить отсчёт """
        self._limit_sec = limit_sec
        self._start_time = time.monotonic()
        self._file_cnt = 0
        self._update_file_label()

        self._blink_on = True
        self.pushButton.setIcon(self._icon)
        self._update_time()

        self.setVisible(True)
        self._timer.start()
        self._blink_timer.start()

    def new_file(self, limit_sec: int):
        """ начало нового файла: сбросить только отсчёт времени """
        self._limit_sec = limit_sec
        self._start_time = time.monotonic()
        self._update_time()

    def stop(self):
        """ остановка записи: скрыть индикатор """
        self._timer.stop()
        self._blink_timer.stop()
        self.pushButton.setIcon(self._icon)
        self.setVisible(False)

    def set_file_count(self, count: int):
        """ обновление числа записанных файлов """
        self._file_cnt = count
        self._update_file_label()

    def _update_time(self):
        elapsed = int(time.monotonic() - self._start_time) if self._start_time is not None else 0
        self.labelRecTime.setText(f"{self._format_time(elapsed)}/{self._format_time(self._limit_sec)}")

    def _update_file_label(self):
        self.labelFileCnt.setText(str(self._file_cnt) if self._file_cnt >= 1 else "")

    def _toggle_blink(self):
        self._blink_on = not self._blink_on
        self.pushButton.setIcon(self._icon if self._blink_on else QIcon())

    @staticmethod
    def _format_time(sec: int) -> str:
        sec = max(0, int(sec))
        return f"{sec // 60:02d}:{sec % 60:02d}"
