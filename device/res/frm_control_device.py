# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'frm_control_devicewHCXGb.ui'
##
## Created by: Qt User Interface Compiler version 6.11.2
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QVBoxLayout, QWidget)
import resources.resources_rc

class Ui_FrmControlDevice(object):
    def setupUi(self, FrmControlDevice):
        if not FrmControlDevice.objectName():
            FrmControlDevice.setObjectName(u"FrmControlDevice")
        FrmControlDevice.resize(198, 136)
        self.verticalLayout_2 = QVBoxLayout(FrmControlDevice)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
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


        self.verticalLayout_2.addLayout(self.verticalLayout)


        self.retranslateUi(FrmControlDevice)

        QMetaObject.connectSlotsByName(FrmControlDevice)
    # setupUi

    def retranslateUi(self, FrmControlDevice):
        FrmControlDevice.setWindowTitle(QCoreApplication.translate("FrmControlDevice", u"Frame", None))
        self.pushButtonStart.setText("")
        self.pushButtonStop.setText("")
        self.labelManage.setText(QCoreApplication.translate("FrmControlDevice", u"\u0423\u043f\u0440\u0430\u0432\u043b\u0435\u043d\u0438\u0435", None))
    # retranslateUi

