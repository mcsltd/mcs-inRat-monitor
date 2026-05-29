from PySide6.QtWidgets import QFrame

from resources.frm_online_control_device import Ui_FrmOnlineControlDevice


class FrmControlPane(QFrame, Ui_FrmOnlineControlDevice):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)

    def state_acquisition(self):
        self.pushButtonStart.setEnabled(False)
        self.pushButtonStop.setEnabled(True)
        self.pushButtonConfig.setEnabled(False)

    def state_connection(self):
        self.pushButtonStart.setEnabled(True)
        self.pushButtonStop.setEnabled(False)
        self.pushButtonConfig.setEnabled(True)

    def state_disconnect(self):
        self.pushButtonStart.setEnabled(False)
        self.pushButtonStop.setEnabled(False)
        self.pushButtonConfig.setEnabled(False)