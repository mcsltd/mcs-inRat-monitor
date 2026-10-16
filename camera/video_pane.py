import logging

from PySide6.QtCore import QPoint, Qt, Signal
from PySide6.QtGui import QColor, QMouseEvent, QPainter, QPen
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtWidgets import (
    QFrame, QHBoxLayout, QLabel, QSizePolicy, QToolButton, QVBoxLayout, QWidget
)

logger = logging.getLogger(__name__)

# размеры панели с видео
DEFAULT_WIDTH = 480
MIN_WIDTH = 240


class _ResizeHandle(QWidget):
    """ уголок изменения ширины панели (перетаскивание по горизонтали) """

    def __init__(self, target: "CameraVideoPane", parent=None):
        super().__init__(parent)
        self._target = target
        self._start_pos = QPoint()
        self._start_width = 0
        self._dragging = False

        self.setFixedSize(16, 16)
        self.setCursor(Qt.CursorShape.SizeHorCursor)
        self.setToolTip("Изменить ширину")
        self.setAttribute(Qt.WidgetAttribute.WA_NoMousePropagation, True)

    def mousePressEvent(self, event: QMouseEvent):
        """ начало перетаскивания """
        if event.button() != Qt.MouseButton.LeftButton:
            return
        self._dragging = True
        self._start_pos = event.globalPosition().toPoint()
        self._start_width = self._target.width()
        event.accept()

    def mouseMoveEvent(self, event: QMouseEvent):
        """ изменение ширины панели при перетаскивании """
        if not self._dragging:
            return
        delta = event.globalPosition().toPoint().x() - self._start_pos.x()
        self._target.set_panel_width(self._start_width + delta)
        event.accept()

    def mouseReleaseEvent(self, event: QMouseEvent):
        """ окончание перетаскивания """
        if event.button() == Qt.MouseButton.LeftButton:
            self._dragging = False
            event.accept()

    def paintEvent(self, _):
        """ отрисовка точек уголка """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        painter.setPen(QPen(QColor(255, 255, 255, 160), 2))
        for x, y in ((13, 13), (9, 9), (5, 5)):
            painter.drawPoint(x, y)


class CameraVideoPane(QFrame):
    """ панель отображения видео с выбранной камеры """

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
        self.setFixedWidth(DEFAULT_WIDTH)

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

        # уголок изменения ширины поверх видео в правом нижнем углу
        self._handle = _ResizeHandle(self)

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

    def set_panel_width(self, width: int):
        """ фиксация ширины панели с ограничениями min/max """
        window_width = self.window().width() if self.window() is not None else 0
        max_width = max(MIN_WIDTH, window_width // 2)
        value = max(MIN_WIDTH, min(int(width), max_width))

        if value != self.width():
            self.setFixedWidth(value)

    def resizeEvent(self, event):
        """ позиционирование уголка в правом нижнем углу """
        super().resizeEvent(event)
        margin = 3
        self._handle.move(
            self.width() - self._handle.width() - margin,
            self.height() - self._handle.height() - margin,
        )
