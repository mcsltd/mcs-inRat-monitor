import logging

from PySide6.QtCore import QObject
from PySide6.QtMultimedia import (
    QCamera, QCameraDevice, QMediaCaptureSession, QMediaDevices
)

from camera.config_pane import FrmConfigCamera
from camera.video_pane import CameraVideoPane

logger = logging.getLogger(__name__)

class Camera(QObject):
    """ Класс для подключения и управления камерой """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._camera: QCameraDevice | None = None
        self._qcamera: QCamera | None = None
        self._session: QMediaCaptureSession | None = None

        # панель вывода видео (добавляется в main_splitter окна)
        self._output_pane = CameraVideoPane()
        self._output_pane.closed.connect(self.close)
        self._output_pane.setVisible(False)

        self._config_pane = FrmConfigCamera()

    def process_update(self, camera_name: str | None = None):
        """ включение/отключение камеры по сигналу из настроек """
        if not camera_name:
            self.close()
            return
        self.set_camera_name(camera_name)

    @property
    def config_pane(self):
        return self._config_pane

    @property
    def is_enabled(self) -> bool:
        """ признак включенной камеры """
        return self._camera is not None

    @property
    def camera_name(self) -> str | None:
        """ название текущей камеры """
        return self._camera.description() if self._camera else None

    @property
    def output_pane(self) -> CameraVideoPane:
        """ панель отображения видео с камеры """
        return self._output_pane

    def set_camera_name(self, name: str | None):
        """ установка выбранной камеры по названию """
        camera = None
        if name:
            camera = next(
                (cam for cam in QMediaDevices.videoInputs()
                 if cam.description() == name),
                None
            )
        self.set_camera(camera)

    def set_camera(self, device: QCameraDevice | None):
        """ запуск вывода видео с выбранной камерой """
        self.stop_camera()

        if device is None:
            self._output_pane.setVisible(False)
            return

        self._camera = device
        self._qcamera = QCamera(device)
        self._session = QMediaCaptureSession()
        self._session.setVideoOutput(self._output_pane.video_widget)
        self._session.setCamera(self._qcamera)
        self._qcamera.errorOccurred.connect(self._on_error)
        self._qcamera.start()

        self._output_pane.set_title(device.description())
        self._output_pane.setVisible(True)
        logger.debug(f"Запущена камера: {device.description()}")

    def stop_camera(self):
        """ остановка вывода видео """
        if self._qcamera is not None:
            try:
                self._qcamera.stop()
            except Exception as err:
                logger.error(f"{self.__class__}: ошибка остановки камеры - {err}")
            self._qcamera = None

        if self._session is not None:
            self._session.setCamera(None)
            self._session = None

        self._camera = None

    def close(self):
        """ закрытие панели камеры по крестику """
        logger.debug(f"{self.__class__}: закрытие панели камеры")
        self.stop_camera()
        self._output_pane.setVisible(False)

    def _on_error(self, error, error_string):
        """ обработка ошибки камеры """
        logger.error(f"{self.__class__}: ошибка камеры - {error_string}")
        self._output_pane.set_title(f"Ошибка: {error_string}")
        self._output_pane.setVisible(True)
