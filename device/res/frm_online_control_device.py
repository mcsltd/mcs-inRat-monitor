# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'frm_online_control_deviceMIPvfn.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QFrame, QGridLayout,
    QGroupBox, QHBoxLayout, QLabel, QPushButton,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_FrmOnlineControlDevice(object):
    def setupUi(self, FrmOnlineControlDevice):
        if not FrmOnlineControlDevice.objectName():
            FrmOnlineControlDevice.setObjectName(u"FrmOnlineControlDevice")
        FrmOnlineControlDevice.resize(317, 150)
        FrmOnlineControlDevice.setFrameShape(QFrame.Shape.Panel)
        FrmOnlineControlDevice.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout = QGridLayout(FrmOnlineControlDevice)
        self.gridLayout.setObjectName(u"gridLayout")
        self.groupBox = QGroupBox(FrmOnlineControlDevice)
        self.groupBox.setObjectName(u"groupBox")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setMinimumSize(QSize(100, 40))
        font = QFont()
        font.setPointSize(12)
        self.groupBox.setFont(font)
        self.gridLayout_3 = QGridLayout(self.groupBox)
        self.gridLayout_3.setSpacing(7)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.pushButtonStart = QPushButton(self.groupBox)
        self.pushButtonStart.setObjectName(u"pushButtonStart")
        self.pushButtonStart.setEnabled(False)
        self.pushButtonStart.setFont(font)

        self.horizontalLayout_2.addWidget(self.pushButtonStart)

        self.pushButtonStop = QPushButton(self.groupBox)
        self.pushButtonStop.setObjectName(u"pushButtonStop")
        self.pushButtonStop.setEnabled(False)
        self.pushButtonStop.setFont(font)

        self.horizontalLayout_2.addWidget(self.pushButtonStop)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.pushButtonConfig = QPushButton(self.groupBox)
        self.pushButtonConfig.setObjectName(u"pushButtonConfig")
        self.pushButtonConfig.setEnabled(False)
        self.pushButtonConfig.setFont(font)

        self.verticalLayout_4.addWidget(self.pushButtonConfig)


        self.verticalLayout.addLayout(self.verticalLayout_4)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.labelActivated = QLabel(self.groupBox)
        self.labelActivated.setObjectName(u"labelActivated")
        self.labelActivated.setFont(font)

        self.gridLayout_2.addWidget(self.labelActivated, 0, 0, 1, 1)

        self.checkBoxActivated = QCheckBox(self.groupBox)
        self.checkBoxActivated.setObjectName(u"checkBoxActivated")
        self.checkBoxActivated.setEnabled(False)
        self.checkBoxActivated.setFont(font)

        self.gridLayout_2.addWidget(self.checkBoxActivated, 0, 1, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout_2)


        self.gridLayout_3.addLayout(self.verticalLayout, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.groupBox, 1, 0, 1, 1)


        self.retranslateUi(FrmOnlineControlDevice)

        QMetaObject.connectSlotsByName(FrmOnlineControlDevice)
    # setupUi

    def retranslateUi(self, FrmOnlineControlDevice):
        FrmOnlineControlDevice.setWindowTitle(QCoreApplication.translate("FrmOnlineControlDevice", u"Frame", None))
        self.groupBox.setTitle(QCoreApplication.translate("FrmOnlineControlDevice", u"\u0423\u043f\u0440\u0430\u0432\u043b\u0435\u043d\u0438\u0435", None))
        self.pushButtonStart.setText(QCoreApplication.translate("FrmOnlineControlDevice", u"\u0421\u0442\u0430\u0440\u0442", None))
        self.pushButtonStop.setText(QCoreApplication.translate("FrmOnlineControlDevice", u"\u0421\u0442\u043e\u043f", None))
        self.pushButtonConfig.setText(QCoreApplication.translate("FrmOnlineControlDevice", u"\u041d\u0430\u0441\u0442\u0440\u043e\u0438\u0442\u044c", None))
        self.labelActivated.setText(QCoreApplication.translate("FrmOnlineControlDevice", u"\u0410\u043a\u0442\u0438\u0432\u0438\u0440\u043e\u0432\u0430\u043d\u043e", None))
        self.checkBoxActivated.setText("")
    # retranslateUi

