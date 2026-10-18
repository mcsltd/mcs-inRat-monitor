from PySide6.QtCore import Signal
from PySide6.QtWidgets import QFrame
from PySide6.QtMultimedia import QMediaDevices

from camera.res.frm_config_camera import Ui_FrmConfigCamera
# пункт по умолчанию в списке камер
UNDEFINED_CAMERA = "Не определено"


class FrmConfigCamera(QFrame, Ui_FrmConfigCamera):
    signal_apply = Signal(object)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)

        self._setup_combobox_switch()
        self._populate_cameras()

        self.set_default()

        self.comboBoxSwitch.currentIndexChanged.connect(self._on_switch_changed)
        self.pushButtonOk.clicked.connect(self._on_ok_clicked)

    def _setup_combobox_switch(self):
        data = [("Отключена", False), ("Включена", True)]
        for text, value in data:
            self.comboBoxSwitch.addItem(text, userData=value)

    def _populate_cameras(self):
        """ наполнение списка доступных камер """
        self.comboBoxCameras.clear()
        self.comboBoxCameras.addItem(UNDEFINED_CAMERA, None)
        for cam in QMediaDevices.videoInputs():
            self.comboBoxCameras.addItem(cam.description(), cam.description())

    def set_default(self, enabled: bool = False, camera_name: str | None = None):
        """ установка значений по умолчанию (по состоянию камеры) """
        self._populate_cameras()
        self.comboBoxSwitch.setCurrentIndex(self.comboBoxSwitch.findData(enabled))
        if camera_name:
            idx = self.comboBoxCameras.findData(camera_name)
            if idx >= 0:
                self.comboBoxCameras.setCurrentIndex(idx)
        elif enabled and self.comboBoxCameras.count() > 1:
            self.comboBoxCameras.setCurrentIndex(1)
        self.comboBoxCameras.setEnabled(enabled)

    def _on_switch_changed(self, idx):
        """ включение/отключение списка камер """
        enabled = bool(self.comboBoxSwitch.currentData())
        self.comboBoxCameras.setEnabled(enabled)

    def _get_camera_name(self) -> str | None:
        if not bool(self.comboBoxSwitch.currentData()):
            return None
        data = self.comboBoxCameras.currentData()
        if data is None:
            return None
        return data

    def _on_ok_clicked(self):
        """ обработка нажатия кнопки применить """
        camera_name = self._get_camera_name()
        self.signal_apply.emit(camera_name)