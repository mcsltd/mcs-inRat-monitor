# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'frm_control_cameraKfMGeZ.ui'
##
## Created by: Qt User Interface Compiler version 6.12.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
    QLabel, QPushButton, QSizePolicy, QVBoxLayout,
    QWidget)
import resources.resources_rc

class Ui_FrmAddCamera(object):
    def setupUi(self, FrmAddCamera):
        if not FrmAddCamera.objectName():
            FrmAddCamera.setObjectName(u"FrmAddCamera")
        FrmAddCamera.resize(174, 131)
        self.gridLayout = QGridLayout(FrmAddCamera)
        self.gridLayout.setObjectName(u"gridLayout")
        self.line_2 = QFrame(FrmAddCamera)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)
        self.line_2.setFrameShape(QFrame.Shape.VLine)

        self.gridLayout.addWidget(self.line_2, 0, 0, 1, 1)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pushButtonAdd = QPushButton(FrmAddCamera)
        self.pushButtonAdd.setObjectName(u"pushButtonAdd")
        self.pushButtonAdd.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonAdd.sizePolicy().hasHeightForWidth())
        self.pushButtonAdd.setSizePolicy(sizePolicy)
        self.pushButtonAdd.setMaximumSize(QSize(75, 75))
        self.pushButtonAdd.setStyleSheet(u"QPushButton {\n"
"    background-color: transparent;\n"
"    border: none;\n"
"}")
        icon = QIcon()
        icon.addFile(u":/images/camera.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButtonAdd.setIcon(icon)
        self.pushButtonAdd.setIconSize(QSize(50, 50))

        self.horizontalLayout.addWidget(self.pushButtonAdd)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.labelCamera = QLabel(FrmAddCamera)
        self.labelCamera.setObjectName(u"labelCamera")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.labelCamera.sizePolicy().hasHeightForWidth())
        self.labelCamera.setSizePolicy(sizePolicy1)
        self.labelCamera.setMaximumSize(QSize(16777215, 20))
        font = QFont()
        font.setPointSize(11)
        self.labelCamera.setFont(font)
        self.labelCamera.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.labelCamera)


        self.gridLayout.addLayout(self.verticalLayout, 0, 1, 1, 1)

        self.line = QFrame(FrmAddCamera)
        self.line.setObjectName(u"line")
        self.line.setFrameShadow(QFrame.Shadow.Sunken)
        self.line.setFrameShape(QFrame.Shape.VLine)

        self.gridLayout.addWidget(self.line, 0, 2, 1, 1)


        self.retranslateUi(FrmAddCamera)

        QMetaObject.connectSlotsByName(FrmAddCamera)
    # setupUi

    def retranslateUi(self, FrmAddCamera):
        FrmAddCamera.setWindowTitle(QCoreApplication.translate("FrmAddCamera", u"Frame", None))
        self.pushButtonAdd.setText("")
        self.labelCamera.setText(QCoreApplication.translate("FrmAddCamera", u"\u041a\u0430\u043c\u0435\u0440\u0430", None))
    # retranslateUi

