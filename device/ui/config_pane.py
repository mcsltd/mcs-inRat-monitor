from PySide6.QtWidgets import QFrame, QComboBox

from device.models import ExgConfig, AccConfig
from device.res.frm_config_device import Ui_FrmConfigDevicePane


class FrmConfigDevicePane(QFrame, Ui_FrmConfigDevicePane):
    """ Класс-фрейм для настроек inRat """

    def __init__(self, config, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.setWindowTitle("inRat")

        # setup combobox
        self._setup_combobox_exg()
        self._setup_combobox_hpf()
        self._setup_combobox_gain()
        self._setup_combobox_acc()
        self._setup_combobox_scale()
        self._setup_combobox_threshold()

        self._config = config
        self.set_default()

        self.comboBoxAcc.currentIndexChanged.connect(self.on_acc_switched)

    def set_default(self):
        """ установка настроек по умолчанию """
        if self._config.activated:
            self.checkBoxActivated.setChecked(True)

        for sig in self._config.signals:
            if isinstance(sig, ExgConfig):
                idx = self.__find_sig_index(data=(sig.type_signal, sig.sample_rate), combobox=self.comboBoxExg)
                self.comboBoxExg.setCurrentIndex(idx)

                idx = self.comboBoxExgGain.findData(sig.gain)
                self.comboBoxExgGain.setCurrentIndex(idx)

                idx = self.comboBoxExgHpf.findData(sig.hpf)
                self.comboBoxExgHpf.setCurrentIndex(idx)

            elif isinstance(sig, AccConfig):
                self.groupBoxEv.setEnabled(False)
                idx = self.__find_sig_index(data=(sig.type_signal, sig.sample_rate), combobox=self.comboBoxAcc)
                self.comboBoxAcc.setCurrentIndex(idx)

                idx = self.comboBoxAccScale.findData(sig.scale)
                self.comboBoxAccScale.setCurrentIndex(idx)

        if "T" in self._config.events.type_events:
            self.checkBoxTemp.setChecked(True)

        if self._config.events and self.groupBoxEv.isEnabled():
            events = {"A": self.checkBoxActivity, "O": self.checkBoxOrientation, "F": self.checkBoxFreefall}
            for key in events.keys():
                if key in self._config.events.type_events:
                    events[key].setChecked(True)
            # self.comboBoxEvSens.findData(data=self._config.events.sensitivity)

    def on_acc_switched(self, idx):
        """ обработка переключения сигналов акселерометра """
        value = self.comboBoxAcc.currentData()
        if value:
            self.groupBoxEv.setEnabled(False)
        else:
            self.groupBoxEv.setEnabled(True)

    def _setup_combobox_acc(self):
        # настройка акселерометра
        data = [("Отключено", None), ("Включено, 100 Гц", ("acc", 100))]
        for text, value in data:
            self.comboBoxAcc.addItem(text, userData=value)

    def _setup_combobox_threshold(self):
        # порог обнаружения событий
        thresholds = [(str(i), i) for i in range(1, 10)]
        for text, thr in thresholds:
            self.comboBoxAcEvThreshold.addItem(text, thr)

    def _setup_combobox_exg(self):
        # настройка exg
        data = [
            ("Отключено", None),
            ("ЭКГ, 500 Гц", ("ecg", 500)),
            ("ЭКГ, 1000 Гц", ("ecg", 1000)),
            ("ЭКГ, 2000 Гц", ("ecg", 2000)),
            ("ЭЭГ, 250 Гц", ("eeg", 250)),
            ("ЭЭГ, 500 Гц", ("eeg", 500))
        ]
        for text, value in data:
            self.comboBoxExg.addItem(text, userData=value)

    def _setup_combobox_scale(self):
        # установка параметров масштаба акселерометра
        scale = [("±2g", 2), ("±4g", 4), ("±8g", 8), ("±16g", 16)]
        for s, v in scale:
            self.comboBoxAccScale.addItem(s, userData=v)

    def _setup_combobox_gain(self):
        """ заполнение comboboxHpfGain элементами в режиме регистрации ЭЭГ """
        self.comboBoxExgGain.clear()
        gain = [("1x", 1), ("2x", 2), ("3x", 3), ("4x", 4)]
        for t, v in gain:
            self.comboBoxExgGain.addItem(t, userData=v)

    def _setup_combobox_hpf(self):
        """ заполнение comboboxHpfGain элементами в режиме регистрации ЭЭГ """
        self.comboBoxExgHpf.clear()
        hpf = [("0.83 Гц", 0.83), ("2.5 Гц", 2.5)]
        for t, v in hpf:
            self.comboBoxExgHpf.addItem(t, userData=v)

    @staticmethod
    def __find_sig_index(data: tuple[str, int | float], combobox: QComboBox) -> int:
        """ вернуть индекс соответствующих значению """
        for idx in range(combobox.count()):
            value = combobox.itemData(idx)
            if data == value:
                return idx
        return 0