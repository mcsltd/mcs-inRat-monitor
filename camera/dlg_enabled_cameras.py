from PySide6.QtCore import Signal
from PySide6.QtMultimedia import QMediaDevices
from PySide6.QtWidgets import QDialog

from camera.res.dlg_enable_cameras import Ui_DlgCameras


class DlgEnabledCameras(QDialog, Ui_DlgCameras):
    """ Диалоговое окно для вывода и выбора доступных камер"""
    signal_select = Signal(object)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)

        self._enable_cameras = {}

        self.pushButtonOpen.setEnabled(False)
        self.pushButtonOpen.clicked.connect(self._on_open_clicked)
        self.pushButtonReset.clicked.connect(self._on_reset_clicked)
        self.listWidgetFoundCameras.currentRowChanged.connect(self._on_current_row_changed)

        self._set_cameras()

    def _set_cameras(self):
        """ отображение доступных камер """
        self._enable_cameras.clear()
        self.listWidgetFoundCameras.clear()

        cameras = QMediaDevices.videoInputs()
        if not cameras:
            # todo add messagebox - камер не обнаружено
            return
        for camera in cameras:
            self.listWidgetFoundCameras.addItem(camera.description())
            self._enable_cameras[camera.description()] = camera

    def _on_current_row_changed(self, row: int):
        """ блокировка кнопки подключения при пустом выборе """
        self.pushButtonOpen.setEnabled(row >= 0)

    def _on_open_clicked(self):
        """ обработка кнопки подключения устройства """
        item = self.listWidgetFoundCameras.currentItem()
        if item is None:
            return
        device_name = item.text()
        self.signal_select.emit(self._enable_cameras[device_name])
        self.close()

    def _on_reset_clicked(self):
        """ обработка кнопки подключения устройства """
        self._enable_cameras.clear()
        self.listWidgetFoundCameras.clear()

    def closeEvent(self, arg__1, /):
        """ обработка закрытия окна """
        pass
