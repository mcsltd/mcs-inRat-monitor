# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'frm_control_devicehfcVPi.ui'
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

class Ui_FrmControlDevice(object):
    def setupUi(self, FrmControlDevice):
        if not FrmControlDevice.objectName():
            FrmControlDevice.setObjectName(u"FrmControlDevice")
        FrmControlDevice.resize(198, 136)
        self.gridLayout = QGridLayout(FrmControlDevice)
        self.gridLayout.setObjectName(u"gridLayout")
        self.line_2 = QFrame(FrmControlDevice)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.VLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout.addWidget(self.line_2, 0, 0, 1, 1)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pushButtonStart = QPushButton(FrmControlDevice)
        self.pushButtonStart.setObjectName(u"pushButtonStart")
        self.pushButtonStart.setEnabled(False)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonStart.sizePolicy().hasHeightForWidth())
        self.pushButtonStart.setSizePolicy(sizePolicy)
        self.pushButtonStart.setMaximumSize(QSize(75, 75))
        self.pushButtonStart.setStyleSheet(u"QPushButton {\n"
"    background-color: transparent;\n"
"    border: none;\n"
"}")
        icon = QIcon()
        icon.addFile(u":/images/start.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButtonStart.setIcon(icon)
        self.pushButtonStart.setIconSize(QSize(50, 50))

        self.horizontalLayout.addWidget(self.pushButtonStart)

        self.pushButtonStop = QPushButton(FrmControlDevice)
        self.pushButtonStop.setObjectName(u"pushButtonStop")
        self.pushButtonStop.setEnabled(False)
        sizePolicy.setHeightForWidth(self.pushButtonStop.sizePolicy().hasHeightForWidth())
        self.pushButtonStop.setSizePolicy(sizePolicy)
        self.pushButtonStop.setMinimumSize(QSize(75, 75))
        self.pushButtonStop.setStyleSheet(u"QPushButton {\n"
"    background-color: transparent;\n"
"    border: none;\n"
"}")
        icon1 = QIcon()
        icon1.addFile(u":/images/stop.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButtonStop.setIcon(icon1)
        self.pushButtonStop.setIconSize(QSize(50, 50))

        self.horizontalLayout.addWidget(self.pushButtonStop)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.labelManage = QLabel(FrmControlDevice)
        self.labelManage.setObjectName(u"labelManage")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.labelManage.sizePolicy().hasHeightForWidth())
        self.labelManage.setSizePolicy(sizePolicy1)
        self.labelManage.setMaximumSize(QSize(16777215, 15))
        font = QFont()
        font.setPointSize(10)
        self.labelManage.setFont(font)
        self.labelManage.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.labelManage)


        self.gridLayout.addLayout(self.verticalLayout, 0, 1, 1, 1)

        self.line = QFrame(FrmControlDevice)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.VLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout.addWidget(self.line, 0, 2, 1, 1)


        self.retranslateUi(FrmControlDevice)

        QMetaObject.connectSlotsByName(FrmControlDevice)
    # setupUi

    def retranslateUi(self, FrmControlDevice):
        FrmControlDevice.setWindowTitle(QCoreApplication.translate("FrmControlDevice", u"Frame", None))
        self.pushButtonStart.setText("")
        self.pushButtonStop.setText("")
        self.labelManage.setText(QCoreApplication.translate("FrmControlDevice", u"\u0423\u043f\u0440\u0430\u0432\u043b\u0435\u043d\u0438\u0435", None))
    # retranslateUi

