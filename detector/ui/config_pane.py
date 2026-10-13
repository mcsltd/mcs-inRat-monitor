from PySide6.QtCore import Signal
from PySide6.QtWidgets import QFrame


from detector.res.frm_config_detector import Ui_FrmConfigDetector


class FrmConfigDetectorPane(QFrame, Ui_FrmConfigDetector):
    """ Класс-фрейм для настроек inRat """

    def __init__(self, detector, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)

        self._detector = detector
        data = [("Отключен", False), ("Включен", True)]
        for t, v in data:
            self.comboBoxSwitch.addItem(t, userData=v)

        self.set_default()
        self.pushButtonOk.clicked.connect(self._on_ok_clicked)

    def set_default(self):
        """ установка значений по умолчанию """
        idx = self.comboBoxSwitch.findData(self._detector.enable)
        self.comboBoxSwitch.setCurrentIndex(idx)

    def _on_ok_clicked(self):
        """ обработка нажатия кнопки применить """
        state = self.comboBoxSwitch.currentData()
        self._detector.enable = state
