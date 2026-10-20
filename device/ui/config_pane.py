from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import QFrame, QComboBox, QMessageBox

from device.enums import TypeSignal
from device.models import ExgConfig, AccConfig, DeviceConfig, EventConfig
from device.res.frm_config_device import Ui_FrmConfigDevicePane


class FrmConfigDevicePane(QFrame, Ui_FrmConfigDevicePane):
    """ Класс-фрейм для настроек inRat """
    signal_apply = Signal(object)
    # запрос на подключение (открытие окна поиска устройств)
    signal_connect_requested = Signal()
    # запрос на отключение подключенного устройства
    signal_disconnect_requested = Signal()
    # выбор устройства из списка доступных
    signal_device_selected = Signal(object)

    def __init__(self, config, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.setWindowTitle("inRat")
        # показывать tooltip даже для заблокированной кнопки Применить
        self.pushButtonOk.setAttribute(Qt.WidgetAttribute.WA_AlwaysShowToolTips, True)

        # доступные устройства (имя -> BLEDevice)
        self._devices: dict[str, object] = {}

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
        self.comboBoxExg.currentIndexChanged.connect(self.on_exg_switched)

        self.pushButtonOk.clicked.connect(self._on_ok_clicked)

    def update_config(self, config):
        """ обновление конфигурации и перерисовка полей """
        self._config = config
        self.set_default()


    def set_default(self):
        """ установка настроек из конфигурации устройства """
        self.checkBoxActivated.setChecked(bool(self._config.activated))

        # сброс полей, заполняемых ниже по конфигурации
        self.comboBoxExg.setCurrentIndex(0)
        self.comboBoxExgGain.setCurrentIndex(0)
        self.comboBoxExgHpf.setCurrentIndex(0)
        self.comboBoxAcc.setCurrentIndex(0)
        self.comboBoxAccScale.setCurrentIndex(0)
        self.checkBoxTemp.setChecked(False)
        self.checkBoxActivity.setChecked(False)
        self.checkBoxOrientation.setChecked(False)
        self.checkBoxFreefall.setChecked(False)

        for sig in self._config.signals:
            if isinstance(sig, ExgConfig):
                idx = self.__find_sig_index(data=(sig.type_signal, sig.sample_rate), combobox=self.comboBoxExg)
                self.comboBoxExg.setCurrentIndex(idx)

                idx = self.comboBoxExgGain.findData(sig.gain)
                self.comboBoxExgGain.setCurrentIndex(idx)

                idx = self.comboBoxExgHpf.findData(sig.hpf)
                self.comboBoxExgHpf.setCurrentIndex(idx)

            elif isinstance(sig, AccConfig):
                idx = self.__find_sig_index(data=(sig.type_signal, sig.sample_rate), combobox=self.comboBoxAcc)
                self.comboBoxAcc.setCurrentIndex(idx)

                idx = self.comboBoxAccScale.findData(sig.scale)
                self.comboBoxAccScale.setCurrentIndex(idx)

        if self._config.events:
            if "T" in self._config.events.type_events:
                self.checkBoxTemp.setChecked(True)

            if self.groupBoxEv.isEnabled():
                events = {"A": self.checkBoxActivity, "O": self.checkBoxOrientation, "F": self.checkBoxFreefall}
                for key in events.keys():
                    if key in self._config.events.type_events:
                        events[key].setChecked(True)
                idx = self.comboBoxAcEvThreshold.findData(self._config.events.threshold)
                if idx >= 0:
                    self.comboBoxAcEvThreshold.setCurrentIndex(idx)

        # синхронизация доступности групп с текущим выбором комбобоксов
        self.on_acc_switched(0)
        self.on_exg_switched(0)

    def on_acc_switched(self, idx):
        """ обработка переключения сигналов акселерометра """
        value = self.comboBoxAcc.currentData()
        if value is None:
            self.groupBoxEv.setEnabled(True)
            self.comboBoxAcEvThreshold.setEnabled(True)
            self.comboBoxAccScale.setEnabled(False)
        else:
            self.groupBoxEv.setEnabled(False)
            self.comboBoxAcEvThreshold.setEnabled(False)
            self.comboBoxAccScale.setEnabled(True)

        self._update_ok_button()

    def on_exg_switched(self, idx):
        """ обработка переключения сигналов exg """
        value = self.comboBoxExg.currentData()
        if value is None:
            self.comboBoxExgGain.setEnabled(False)
            self.comboBoxExgHpf.setEnabled(False)
            self.checkBoxTemp.setChecked(False)
            checkboxes = [self.checkBoxTemp, self.checkBoxFreefall, self.checkBoxActivity, self.checkBoxOrientation]
            for box in checkboxes:
                box.setEnabled(False)
                box.setChecked(False)
        else:
            self.comboBoxExgGain.setEnabled(True)
            self.comboBoxExgHpf.setEnabled(True)
            checkboxes = [self.checkBoxTemp, self.checkBoxFreefall, self.checkBoxActivity, self.checkBoxOrientation]
            for box in checkboxes:
                box.setEnabled(True)

        self._update_ok_button()

    def _update_ok_button(self):
        """ блокировка кнопки применения, если exg и acc отключены """
        exg = self.comboBoxExg.currentData()
        acc = self.comboBoxAcc.currentData()
        enabled = exg is not None or acc is not None
        self.pushButtonOk.setEnabled(enabled)
        self.pushButtonOk.setToolTip("" if enabled else "Выберите ExG или Акселерометр")

    def _setup_combobox_acc(self):
        # настройка акселерометра
        data = [("Отключено", None), ("Включено, 100 Гц", (TypeSignal.ACC, 100))]
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
            ("ЭКГ, 500 Гц", (TypeSignal.ECG, 500)),
            ("ЭКГ, 1000 Гц", (TypeSignal.ECG, 1000)),
            ("ЭКГ, 2000 Гц", (TypeSignal.ECG, 2000)),
            ("ЭЭГ, 250 Гц", (TypeSignal.EEG, 250)),
            ("ЭЭГ, 500 Гц", (TypeSignal.EEG, 500))
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

    def _get_exg_config(self) -> ExgConfig | None:
        """ получение настроек сигнала exg """
        data_exg = self.comboBoxExg.currentData()
        if data_exg is None:
            return None
        type_signal, sample_rate = data_exg
        hpf = self.comboBoxExgHpf.currentData()
        gain = self.comboBoxExgGain.currentData()
        exg_config = ExgConfig(type_signal=type_signal, hpf=hpf, sample_rate=sample_rate, gain=gain,)
        return exg_config

    def _get_acc_config(self) -> AccConfig | None:
        """ получение настроек сигнала acc """
        data_acc = self.comboBoxAcc.currentData()
        if data_acc is None:
            return None
        type_signal, sample_rate = data_acc
        scale = self.comboBoxAccScale.currentData()
        acc_config = AccConfig(type_signal=type_signal, sample_rate=sample_rate, scale=scale)
        return acc_config

    def _get_event_config(self) -> EventConfig | None:
        """ получение настроек регистрации событий """
        event = []
        if self.checkBoxTemp.isChecked():
            event.append("T")
        if self.checkBoxActivity.isChecked():
            event.append("A")
        if self.checkBoxOrientation.isChecked():
            event.append("O")
        if self.checkBoxFreefall.isChecked():
            event.append("F")
        if len(event) != 0:
            threshold = self.comboBoxAcEvThreshold.currentData()
            event_config = EventConfig(type_events=event, threshold=threshold)
            return event_config
        else:
            return None

    def _get_config(self) -> DeviceConfig | None:
        """
        сохранение настроек
        DeviceConfig(
            activated=False,
            signals=[
                ExgConfig(type_signal="ecg", sample_rate=1000, hpf=0.83, gain=1),
                AccConfig(type_signal="acc", sample_rate=100, scale=2)
            ],
            events=EventConfig(type_events=["T",], threshold=2)
        )
        """
        exg_config = self._get_exg_config()
        acc_config = self._get_acc_config()
        ev_config = self._get_event_config()

        if exg_config is None and acc_config is None:
            return None

        config = DeviceConfig(
            activated=self.checkBoxActivated.isChecked(),
            signals=[exg_config, acc_config],
            events=ev_config
        )
        return config

    def _on_ok_clicked(self):
        """ обработка нажатия кнопки применить """
        config = self._get_config()

        if config is None:
            return

        self.signal_apply.emit(config)
