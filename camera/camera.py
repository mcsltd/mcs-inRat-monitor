import logging

from PySide6.QtCore import QObject, QUrl
from PySide6.QtMultimedia import (
    QCamera, QCameraDevice, QMediaCaptureSession, QMediaDevices, QMediaRecorder,
    QMediaFormat,
)

from camera.config_pane import FrmConfigCamera
from camera.video_pane import CameraVideoPane

logger = logging.getLogger(__name__)

# индикатор записи в шапке панели
RECORD_INDICATOR = "● "


class Camera(QObject):
    """ Класс для подключения и управления камерой """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._camera: QCameraDevice | None = None
        self._qcamera: QCamera | None = None
        self._session: QMediaCaptureSession | None = None
        self._recorder: QMediaRecorder | None = None

        # колбэк, возвращающий путь следующего файла записи видео
        self._video_file_provider = None
        # флаг отложенного старта записи (ролловер при остановке рекордера)
        self._pending_record = False
        self._base_title = "Камера"

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
        """ панель отображения видео с камерой """
        return self._output_pane

    @property
    def is_video_recording(self) -> bool:
        """ признак идущей записи видео """
        return (
            self._recorder is not None
            and self._recorder.recorderState() == QMediaRecorder.RecorderState.RecordingState
        )

    def set_video_file_provider(self, provider):
        """ установка колбэка, возвращающего путь следующего файла видео """
        self._video_file_provider = provider

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

        # рекордер записи видео в ту же сессию (кодек ОС, без ручной подачи кадров)
        self._recorder = QMediaRecorder(self)
        fmt = QMediaFormat()
        fmt.setFileFormat(QMediaFormat.FileFormat.MPEG4)
        fmt.setVideoCodec(QMediaFormat.VideoCodec.H264)
        self._recorder.setMediaFormat(fmt)
        self._recorder.setQuality(QMediaRecorder.Quality.HighQuality)
        self._recorder.errorOccurred.connect(self._on_recorder_error)
        self._recorder.recorderStateChanged.connect(self._on_recorder_state_changed)
        self._session.setRecorder(self._recorder)

        self._session.setCamera(self._qcamera)
        self._qcamera.errorOccurred.connect(self._on_error)
        self._qcamera.start()

        self._base_title = device.description()
        self._output_pane.set_title(self._base_title)
        self._output_pane.setVisible(True)
        logger.debug(f"Запущена камера: {device.description()}")

    def start_video_recording(self):
        """ старт записи видео в файл текущей записи сигналов """
        if not self.is_enabled or self._recorder is None:
            logger.debug(f"{self.__class__}: запись видео пропущена - камера выключена")
            return
        if self.is_video_recording:
            logger.debug(f"{self.__class__}: запись видео уже идёт")
            return

        path = self._video_file_provider() if self._video_file_provider else None
        if not path:
            logger.warning(f"{self.__class__}: запись видео пропущена - путь для файла не определён")
            return

        self._recorder.setOutputLocation(QUrl.fromLocalFile(path))
        self._recorder.record()
        self._set_recording_indicator(True)
        logger.debug(f"{self.__class__}: началась запись видео - {path}")

    def stop_video_recording(self):
        """ остановка записи видео с финализацией файла """
        self._pending_record = False
        if not self.is_video_recording:
            return
        self._recorder.stop()
        self._set_recording_indicator(False)
        logger.debug(f"{self.__class__}: остановлена запись видео")

    def rotate_video_recording(self):
        """
        переключение записи видео на новый файл (ролловер записи сигналов).

        Остановка рекордера асинхронна, поэтому новый старт выполняется
        в слоте stateChanged после фактического завершения записи.
        """
        if not self.is_video_recording:
            return
        self._pending_record = True
        self._recorder.stop()
        logger.debug(f"{self.__class__}: переключение записи видео на новый файл")

    def stop_camera(self):
        """ остановка вывода видео """
        # сначала финализируем файл записи, затем останавливаем сессию
        self.stop_video_recording()

        if self._qcamera is not None:
            try:
                self._qcamera.stop()
            except Exception as err:
                logger.error(f"{self.__class__}: ошибка остановки камеры - {err}")
            self._qcamera = None

        if self._session is not None:
            self._session.setCamera(None)
            self._session = None

        self._recorder = None
        self._camera = None

    def close(self):
        """ закрытие панели камеры по крестику """
        logger.debug(f"{self.__class__}: закрытие панели камеры")
        self.stop_camera()
        self._output_pane.setVisible(False)

    def _set_recording_indicator(self, active: bool):
        """ индикация записи в шапке панели """
        if active:
            self._output_pane.set_title(f"{RECORD_INDICATOR}{self._base_title}")
        else:
            self._output_pane.set_title(self._base_title)

    def _on_recorder_state_changed(self, state):
        """ отложенный старт после завершения предыдущего файла (ролловер) """
        if (
            state == QMediaRecorder.RecorderState.StoppedState
            and self._pending_record
            and self._recorder is not None
        ):
            self._pending_record = False
            logger.debug(f"{self.__class__}: старт записи видео после ролловера")
            self.start_video_recording()

    def _on_recorder_error(self, error, error_string):
        """ обработка ошибки записи видео """
        logger.error(f"{self.__class__}: ошибка записи видео - {error_string}")
        self._pending_record = False
        self._set_recording_indicator(False)
        self._output_pane.set_title(f"Ошибка записи: {error_string}")

    def _on_error(self, error, error_string):
        """ обработка ошибки камеры """
        logger.error(f"{self.__class__}: ошибка камеры - {error_string}")
        self._output_pane.set_title(f"Ошибка: {error_string}")
        self._output_pane.setVisible(True)
