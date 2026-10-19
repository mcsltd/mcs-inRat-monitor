from PySide6.QtGui import Qt, QFont
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QProgressBar, QSizePolicy
from PySide6.QtWidgets import QStyleFactory

class WaitingDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ожидание открытия")
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.setFixedSize(350, 150)

        layout = QVBoxLayout()
        layout.setSpacing(10)  # Добавляем отступы между элементами
        layout.setContentsMargins(20, 20, 20, 20)  # Устанавливаем отступы от краев

        font = QFont()
        font.setPointSize(12)
        font.setFamily("Arial")  # Явно указываем шрифт

        self.label = QLabel("Пожалуйста, подождите, пока устройство откроется...")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setFont(font)

        # перенос слов для длинного текста
        self.label.setWordWrap(True)

        # минимальная высота для метки
        self.label.setMinimumHeight(50)

        self.label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.MinimumExpanding)

        self.progress = QProgressBar()
        self.progress.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.progress.setRange(0, 0)
        self.progress.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.progress.setFixedHeight(25)  # Фиксированная высота для прогресс-бара

        layout.addWidget(self.label, stretch=1)  # stretch позволяет метке занимать больше места
        layout.addWidget(self.progress, stretch=0)  # прогресс-бар без растяжения

        self.setLayout(layout)
        self.progress.setStyle(QStyleFactory.create("Fusion"))
