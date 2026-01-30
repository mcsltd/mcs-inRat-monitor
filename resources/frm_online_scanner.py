# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'frm_online_scannerAUQPos.ui'
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
        FrmScanner.resize(396, 216)
        FrmScanner.setMinimumSize(QSize(300, 0))
        self.gridLayout_2 = QGridLayout(FrmScanner)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(5, 5, 5, 5)
        self.groupBox = QGroupBox(FrmScanner)
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
        self.gridLayout_3 = QGridLayout(self.groupBox)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.labelDevice = QLabel(self.groupBox)
        self.labelDevice.setObjectName(u"labelDevice")
        sizePolicy.setHeightForWidth(self.labelDevice.sizePolicy().hasHeightForWidth())
        self.labelDevice.setSizePolicy(sizePolicy)
        self.labelDevice.setMinimumSize(QSize(80, 30))
        self.labelDevice.setFont(font)
        self.labelDevice.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout.addWidget(self.labelDevice)

        self.comboBoxDevice = QComboBox(self.groupBox)
        self.comboBoxDevice.setObjectName(u"comboBoxDevice")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.comboBoxDevice.sizePolicy().hasHeightForWidth())
        self.comboBoxDevice.setSizePolicy(sizePolicy1)
        self.comboBoxDevice.setMinimumSize(QSize(0, 30))
        self.comboBoxDevice.setFont(font)

        self.horizontalLayout.addWidget(self.comboBoxDevice)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.pushButtonOpen = QPushButton(self.groupBox)
        self.pushButtonOpen.setObjectName(u"pushButtonOpen")
        sizePolicy1.setHeightForWidth(self.pushButtonOpen.sizePolicy().hasHeightForWidth())
        self.pushButtonOpen.setSizePolicy(sizePolicy1)
        self.pushButtonOpen.setMinimumSize(QSize(0, 40))
        self.pushButtonOpen.setFont(font)

        self.verticalLayout.addWidget(self.pushButtonOpen)


        self.gridLayout_3.addLayout(self.verticalLayout, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)


        self.retranslateUi(FrmScanner)

        QMetaObject.connectSlotsByName(FrmScanner)
    # setupUi

    def retranslateUi(self, FrmScanner):
        FrmScanner.setWindowTitle(QCoreApplication.translate("FrmScanner", u"Frame", None))
        self.groupBox.setTitle(QCoreApplication.translate("FrmScanner", u"BLE \u0441\u043a\u0430\u043d\u0435\u0440", None))
        self.labelDevice.setText(QCoreApplication.translate("FrmScanner", u"\u0423\u0441\u0442\u0440\u043e\u0439\u0441\u0442\u0432\u0430", None))
        self.pushButtonOpen.setText(QCoreApplication.translate("FrmScanner", u"\u041e\u0442\u043a\u0440\u044b\u0442\u044c", None))
    # retranslateUi

