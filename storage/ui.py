from PySide6.QtWidgets import QFrame

from resources.frm_online_control_recording import Ui_FrmOnlineControlRecording


def to_str_hhmmss(seconds) -> str:
    str_hh_mm_ss = f"{int(seconds // 3600):02d}:{int(seconds // 60):02d}:{seconds % 60:02d}"
    return str_hh_mm_ss

class FrmOnlineControlRecording(QFrame, Ui_FrmOnlineControlRecording):

    def __init__(self, module, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.module = module
        self._timer = 0
        self.startTimer(1000)

        self._timebase = 1200
        self.labelFileCounter.setText("000")

    @property
    def timebase(self):
        return self._timebase
    @timebase.setter
    def timebase(self, value: int):
        self._timebase = value

    def set_file_count(self, value):
        self.labelFileCounter.setText(f"{value:03d}")

    def enable_archive(self, state: bool = False):
        self.pushButtonOpenArchive.setEnabled(state)

    def set_enable(self):
        self.pushButtonSelectSaveDir.setEnabled(True)
        self.pushButtonStartRecording.setEnabled(True)
        self.pushButtonStopRecording.setEnabled(False)

    def set_disable(self):
        self.pushButtonSelectSaveDir.setEnabled(False)
        self.pushButtonStartRecording.setEnabled(False)
        self.pushButtonStopRecording.setEnabled(False)

    def timerEvent(self, event, /):
        if self.module._recording:
            self._timer += 1
        else:
            self._timer = 0
        self.labelRecordingTime.setText(f"{to_str_hhmmss(self._timer)}")