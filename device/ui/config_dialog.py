from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QDialog

from device.enums import EventType, Mode, EnabledChannels, TypeSignal
from device.inrat import inRat, FIRMWARE_V0, FIRMWARE_V1
from resources.dlg_inrat_config import Ui_DlgDeviceConfig


class DlgConfigDevice(QDialog, Ui_DlgDeviceConfig):

    signal_acc = Signal(bool)
    signal_ecg_emg = Signal(bool)

    def __init__(self, device: inRat, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)

        self._device = device

        mode = [("ЭКГ", TypeSignal.ECG), ("ЭЭГ", TypeSignal.EEG)]
        for t, v in mode:
            self.comboBoxMode.addItem(t, userData=v)
        self.on_mode_changed(index=0)

        # scale = [("±2", 2), ("±4", 4), ("±8", 8), ("±16", 16)]
        # for s, v in scale:
        #     self.comboBoxFullScaleAccelerometer.addItem(s, userData=v)
        self.comboBoxFullScaleAccelerometer.hide()
        self.labelFullScaleAccelerometer.hide()

        thresholds = [("низкий", 2), ("средний", 6), ("высокий", 9)]
        for text, thr in thresholds:
            self.comboBoxActivityThreshold.addItem(text, thr)

        self.pushButtonOk.clicked.connect(self.on_ok_clicked)
        self.pushButtonCancel.clicked.connect(self.close)
        self.comboBoxMode.currentIndexChanged.connect(self.on_mode_changed)

        for label in [self.labelInfoActivity, self.labelInfoFreefall,
                      self.labelInfoOrientation, self.labelInfoTemperature]:
            label.setAlignment(Qt.AlignCenter)
            label.setFixedSize(20, 20)
            label.setStyleSheet(""" QLabel { background-color: #0078D4; color: white; border-radius: 10px; font-weight: bold; padding: 2px; }
                                    QLabel:hover { background-color: #106EBE; } """)
        self.show_device_info()
        self.setup_ui_from_firmware()
        self.set_default_settings()

    def set_default_settings(self):
        """ установка настроек установленных в inRat """
        if self._device.enabled_channels & EnabledChannels.ECG:
            self.checkBoxSignal.setChecked(True)

        # установить режим съема для inRat с новой версией firmware
        if self._device.firmware == FIRMWARE_V1:
            index = self.comboBoxMode.findData(self._device.mode)
            self.comboBoxMode.setCurrentIndex(index) # установка выбранного режима съема
            self.on_mode_changed(index)
            if (
                    self._device.enabled_channels & EnabledChannels.ACC_X and
                    self._device.enabled_channels & EnabledChannels.ACC_Y and
                    self._device.enabled_channels & EnabledChannels.ACC_Z
            ):
                self.checkBoxAcceleration.setChecked(True)

        # установка частоты
        sampling_rate = str(self._device.sample_rate)
        idx = self.comboBoxSampleRate.findText(sampling_rate)
        self.comboBoxSampleRate.setCurrentIndex(idx)

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
            self.labelMode.hide()
            self.comboBoxMode.hide()
            self.checkBoxAcceleration.hide()


    def show_device_info(self):
        """ показать информацию об устройстве """
        self.labelDeviceValue.setText(f"{self._device.name}")
        self.labelSnValue.setText(f"{self._device.serial}")
        self.labelModelValue.setText(f"{self._device.model}")
        self.labelFirmwareValue.setText(f"{self._device.firmware}")
        self.labelHardwareValue.setText(f"{self._device.hardware}")

    def on_mode_changed(self, index):
        """ обработка выбор режима съема сигнала """
        sample_rates = []
        if self.comboBoxMode.itemData(index) is TypeSignal.ECG:
            sample_rates = [500, 1000, 2000]
        if self.comboBoxMode.itemData(index) is TypeSignal.EEG:
            sample_rates = [250, 500]
        self.comboBoxSampleRate.clear()
        for sr in sample_rates:
            self.comboBoxSampleRate.addItem(str(sr), userData=sr)
        self.checkBoxSignal.setText(self.comboBoxMode.currentText())

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
        # установка режима регистрации
        self._device.mode = self.comboBoxMode.currentData()

        # установка частоты
        sample_rate = self.comboBoxSampleRate.currentData()
        self._device.sample_rate = sample_rate

        # установка масштаба акселерометра
        # scale = self.comboBoxFullScaleAccelerometer.currentData()
        # self.device.full_scale_accelerometer = scale

        # активация каналов
        enabled_channels = EnabledChannels.NONE
        if self.checkBoxSignal.isChecked():
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