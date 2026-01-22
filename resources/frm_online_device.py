# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'frm_online_devicekhDXmf.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QGroupBox,
    QPushButton, QSizePolicy, QVBoxLayout, QWidget)

class Ui_FrmDevice(object):
    def setupUi(self, FrmDevice):
        if not FrmDevice.objectName():
            FrmDevice.setObjectName(u"FrmDevice")
        FrmDevice.resize(337, 177)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(FrmDevice.sizePolicy().hasHeightForWidth())
        FrmDevice.setSizePolicy(sizePolicy)
        self.gridLayout = QGridLayout(FrmDevice)
        self.gridLayout.setObjectName(u"gridLayout")
        self.groupBox = QGroupBox(FrmDevice)
        self.groupBox.setObjectName(u"groupBox")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy1)
        font = QFont()
        font.setPointSize(12)
        self.groupBox.setFont(font)
        self.verticalLayoutWidget = QWidget(self.groupBox)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(10, 20, 301, 131))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.pushButtonStart = QPushButton(self.verticalLayoutWidget)
        self.pushButtonStart.setObjectName(u"pushButtonStart")
        self.pushButtonStart.setEnabled(False)

        self.verticalLayout.addWidget(self.pushButtonStart)

        self.pushButtonStop = QPushButton(self.verticalLayoutWidget)
        self.pushButtonStop.setObjectName(u"pushButtonStop")
        self.pushButtonStop.setEnabled(False)

        self.verticalLayout.addWidget(self.pushButtonStop)

        self.pushButtonDisconnect = QPushButton(self.verticalLayoutWidget)
        self.pushButtonDisconnect.setObjectName(u"pushButtonDisconnect")
        self.pushButtonDisconnect.setEnabled(False)

        self.verticalLayout.addWidget(self.pushButtonDisconnect)


        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)


        self.retranslateUi(FrmDevice)

        QMetaObject.connectSlotsByName(FrmDevice)
    # setupUi

    def retranslateUi(self, FrmDevice):
        FrmDevice.setWindowTitle(QCoreApplication.translate("FrmDevice", u"Frame", None))
        self.groupBox.setTitle(QCoreApplication.translate("FrmDevice", u"InRat", None))
        self.pushButtonStart.setText(QCoreApplication.translate("FrmDevice", u"\u0421\u0442\u0430\u0440\u0442", None))
        self.pushButtonStop.setText(QCoreApplication.translate("FrmDevice", u"\u0421\u0442\u043e\u043f", None))
        self.pushButtonDisconnect.setText(QCoreApplication.translate("FrmDevice", u"\u041e\u0442\u043a\u043b\u044e\u0447\u0438\u0442\u044c", None))
    # retranslateUi

