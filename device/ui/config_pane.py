from PySide6.QtWidgets import QFrame

from device.enums import TypeSignal
from device.res.frm_config_device import Ui_FrmConfigDevicePane


class FrmConfigDevicePane(QFrame, Ui_FrmConfigDevicePane):
    """ Класс-фрейм с настройками inRat """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.setWindowTitle("inRat")

        # setup combobox
        self.setup_combobox_acc()
        self.setup_combobox_exg()
        self.setup_combobox_scale()
        self.setup_combobox_threshold()
        self.setup_combobox_hpf()
        self.setup_combobox_gain()
        self.setup_combobox_temp()

    def setup_combobox_acc(self):
        # настройка акселерометра
        data = ["Отключено", "Включено, 100 Гц"]
        for text in data:
            self.comboBoxAcc.addItem(text)

    def setup_combobox_threshold(self):
        # порог обнаружения событий
        thresholds = [("низкая", 2), ("средняя", 6), ("высокая", 9)]
        for text, thr in thresholds:
            self.comboBoxEvSens.addItem(text, thr)

    def setup_combobox_temp(self):
        # температура
        data_temp = ["Отключено", "Включено"]
        for text in data_temp:
            self.comboBoxTemp.addItem(text)

    def setup_combobox_exg(self):
        # настройка exg
        data = ["ЭКГ, 500 Гц", "ЭКГ, 1000 Гц", "ЭКГ, 2000 Гц", "ЭЭГ, 250 Гц", "ЭЭГ, 500 Гц"]
        for t in data:
            self.comboBoxExg.addItem(t)

    def setup_combobox_scale(self):
        # установка параметров масштаба акселерометра
        scale = [("±2g", 2), ("±4g", 4), ("±8g", 8), ("±16g", 16)]
        for s, v in scale:
            self.comboBoxScaleAcc.addItem(s, userData=v)

    def setup_combobox_gain(self):
        """ заполнение comboboxHpfGain элементами в режиме регистрации ЭЭГ """
        self.comboBoxGain.clear()
        gain = [("1x", 1), ("2x", 2), ("3x", 3), ("4x", 4)]
        for t, v in gain:
            self.comboBoxGain.addItem(t, userData=v)

    def setup_combobox_hpf(self):
        """ заполнение comboboxHpfGain элементами в режиме регистрации ЭЭГ """
        self.comboBoxHpf.clear()
        hpf = [("0.83 Гц", 0.83), ("2.5 Гц", 2.5)]
        for t, v in hpf:
            self.comboBoxHpf.addItem(t, userData=v)
