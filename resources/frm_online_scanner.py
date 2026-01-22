# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'frm_online_scannerqHQELR.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QGridLayout,
    QGroupBox, QHBoxLayout, QLabel, QPushButton,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_FrmScanner(object):
    def setupUi(self, FrmScanner):
        if not FrmScanner.objectName():
            FrmScanner.setObjectName(u"FrmScanner")
        FrmScanner.resize(337, 177)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(FrmScanner.sizePolicy().hasHeightForWidth())
        FrmScanner.setSizePolicy(sizePolicy)
        self.gridLayout = QGridLayout(FrmScanner)
        self.gridLayout.setObjectName(u"gridLayout")
        self.groupBox = QGroupBox(FrmScanner)
        self.groupBox.setObjectName(u"groupBox")
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        font = QFont()
        font.setPointSize(12)
        self.groupBox.setFont(font)
        self.verticalLayoutWidget = QWidget(self.groupBox)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(10, 20, 301, 121))
        self.verticalLayoutWidget.setFont(font)
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayoutDevice = QHBoxLayout()
        self.horizontalLayoutDevice.setObjectName(u"horizontalLayoutDevice")
        self.labelDevice = QLabel(self.verticalLayoutWidget)
        self.labelDevice.setObjectName(u"labelDevice")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.labelDevice.sizePolicy().hasHeightForWidth())
        self.labelDevice.setSizePolicy(sizePolicy1)
        self.labelDevice.setMaximumSize(QSize(88, 16777215))
        self.labelDevice.setFont(font)

        self.horizontalLayoutDevice.addWidget(self.labelDevice)

        self.comboBoxDevice = QComboBox(self.verticalLayoutWidget)
        self.comboBoxDevice.setObjectName(u"comboBoxDevice")
        sizePolicy1.setHeightForWidth(self.comboBoxDevice.sizePolicy().hasHeightForWidth())
        self.comboBoxDevice.setSizePolicy(sizePolicy1)
        self.comboBoxDevice.setFont(font)

        self.horizontalLayoutDevice.addWidget(self.comboBoxDevice)


        self.verticalLayout.addLayout(self.horizontalLayoutDevice)

        self.pushButtonOpen = QPushButton(self.verticalLayoutWidget)
        self.pushButtonOpen.setObjectName(u"pushButtonOpen")
        self.pushButtonOpen.setEnabled(False)
        self.pushButtonOpen.setFont(font)

        self.verticalLayout.addWidget(self.pushButtonOpen)


        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)


        self.retranslateUi(FrmScanner)

        QMetaObject.connectSlotsByName(FrmScanner)
    # setupUi

    def retranslateUi(self, FrmScanner):
        FrmScanner.setWindowTitle(QCoreApplication.translate("FrmScanner", u"Frame", None))
        self.groupBox.setTitle(QCoreApplication.translate("FrmScanner", u"BLE c\u043a\u0430\u043d\u0435\u0440", None))
        self.labelDevice.setText(QCoreApplication.translate("FrmScanner", u"\u0423\u0441\u0442\u0440\u043e\u0439\u0441\u0442\u0432\u043e", None))
        self.pushButtonOpen.setText(QCoreApplication.translate("FrmScanner", u"\u0421\u043e\u0435\u0434\u0438\u043d\u0438\u0442\u044c\u0441\u044f", None))
    # retranslateUi

