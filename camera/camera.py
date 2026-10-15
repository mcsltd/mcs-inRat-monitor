import logging

from PySide6.QtCore import QObject

from PySide6.QtMultimedia import QCameraDevice
from PySide6.QtWidgets import QFrame

from camera.dlg_enabled_cameras import DlgEnabledCameras
from camera.res.frm_control_camera import Ui_FrmAddCamera

logger = logging.getLogger(__name__)

class FrmControlCamera(QFrame, Ui_FrmAddCamera):
    """ фрейм для управления камерой """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)



class Camera(QObject):
    """ Класс для подключения и управления камерой """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._camera: QCameraDevice | None = None

        self._control_pane = FrmControlCamera()
        self._config_pane = ...
        self._output_pane = ...

        self._control_pane.pushButtonAdd.clicked.connect(self._on_add_clicked)

    @property
    def control_pane(self):
        return self._control_pane

    def _set_camera(self, camera: QCameraDevice):
        """ установка выбранной камеры """
        self._camera = camera
        logger.debug(f"Добавлена камера: {self._camera}")

    def _on_add_clicked(self):
        """ обработка нажатия кнопки добавить камеру """
        dlg = DlgEnabledCameras()
        dlg.signal_select.connect(self._set_camera)
        dlg.exec()