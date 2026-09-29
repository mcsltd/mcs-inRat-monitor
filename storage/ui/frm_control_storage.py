from PySide6.QtWidgets import QFrame

from storage.res.frm_control_recording import Ui_frmControlRecording


class FrmControlStorage(QFrame, Ui_frmControlRecording):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)