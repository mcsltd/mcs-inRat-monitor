import logging

from PySide6.QtCore import Qt, Signal
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtWidgets import (
    QFrame, QHBoxLayout, QLabel, QSizePolicy, QToolButton, QVBoxLayout
)

logger = logging.getLogger(__name__)

# минимальная ширина панели с видео (при ресайзе сплиттером)
MIN_WIDTH = 240


class CameraVideoPane(QFrame):
    """ панель отображения видео с выбранной камерой """

    closed = Signal()  # закрытие панели по крестику

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setObjectName("CameraVideoPane")
        self.setStyleSheet(
            """
            CameraVideoPane {
                background-color: rgb(64, 64, 64);
                border: 1px solid rgb(90, 90, 90);
            }
            QLabel {
                color: white;
                background: transparent;
            }
            QToolButton {
                background: transparent;
                border: none;
                color: white;
                font-size: 14pt;
                font-weight: bold;
            }
            QToolButton:hover {
                color: rgb(255, 80, 80);
            }
            """
        )
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        self.setMinimumWidth(MIN_WIDTH)

        # шапка: название камеры и кнопка закрытия
        self._label_title = QLabel("Камера")
        self._label_title.setWordWrap(False)

        self._button_close = QToolButton()
        self._button_close.setText("✕")
        self._button_close.setAutoRaise(True)
        self._button_close.setToolTip("Закрыть окно камеры")
        self._button_close.setFixedSize(26, 26)
        self._button_close.clicked.connect(self._on_close_clicked)

        header = QHBoxLayout()
        header.setContentsMargins(6, 2, 2, 2)
        header.setSpacing(4)
        header.addWidget(self._label_title, 1)
        header.addWidget(self._button_close, 0, Qt.AlignmentFlag.AlignTop)

        # область вывода видео
        self._video = QVideoWidget()
        self._video.setAspectRatioMode(Qt.AspectRatioMode.KeepAspectRatio)
        self._video.setMinimumSize(160, 120)
        self._video.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(2, 2, 2, 2)
        layout.setSpacing(2)
        layout.addLayout(header)
        layout.addWidget(self._video, 1)

    def _on_close_clicked(self):
        """ обработка нажатия крестика """
        self.closed.emit()

    @property
    def video_widget(self) -> QVideoWidget:
        """ виджет вывода видео """
        return self._video

    @property
    def close_button(self) -> QToolButton:
        """ кнопка закрытия панели """
        return self._button_close

    def set_title(self, text: str):
        """ установка текста в шапке панели """
        self._label_title.setText(text)
