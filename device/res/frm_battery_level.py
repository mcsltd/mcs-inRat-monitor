# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'frm_battery_levelXaHwrD.ui'
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
    QProgressBar, QSizePolicy, QWidget)

class Ui_FrmBattery(object):
    def setupUi(self, FrmBattery):
        if not FrmBattery.objectName():
            FrmBattery.setObjectName(u"FrmBattery")
        FrmBattery.resize(137, 65)
        self.horizontalLayout_3 = QHBoxLayout(FrmBattery)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.progressBarBatteryLevel = QProgressBar(FrmBattery)
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

        self.labelBatteryLevel = QLabel(FrmBattery)
        self.labelBatteryLevel.setObjectName(u"labelBatteryLevel")
        self.labelBatteryLevel.setMinimumSize(QSize(30, 0))
        self.labelBatteryLevel.setMaximumSize(QSize(30, 16777215))

        self.horizontalLayout.addWidget(self.labelBatteryLevel)


        self.horizontalLayout_3.addLayout(self.horizontalLayout)


        self.retranslateUi(FrmBattery)

        QMetaObject.connectSlotsByName(FrmBattery)
    # setupUi

    def retranslateUi(self, FrmBattery):
        FrmBattery.setWindowTitle(QCoreApplication.translate("FrmBattery", u"Frame", None))
        self.labelBatteryLevel.setText(QCoreApplication.translate("FrmBattery", u"10%", None))
    # retranslateUi

