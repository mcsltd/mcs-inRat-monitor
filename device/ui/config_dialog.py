from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QDialog

from device.enums import EventType, Mode, EnabledChannels, TypeSignal
from device.inrat import inRat, FIRMWARE_V0, FIRMWARE_V1
from resources.dlg_inrat_config_v1 import Ui_DlgDeviceConfig


class DlgConfigDevice(QDialog, Ui_DlgDeviceConfig):

    signal_acc = Signal(bool)
    signal_ecg_emg = Signal(bool)

    def __init__(self, device: inRat, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)

        self._device = device

        data = [("ЭКГ, 500 Гц", (TypeSignal.ECG, 500)), ("ЭКГ, 1000 Гц", (TypeSignal.ECG, 1000)),
                ("ЭКГ, 2000 Гц", (TypeSignal.ECG, 2000)), ("ЭЭГ, 250 Гц", (TypeSignal.EEG, 250)),
                ("ЭЭГ, 500 Гц", (TypeSignal.EEG, 500))]
        for t, v in data:
            self.comboBoxModeSampleRate.addItem(t, userData=v)

        scale = [("±2", 2), ("±4", 4), ("±8", 8), ("±16", 16)]
        for s, v in scale:
            self.comboBoxFullScaleAccelerometer.addItem(s, userData=v)

        thresholds = [("низкая", 2), ("средняя", 6), ("высокая", 9)]
        for text, thr in thresholds:
            self.comboBoxActivityThreshold.addItem(text, thr)

        self.pushButtonOk.clicked.connect(self.on_ok_clicked)
        self.pushButtonCancel.clicked.connect(self.close)
        # self.comboBoxModeSampleRate.currentIndexChanged.connect(self.on_mode_changed)

        self.checkBoxExg.checkStateChanged.connect(self.on_exg_clicked)
        self.checkBoxAcceleration.checkStateChanged.connect(self.on_acc_clicked)
        self.checkBoxFreefall.stateChanged.connect(self.on_event_state_changed)
        self.checkBoxActivity.stateChanged.connect(self.on_event_state_changed)
        self.checkBoxOrientation.stateChanged.connect(self.on_event_state_changed)

        for label in [self.labelInfoActivity, self.labelInfoFreefall,
                      self.labelInfoOrientation, self.labelInfoTemperature]:
            label.setAlignment(Qt.AlignCenter)
            label.setFixedSize(20, 20)
            label.setStyleSheet(""" QLabel { background-color: #0078D4; color: white; border-radius: 10px; font-weight: bold; padding: 2px; }
                                    QLabel:hover { background-color: #106EBE; } """)
        self.show_device_info()
        self.setup_ui_from_firmware()
        self.set_default_settings()

    def on_exg_clicked(self, state):
        """ обработка выбора съема exg """
        if state is Qt.CheckState.Unchecked:
            self.comboBoxModeSampleRate.setEnabled(False)

        elif state is Qt.CheckState.Checked:
            self.comboBoxModeSampleRate.setEnabled(True)

    def on_acc_clicked(self, state):
        """ обработка выбора съема акселерометра """
        if state is Qt.CheckState.Unchecked:
            self.comboBoxFullScaleAccelerometer.setEnabled(False)
            self.groupBoxEnabledEvents.setEnabled(True)

        elif state is Qt.CheckState.Checked:
            self.comboBoxFullScaleAccelerometer.setEnabled(True)
            self.groupBoxEnabledEvents.setEnabled(False)

    def on_event_state_changed(self):
        """ обработка смены состояния событий """
        if (
                self.checkBoxOrientation.isChecked()
                or self.checkBoxActivity.isChecked()
                or self.checkBoxFreefall.isChecked()
        ):
            self.checkBoxAcceleration.setEnabled(False)
            self.comboBoxActivityThreshold.setEnabled(True)
        else:
            self.checkBoxAcceleration.setEnabled(True)
            self.comboBoxActivityThreshold.setEnabled(False)

    def disable_eeg_items(self):
        """Отключает все пункты с типом сигнала EEG в комбобоксе"""
        for i in range(self.comboBoxModeSampleRate.count()):
            item_data = self.comboBoxModeSampleRate.itemData(i)
            if item_data and item_data[0] == TypeSignal.EEG:
                self.comboBoxModeSampleRate.model().item(i, 0).setEnabled(False)

    def find_index_by_mode_and_rate(self, mode, rate):
        """ вспомогательная функция """
        for i in range(self.comboBoxModeSampleRate.count()):
            item_mode, item_rate = self.comboBoxModeSampleRate.itemData(i)
            if item_mode == mode and item_rate == rate:
                return i
        return -1

    def set_default_settings(self):
        """ установка настроек установленных в inRat """
        if self._device.enabled_channels & EnabledChannels.ECG:
            self.checkBoxExg.setChecked(True)
            index = self.find_index_by_mode_and_rate(mode=self._device.mode, rate=self._device.sample_rate)
            self.comboBoxModeSampleRate.setCurrentIndex(index)

        # установить режим съема для inRat с новой версией firmware
        if self._device.firmware == FIRMWARE_V1:
            if (
                    self._device.enabled_channels & EnabledChannels.ACC_X and
                    self._device.enabled_channels & EnabledChannels.ACC_Y and
                    self._device.enabled_channels & EnabledChannels.ACC_Z
            ):
                self.checkBoxAcceleration.setChecked(True)

        # установка порога активности
        value = self._device.activity_threshold
        idx = self.comboBoxActivityThreshold.findData(value)
        if idx != -1:
            self.comboBoxActivityThreshold.setCurrentIndex(idx)

        # установка событий
        if bool(self._device.enabled_events & EventType.TEMP):
            self.checkBoxTemp.setChecked(True)
        if bool(self._device.enabled_events & EventType.ACTIVITY):
            self.checkBoxActivity.setChecked(True)
        if bool(self._device.enabled_events & EventType.ORIENTATION):
            self.checkBoxOrientation.setChecked(True)
        if bool(self._device.enabled_events & EventType.FREEFALL):
            self.checkBoxFreefall.setChecked(True)

    def setup_ui_from_firmware(self):
        # деактивация неподдерживаемых настроек
        if self._device.firmware == FIRMWARE_V0:
            self.checkBoxAcceleration.hide()
            self.comboBoxFullScaleAccelerometer.hide()
            self.disable_eeg_items()

    def show_device_info(self):
        """ показать информацию об устройстве """
        self.labelDeviceValue.setText(f"{self._device.name}")
        self.labelSnValue.setText(f"{self._device.serial}")
        self.labelModelValue.setText(f"{self._device.model}")
        self.labelFirmwareValue.setText(f"{self._device.firmware}")
        self.labelHardwareValue.setText(f"{self._device.hardware}")

    def get_enabled_events(self) -> int:
        """ получить активированные события """
        enabled_events = EventType.NONE
        if self.checkBoxTemp.isChecked():
            enabled_events |= EventType.TEMP
        if self.checkBoxActivity.isChecked():
            enabled_events |= EventType.ACTIVITY
        if self.checkBoxOrientation.isChecked():
            enabled_events |= EventType.ORIENTATION
        if self.checkBoxFreefall.isChecked():
            enabled_events |= EventType.FREEFALL
        return enabled_events

    def on_ok_clicked(self):
        # установка режима регистрации и частоты
        mode, sample_rate = self.comboBoxModeSampleRate.currentData()
        self._device.mode = mode
        self._device.sample_rate = sample_rate

        # установка масштаба акселерометра
        scale = self.comboBoxFullScaleAccelerometer.currentData()
        self._device.full_scale_accelerometer = scale

        # активация каналов
        enabled_channels = EnabledChannels.NONE
        if self.checkBoxExg.isChecked():
            enabled_channels |= EnabledChannels.ECG
            self.signal_ecg_emg.emit(True)
        else:
            self.signal_acc.emit(False)

        if self.checkBoxAcceleration.isChecked():
            enabled_channels |= EnabledChannels.ACC_X | EnabledChannels.ACC_Y | EnabledChannels.ACC_Z
            self.signal_acc.emit(True)
        else:
            self.signal_acc.emit(False)
        self._device.enabled_channels = enabled_channels

        # установка порога активности
        thr = self.comboBoxActivityThreshold.currentData()
        self._device.activity_threshold = thr

        # установка активированных событий
        enabled_events = self.get_enabled_events()
        self._device.enabled_events = enabled_events

        self.close()
