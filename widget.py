from PySide6.QtGui import Qt, QFont
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QProgressBar, QSizePolicy


class WaitingDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ожидание открытия устройства")
        self.setWindowModality(Qt.WindowModality.ApplicationModal)

        # Установка политики размера, чтобы диалог мог адаптироваться
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        # Позволяем диалогу изменять размер при необходимости
        self.setFixedSize(350, 150)  # или используйте self.resize() и setMinimumSize

        layout = QVBoxLayout()
        layout.setSpacing(10)  # Добавляем отступы между элементами
        layout.setContentsMargins(20, 20, 20, 20)  # Устанавливаем отступы от краев

        # Настройка шрифта
        font = QFont()
        font.setPointSize(12)
        font.setFamily("Arial")  # Явно указываем шрифт

        # Настройка QLabel для правильного отображения текста
        self.label = QLabel("Пожалуйста, подождите, пока устройство откроется...")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setFont(font)

        # ВАЖНО: разрешить перенос слов для длинного текста
        self.label.setWordWrap(True)

        # Настройка минимальной высоты для метки
        self.label.setMinimumHeight(50)

        # Использовать политику размера, позволяющую метке расширяться
        self.label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.MinimumExpanding)

        # Прогресс бар
        self.progress = QProgressBar()
        self.progress.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.progress.setRange(0, 0)
        self.progress.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.progress.setFixedHeight(25)  # Фиксированная высота для прогресс-бара

        # Добавляем все в layout
        layout.addWidget(self.label, stretch=1)  # stretch позволяет метке занимать больше места
        layout.addWidget(self.progress, stretch=0)  # прогресс-бар без растяжения

        self.setLayout(layout)
