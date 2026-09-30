from PySide6.QtWidgets import QDialog

from resources.dlg_config import Ui_DlgConfig


class DlgConfig(QDialog, Ui_DlgConfig):
    """ Диалоговое окно настройки модулей """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
