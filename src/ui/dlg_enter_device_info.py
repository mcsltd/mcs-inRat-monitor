# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dlg_enter_device_infoaECyXW.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(375, 150)
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(20, 20, 291, 16))
        self.gridLayoutWidget = QWidget(Form)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(30, 60, 311, 41))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.labelSN = QLabel(self.gridLayoutWidget)
        self.labelSN.setObjectName(u"labelSN")

        self.gridLayout.addWidget(self.labelSN, 0, 0, 1, 1)

        self.lineEditSNValue = QLineEdit(self.gridLayoutWidget)
        self.lineEditSNValue.setObjectName(u"lineEditSNValue")

        self.gridLayout.addWidget(self.lineEditSNValue, 0, 1, 1, 1)

        self.pushButtonConnect = QPushButton(Form)
        self.pushButtonConnect.setObjectName(u"pushButtonConnect")
        self.pushButtonConnect.setGeometry(QRect(270, 110, 75, 24))
        self.pushButtonSave = QPushButton(Form)
        self.pushButtonSave.setObjectName(u"pushButtonSave")
        self.pushButtonSave.setGeometry(QRect(190, 110, 75, 24))

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"Please, enter device information:", None))
        self.labelSN.setText(QCoreApplication.translate("Form", u"Serial Number", None))
        self.pushButtonConnect.setText(QCoreApplication.translate("Form", u"Connect", None))
        self.pushButtonSave.setText(QCoreApplication.translate("Form", u"Save", None))
    # retranslateUi

