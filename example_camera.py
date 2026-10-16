import sys
from PySide6.QtCore import Qt, QUrl, Slot
from PySide6.QtMultimedia import QCamera, QMediaCaptureSession, QMediaDevices, QVideoSink, QVideoFrame
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QComboBox, QLabel, QMessageBox
)


class CameraWidget(QWidget):
    """Виджет для отображения видео с камеры ноутбука."""

    def __init__(self, parent=None):
        super().__init__(parent)

        # --- UI ---
        self.video_widget = QVideoWidget()
        self.video_widget.setMinimumSize(640, 480)

        self.camera_combo = QComboBox()
        self.start_btn = QPushButton("Старт")
        self.stop_btn = QPushButton("Стоп")
        self.stop_btn.setEnabled(False)
        self.status_label = QLabel("Готово")

        controls = QHBoxLayout()
        controls.addWidget(QLabel("Камера:"))
        controls.addWidget(self.camera_combo, 1)
        controls.addWidget(self.start_btn)
        controls.addWidget(self.stop_btn)

        layout = QVBoxLayout(self)
        layout.addWidget(self.video_widget, 1)
        layout.addLayout(controls)
        layout.addWidget(self.status_label)

        # --- Мультимедиа ---
        self._capture_session = QMediaCaptureSession()
        self._capture_session.setVideoOutput(self.video_widget)

        self._camera: QCamera | None = None

        # Сигналы
        self.start_btn.clicked.connect(self.start_camera)
        self.stop_btn.clicked.connect(self.stop_camera)

        self._populate_cameras()

    # ---------- Внутреннее ----------
    def _populate_cameras(self):
        """Заполнить выпадающий список доступными камерами."""
        self.camera_combo.clear()
        cameras = QMediaDevices.videoInputs()
        if not cameras:
            self.camera_combo.addItem("Камеры не найдены")
            self.start_btn.setEnabled(False)
            return
        for cam in cameras:
            self.camera_combo.addItem(cam.description(), cam)

    # ---------- Публичные слоты ----------
    @Slot()
    def start_camera(self):
        if self._camera is not None:
            return

        cam_info = self.camera_combo.currentData()
        if cam_info is None:
            QMessageBox.warning(self, "Ошибка", "Камера недоступна")
            return

        self._camera = QCamera(cam_info)
        self._capture_session.setCamera(self._camera)

        self._camera.errorOccurred.connect(self._on_error)
        self._camera.activeChanged.connect(self._on_active_changed)

        self._camera.start()

        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.camera_combo.setEnabled(False)
        self.status_label.setText("Камера запущена")

    @Slot()
    def stop_camera(self):
        if self._camera is None:
            return
        self._camera.stop()
        self._camera = None
        self._capture_session.setCamera(None)

        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.camera_combo.setEnabled(True)
        self.status_label.setText("Камера остановлена")

    # ---------- Обработчики ----------
    @Slot(QCamera.Error, str)
    def _on_error(self, error, error_string):
        self.status_label.setText(f"Ошибка: {error_string}")
        QMessageBox.critical(self, "Ошибка камеры", error_string)

    @Slot(bool)
    def _on_active_changed(self, active: bool):
        self.status_label.setText("Камера активна" if active else "Камера неактивна")

    # ---------- Корректное завершение ----------
    def closeEvent(self, event):
        self.stop_camera()
        super().closeEvent(event)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Видео с камеры ноутбука")
        self.resize(800, 600)
        self.camera = CameraWidget()
        layout = QVBoxLayout(self)
        layout.addWidget(self.camera)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())