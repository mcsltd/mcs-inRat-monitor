from PySide6.QtWidgets import QFrame

from device.models import ExgConfig, AccConfig
from device.res.frm_config_device import Ui_FrmConfigDevicePane


class FrmConfigDevicePane(QFrame, Ui_FrmConfigDevicePane):
    """ Класс-фрейм для настроек inRat """

    def __init__(self, config, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.setWindowTitle("inRat")

        # setup combobox
        self._setup_combobox_acc()
        self._setup_combobox_exg()
        self._setup_combobox_scale()
        self._setup_combobox_threshold()
        self._setup_combobox_hpf()
        self._setup_combobox_gain()

        self._config = config
        self.set_default()

        self.comboBoxAcc.currentIndexChanged.connect(self.on_acc_switched)

    def set_default(self):
        """ установка настроек по умолчанию """
        if self._config.activated:
            self.checkBoxActivated.setChecked(True)

        for sig in self._config.signals:
            if isinstance(sig, ExgConfig):
                idx = self.comboBoxExg.findData((sig.type_signal, sig.sample_rate))
                if idx == -1:
                    self.comboBoxExg.setCurrentIndex(0)
                else:
                    self.comboBoxExg.setCurrentIndex(idx)

                idx = self.comboBoxGain.findData(sig.gain)
                self.comboBoxGain.setCurrentIndex(idx)

                idx = self.comboBoxHpf.findData(sig.hpf)
                self.comboBoxHpf.setCurrentIndex(idx)

            elif isinstance(sig, AccConfig):
                self.groupBoxEv.setEnabled(False)
                idx = self.comboBoxAcc.findData((sig.type_signal, sig.sample_rate))
                self.comboBoxAcc.setCurrentIndex(idx)

                idx = self.comboBoxScaleAcc.findData((sig.type_signal, sig.scale))
                self.comboBoxScaleAcc.setCurrentIndex(idx)

        if self._config.events and self.groupBoxEv.isEnabled():
            events = {
                "T": self.checkBoxTemp, "A": self.checkBoxActivity,
                "O": self.checkBoxOrientation, "F": self.checkBoxFreefall
            }
            for key in events.keys():
                if key in self._config.events.type_events:
                    events[key].setChecked(True)
            # self.comboBoxEvSens.findData(data=self._config.events.sensitivity)


        # set activate
        # ecg, 1000 Hz
        # acc, 100 Hz
        # disable activity event
        # enable temp

    def on_acc_switched(self, idx):
        """ обработка переключения сигналов акселерометра """
        value = self.comboBoxAcc.currentData()
        if value:
            self.groupBoxEv.setEnabled(False)
        else:
            self.groupBoxEv.setEnabled(True)

    def _setup_combobox_acc(self):
        # настройка акселерометра
        data = [("Отключено", False), ("Включено, 100 Гц", True)]
        for text, value in data:
            self.comboBoxAcc.addItem(text, userData=value)

    def _setup_combobox_threshold(self):
        # порог обнаружения событий
        thresholds = [("низкая", 2), ("средняя", 6), ("высокая", 9)]
        for text, thr in thresholds:
            self.comboBoxEvSens.addItem(text, thr)

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
            self.comboBoxScaleAcc.addItem(s, userData=v)

    def _setup_combobox_gain(self):
        """ заполнение comboboxHpfGain элементами в режиме регистрации ЭЭГ """
        self.comboBoxGain.clear()
        gain = [("1x", 1), ("2x", 2), ("3x", 3), ("4x", 4)]
        for t, v in gain:
            self.comboBoxGain.addItem(t, userData=v)

    def _setup_combobox_hpf(self):
        """ заполнение comboboxHpfGain элементами в режиме регистрации ЭЭГ """
        self.comboBoxHpf.clear()
        hpf = [("0.83 Гц", 0.83), ("2.5 Гц", 2.5)]
        for t, v in hpf:
            self.comboBoxHpf.addItem(t, userData=v)
