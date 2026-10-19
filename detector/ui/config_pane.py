from PySide6.QtCore import Signal
from PySide6.QtWidgets import QFrame, QMessageBox

from detector.models import CONFIG_HUMAN, CONFIG_RAT, ConfigDetector, Subject
from detector.res.frm_config_detector import Ui_FrmConfigDetector

PRESETS = {Subject.HUMAN: CONFIG_HUMAN, Subject.RAT: CONFIG_RAT}


class FrmConfigDetectorPane(QFrame, Ui_FrmConfigDetector):
    """ Класс-фрейм для настроек детектора r-пиков """
    signal_apply = Signal(object)

    def __init__(self, detector, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self._detector = detector

        self._setup_combobox_switch()
        self._setup_combobox_object()

        self.set_default()

        self.comboBoxSwitch.currentIndexChanged.connect(self._on_switch_changed)
        self.comboBoxObject.currentIndexChanged.connect(self._on_object_changed)
        self.pushButtonOk.clicked.connect(self._on_ok_clicked)

    def _setup_combobox_switch(self):
        data = [("Отключен", False), ("Включен", True)]
        for text, value in data:
            self.comboBoxSwitch.addItem(text, userData=value)

    def _setup_combobox_object(self):
        data = [("Человек", Subject.HUMAN), ("Крыса", Subject.RAT)]
        for text, subject in data:
            self.comboBoxObject.addItem(text, userData=subject)

    def set_default(self):
        """ установка значений по умолчанию """
        config = self._detector.config
        self.comboBoxSwitch.setCurrentIndex(self.comboBoxSwitch.findData(config.enabled))
        self.comboBoxObject.setCurrentIndex(self.comboBoxObject.findData(config.subject))
        self._fill_params(config)
        self.groupBoxDetectorParams.setEnabled(config.enabled)

    def _fill_params(self, config: ConfigDetector):
        """ заполнение полей параметров детектора """
        self.lineEditLowHz.setText(str(config.low_freq))
        self.lineEditHighHz.setText(str(config.high_freq))
        self.lineEditIntegrWin.setText(str(config.win_sec))
        self.lineEditRef.setText(str(config.refractory_sec))
        self.lineEditTwave.setText(str(config.twave_sec))

    def _on_switch_changed(self, idx):
        """ включение/отключение группы параметров детектора """
        self.groupBoxDetectorParams.setEnabled(bool(self.comboBoxSwitch.currentData()))

    def _on_object_changed(self, idx):
        """ подстановка пресета параметров для выбранного объекта """
        preset = PRESETS.get(self.comboBoxObject.currentData())
        if preset is not None:
            self._fill_params(preset)

    def _get_config(self) -> ConfigDetector | None:
        """ сборка конфига из полей с валидацией """
        try:
            low = float(self.lineEditLowHz.text())
            high = float(self.lineEditHighHz.text())
            win = float(self.lineEditIntegrWin.text())
            ref = float(self.lineEditRef.text())
            twave = float(self.lineEditTwave.text())
        except ValueError:
            self._show_error("Параметры детектора должны быть числами")
            return None

        if not 0 < low < high:
            self._show_error(
                "Границы полосового фильтра должны удовлетворять условию: "
                "0 < нижняя < верхняя")
            return None
        if win <= 0:
            self._show_error("Окно интегрирования должно быть больше нуля")
            return None
        if ref <= 0:
            self._show_error("Рефрактерный период должен быть больше нуля")
            return None
        if twave <= 0:
            self._show_error("Длительность T-волны должна быть больше нуля")
            return None

        return ConfigDetector(
            low_freq=low,
            high_freq=high,
            win_sec=win,
            refractory_sec=ref,
            twave_sec=twave,
            enabled=bool(self.comboBoxSwitch.currentData()),
            subject=self.comboBoxObject.currentData(),
        )

    def _show_error(self, msg: str):
        QMessageBox.warning(self, "Ошибка", msg, QMessageBox.StandardButton.Ok)

    def _on_ok_clicked(self):
        """ обработка нажатия кнопки применить """
        config = self._get_config()
        if config is not None:
            self.signal_apply.emit(config)
