# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'frm_online_deviceXQojNI.ui'
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
    QPushButton, QSizePolicy, QWidget)

class Ui_FrmDevice(object):
    def setupUi(self, FrmDevice):
        if not FrmDevice.objectName():
            FrmDevice.setObjectName(u"FrmDevice")
        FrmDevice.resize(380, 243)
        self.gridLayout_3 = QGridLayout(FrmDevice)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(5, 5, 5, 5)
        self.groupBox = QGroupBox(FrmDevice)
        self.groupBox.setObjectName(u"groupBox")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setMinimumSize(QSize(350, 180))
        font = QFont()
        font.setPointSize(12)
        self.groupBox.setFont(font)
        self.gridLayout_2 = QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(10, 10, 10, 10)
        self.pushButtonStart = QPushButton(self.groupBox)
        self.pushButtonStart.setObjectName(u"pushButtonStart")
        self.pushButtonStart.setEnabled(False)
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.pushButtonStart.sizePolicy().hasHeightForWidth())
        self.pushButtonStart.setSizePolicy(sizePolicy1)
        self.pushButtonStart.setMinimumSize(QSize(0, 40))
        self.pushButtonStart.setFont(font)

        self.gridLayout_4.addWidget(self.pushButtonStart, 0, 0, 1, 1)

        self.pushButtonStop = QPushButton(self.groupBox)
        self.pushButtonStop.setObjectName(u"pushButtonStop")
        self.pushButtonStop.setEnabled(False)
        sizePolicy1.setHeightForWidth(self.pushButtonStop.sizePolicy().hasHeightForWidth())
        self.pushButtonStop.setSizePolicy(sizePolicy1)
        self.pushButtonStop.setMinimumSize(QSize(0, 40))
        self.pushButtonStop.setFont(font)

        self.gridLayout_4.addWidget(self.pushButtonStop, 1, 0, 1, 1)

        self.pushButtonDisconnect = QPushButton(self.groupBox)
        self.pushButtonDisconnect.setObjectName(u"pushButtonDisconnect")
        self.pushButtonDisconnect.setEnabled(False)
        sizePolicy1.setHeightForWidth(self.pushButtonDisconnect.sizePolicy().hasHeightForWidth())
        self.pushButtonDisconnect.setSizePolicy(sizePolicy1)
        self.pushButtonDisconnect.setMinimumSize(QSize(0, 40))
        self.pushButtonDisconnect.setFont(font)

        self.gridLayout_4.addWidget(self.pushButtonDisconnect, 2, 0, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout_4, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)


        self.gridLayout_3.addLayout(self.gridLayout, 0, 0, 1, 1)


        self.retranslateUi(FrmDevice)

        QMetaObject.connectSlotsByName(FrmDevice)
    # setupUi

    def retranslateUi(self, FrmDevice):
        FrmDevice.setWindowTitle(QCoreApplication.translate("FrmDevice", u"Frame", None))
        self.groupBox.setTitle(QCoreApplication.translate("FrmDevice", u"inRat", None))
        self.pushButtonStart.setText(QCoreApplication.translate("FrmDevice", u"\u0421\u0442\u0430\u0440\u0442", None))
        self.pushButtonStop.setText(QCoreApplication.translate("FrmDevice", u"\u0421\u0442\u043e\u043f", None))
        self.pushButtonDisconnect.setText(QCoreApplication.translate("FrmDevice", u"\u041e\u0442\u043a\u043b\u044e\u0447\u0438\u0442\u044c", None))
    # retranslateUi

