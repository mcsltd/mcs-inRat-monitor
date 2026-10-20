# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'frm_battery_leveldpGAvk.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QProgressBar, QSizePolicy, QWidget)

class Ui_FrmDeviceStatus(object):
    def setupUi(self, FrmDeviceStatus):
        if not FrmDeviceStatus.objectName():
            FrmDeviceStatus.setObjectName(u"FrmDeviceStatus")
        FrmDeviceStatus.resize(175, 69)
        self.horizontalLayout_3 = QHBoxLayout(FrmDeviceStatus)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.labelDeviceName = QLabel(FrmDeviceStatus)
        self.labelDeviceName.setObjectName(u"labelDeviceName")
        font = QFont()
        font.setPointSize(11)
        self.labelDeviceName.setFont(font)

        self.horizontalLayout.addWidget(self.labelDeviceName)

        self.progressBarBatteryLevel = QProgressBar(FrmDeviceStatus)
        self.progressBarBatteryLevel.setObjectName(u"progressBarBatteryLevel")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.progressBarBatteryLevel.sizePolicy().hasHeightForWidth())
        self.progressBarBatteryLevel.setSizePolicy(sizePolicy)
        self.progressBarBatteryLevel.setMinimumSize(QSize(65, 20))
        self.progressBarBatteryLevel.setMaximumSize(QSize(65, 25))
        self.progressBarBatteryLevel.setValue(10)
        self.progressBarBatteryLevel.setTextVisible(False)

        self.horizontalLayout.addWidget(self.progressBarBatteryLevel)

        self.labelBatteryLevel = QLabel(FrmDeviceStatus)
        self.labelBatteryLevel.setObjectName(u"labelBatteryLevel")
        self.labelBatteryLevel.setMinimumSize(QSize(30, 0))
        self.labelBatteryLevel.setMaximumSize(QSize(30, 16777215))

        self.horizontalLayout.addWidget(self.labelBatteryLevel)


        self.horizontalLayout_3.addLayout(self.horizontalLayout)


        self.retranslateUi(FrmDeviceStatus)

        QMetaObject.connectSlotsByName(FrmDeviceStatus)
    # setupUi

    def retranslateUi(self, FrmDeviceStatus):
        FrmDeviceStatus.setWindowTitle(QCoreApplication.translate("FrmDeviceStatus", u"Frame", None))
        self.labelDeviceName.setText(QCoreApplication.translate("FrmDeviceStatus", u"inRat-1", None))
        self.labelBatteryLevel.setText(QCoreApplication.translate("FrmDeviceStatus", u"10%", None))
    # retranslateUi

