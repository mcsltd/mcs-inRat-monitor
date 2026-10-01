from PySide6.QtWidgets import QFrame

from device.res.frm_control_device import Ui_FrmControlDevice
from device.res.frm_online_control_device import Ui_FrmOnlineControlDevice


class FrmControlDevicePane(QFrame, Ui_FrmControlDevice):
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
        self.pushButtonStart.setEnabled(True)
        self.pushButtonStop.setEnabled(False)

    def set_start(self):
        self.pushButtonStart.setEnabled(False)
        self.pushButtonStop.setEnabled(True)

    # def state_acquisition(self):
    #     self.pushButtonStart.setEnabled(False)
    #     self.pushButtonStop.setEnabled(True)
    #     self.pushButtonConfig.setEnabled(False)
    #     self.checkBoxActivated.setEnabled(False)

    # def state_connection(self):
    #     self.pushButtonStart.setEnabled(True)
    #     self.pushButtonStop.setEnabled(False)
    #     self.pushButtonConfig.setEnabled(True)
    #     self.checkBoxActivated.setEnabled(True)

    # def state_disconnect(self):
    #     self.pushButtonStart.setEnabled(False)
    #     self.pushButtonStop.setEnabled(False)
    #     self.pushButtonConfig.setEnabled(False)
    #     self.checkBoxActivated.setEnabled(False)
    #     self.checkBoxActivated.setChecked(False)