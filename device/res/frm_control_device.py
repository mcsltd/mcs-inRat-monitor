# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'frm_control_deviceeRZISP.ui'
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

class Ui_FrmControlDevice(object):
    def setupUi(self, FrmControlDevice):
        if not FrmControlDevice.objectName():
            FrmControlDevice.setObjectName(u"FrmControlDevice")
        FrmControlDevice.resize(194, 128)
        self.verticalLayout_2 = QVBoxLayout(FrmControlDevice)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pushButtonStop = QPushButton(FrmControlDevice)
        self.pushButtonStop.setObjectName(u"pushButtonStop")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonStop.sizePolicy().hasHeightForWidth())
        self.pushButtonStop.setSizePolicy(sizePolicy)
        self.pushButtonStop.setMaximumSize(QSize(75, 75))

        self.horizontalLayout.addWidget(self.pushButtonStop)

        self.pushButtonStart = QPushButton(FrmControlDevice)
        self.pushButtonStart.setObjectName(u"pushButtonStart")
        sizePolicy.setHeightForWidth(self.pushButtonStart.sizePolicy().hasHeightForWidth())
        self.pushButtonStart.setSizePolicy(sizePolicy)
        self.pushButtonStart.setMinimumSize(QSize(75, 75))

        self.horizontalLayout.addWidget(self.pushButtonStart)


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
        self.pushButtonStop.setText(QCoreApplication.translate("FrmControlDevice", u"\u0421\u0442\u0430\u0440\u0442", None))
        self.pushButtonStart.setText(QCoreApplication.translate("FrmControlDevice", u"\u0421\u0442\u043e\u043f", None))
        self.labelManage.setText(QCoreApplication.translate("FrmControlDevice", u"\u0423\u043f\u0440\u0430\u0432\u043b\u0435\u043d\u0438\u0435", None))
    # retranslateUi

