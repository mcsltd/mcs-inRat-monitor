from PySide6.QtWidgets import QFrame

from ble_scanner.res.frm_control_scanner import Ui_FrmControlScanner


class FrmControlScannerPane(QFrame, Ui_FrmControlScanner):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)