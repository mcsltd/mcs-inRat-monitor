from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog

from device.enums import EventType, Mode, EnabledChannels
from device.inrat import InRat
from resources.dlg_inrat_config import Ui_DlgDeviceConfig


class DlgConfigDevice(QDialog, Ui_DlgDeviceConfig):

    def __init__(self, device: InRat, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)

        self._device = device

        mode = [("ЭКГ", Mode.ECG), ("ЭЭГ", Mode.EEG)]
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
        if self.comboBoxMode.itemData(index) is Mode.ECG:
            sample_rates = [500, 1000, 2000]
        if self.comboBoxMode.itemData(index) is Mode.EEG:
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
        self._device.sampling_rate = sample_rate

        # установка масштаба акселерометра
        # scale = self.comboBoxFullScaleAccelerometer.currentData()
        # self.device.full_scale_accelerometer = scale

        # активация каналов
        enabled_channels = EnabledChannels.NONE
        if self.checkBoxSignal.isChecked():
            enabled_channels |= EnabledChannels.ECG
        if self.checkBoxAcceleration.isChecked():
            enabled_channels |= EnabledChannels.ACC_X | EnabledChannels.ACC_Y | EnabledChannels.ACC_Z
        self._device.enabled_channels = enabled_channels

        # установка порога активности
        thr = self.comboBoxActivityThreshold.currentData()
        self._device.activity_threshold = thr

        # установка активированных событий
        enabled_events = self.get_enabled_events()
        self._device.enabled_events = enabled_events

        self.close()