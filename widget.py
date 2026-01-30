from PySide6.QtGui import Qt, QFont, QIcon
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QProgressBar, QSizePolicy


class WaitingDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Waiting for connection")
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.setWindowIcon(QIcon("resources/iconMCS.ico"))

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

# from PySide6.QtGui import Qt, QFont, QIcon
# from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QProgressBar, QSizePolicy, QPushButton, QHBoxLayout, \
#     QSpacerItem, QApplication
# class DlgConnection(QDialog):
#
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.setWindowIcon(QIcon("resources/iconMCS.ico"))
#
#         self.setWindowTitle("Соединение")
#         self.setWindowModality(Qt.WindowModality.ApplicationModal)
#
#         # self.pushBtnCancel = QPushButton("Отменить", self)
#         # self.pushBtnCancel.setEnabled(True)
#         # self.pushBtnRetry = QPushButton("Повторить", self)
#         # self.pushBtnRetry.setEnabled(False)
#
#         font = QFont()
#         font.setPointSize(12)
#
#         self.setFixedSize(300, 150)
#         layout = QVBoxLayout()
#         h_layout = QHBoxLayout()
#
#         self.label = QLabel("Пожалуйста, дождитесь когда устройство откроется")
#         self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         self.label.setFont(font)
#
#         layout.addWidget(self.label)
#         # h_layout.addWidget(self.pushBtnRetry)
#         # h_layout.addWidget(self.pushBtnCancel)
#
#         layout.addLayout(h_layout)
#         self.setLayout(layout)
#
#         # self.pushBtnCancel.clicked.connect(self.close)
#
# if __name__ == "__main__":
#     app = QApplication([])
#
#     dlg = DlgConnection()
#     dlg.show()
#
#     app.exec()