from PySide6.QtWidgets import QFrame

from storage.res.frm_control_recording import Ui_frmControlRecording


class FrmControlStorage(QFrame, Ui_frmControlRecording):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)

    def set_enabled(self, enable: bool):
        if enable:
            self.pushButtonStart.setEnabled(True)
            self.pushButtonStop.setEnabled(False)
        else:
            self.pushButtonStart.setEnabled(False)
            self.pushButtonStop.setEnabled(False)

    def set_pause(self):
        """ состояние ожидания запуска """
        self.pushButtonStart.setEnabled(True)
        self.pushButtonStop.setEnabled(False)

    def set_start(self):
        """ состояние старта """
        self.pushButtonStart.setEnabled(False)
        self.pushButtonStop.setEnabled(True)