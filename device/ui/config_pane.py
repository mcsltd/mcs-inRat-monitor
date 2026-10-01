from PySide6.QtWidgets import QFrame

from device.res.frm_config_device import Ui_FrmConfigDevicePane


class FrmConfigDevicePane(QFrame, Ui_FrmConfigDevicePane):
    """ Класс-фрейм с настройками inRat """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.setWindowTitle("inRat")


