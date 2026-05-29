from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog

from device.enums import EventType, Mode
from resources.dlg_inrat_config import Ui_DlgDeviceConfig


class DlgConfigDevice(QDialog, Ui_DlgDeviceConfig):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)

        mode = [("ЭКГ", Mode.ECG), ("ЭЭГ", Mode.EEG)]
        for t, v in mode:
            self.comboBoxMode.addItem(t, userData=v)

        sample_rate = [500, 1000, 2000]
        for sr in sample_rate:
            self.comboBoxSampleRate.addItem(str(sr), userData=sr)

        # scale = [("±2", 2), ("±4", 4), ("±8", 8), ("±16", 16)]
        # for s, v in scale:
        #     self.comboBoxFullScaleAccelerometer.addItem(s, userData=v)
        self.comboBoxFullScaleAccelerometer.hide()
        self.labelFullScaleAccelerometer.hide()

        thresholds = [("низкий", 2), ("средний", 6), ("высокий", 9)]
        for text, thr in thresholds:
            self.comboBoxActivityThreshold.addItem(text, thr)

        # self.pushButtonOk.clicked.connect(self.on_ok_clicked)
        self.pushButtonCancel.clicked.connect(self.close)

        for label in [self.labelInfoActivity, self.labelInfoFreefall,
                      self.labelInfoOrientation, self.labelInfoTemperature]:
            label.setAlignment(Qt.AlignCenter)
            label.setFixedSize(20, 20)
            label.setStyleSheet("""
                    QLabel {
                        background-color: #0078D4; color: white; border-radius: 10px; font-weight: bold; padding: 2px;
                    }
                    QLabel:hover { background-color: #106EBE; }
                    """)

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

    # def on_ok_clicked(self):
    #     # установка частоты
    #     sample_rate = self.comboBoxSampleRate.currentData()
    #     self.device.sampling_rate = sample_rate
    #     # установка масштаба акселерометра
    #     # scale = self.comboBoxFullScaleAccelerometer.currentData()
    #     # self.device.full_scale_accelerometer = scale
    #     # установка порога активности
    #     thr = self.comboBoxActivityThreshold.currentData()
    #     self.device.activity_threshold = thr
    #     # установка активированных событий
    #     enabled_events = self.get_enabled_events()
    #     self.device.enabled_events = enabled_events
    #
    #     self.close()