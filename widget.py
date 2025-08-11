from PySide6.QtGui import Qt
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QProgressBar

class WaitingDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Waiting for connection")
        self.setWindowModality(Qt.WindowModality.ApplicationModal)

        self.setFixedSize(300, 150)
        layout = QVBoxLayout()

        self.label = QLabel("Please wait for the device to connect...")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.progress = QProgressBar()
        self.progress.setRange(0, 0)

        layout.addWidget(self.label)
        layout.addWidget(self.progress)

        self.setLayout(layout)
