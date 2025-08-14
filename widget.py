from PySide6.QtGui import Qt, QFont
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QProgressBar, QSizePolicy


class WaitingDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Waiting for connection")
        self.setWindowModality(Qt.WindowModality.ApplicationModal)

        font = QFont()
        font.setPointSize(12)

        self.setFixedSize(300, 150)
        layout = QVBoxLayout()

        self.label = QLabel("Please wait for the device to connect...")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setFont(font)

        self.progress = QProgressBar()
        self.progress.setRange(0, 0)

        self.progress.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        layout.setContentsMargins(10, 10, 10, 10)  # Добавляем отступы

        layout.addWidget(self.label)
        layout.addWidget(self.progress)

        self.setLayout(layout)
