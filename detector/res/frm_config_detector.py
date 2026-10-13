# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'frm_config_detectorRbDEHj.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFormLayout, QFrame,
    QGridLayout, QGroupBox, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_FrmConfigDetector(object):
    def setupUi(self, FrmConfigDetector):
        if not FrmConfigDetector.objectName():
            FrmConfigDetector.setObjectName(u"FrmConfigDetector")
        FrmConfigDetector.resize(577, 443)
        self.gridLayout = QGridLayout(FrmConfigDetector)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.labelDetector = QLabel(FrmConfigDetector)
        self.labelDetector.setObjectName(u"labelDetector")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.labelDetector)

        self.comboBoxSwitch = QComboBox(FrmConfigDetector)
        self.comboBoxSwitch.setObjectName(u"comboBoxSwitch")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.comboBoxSwitch)


        self.verticalLayout.addLayout(self.formLayout)

        self.groupBoxDetectorParams = QGroupBox(FrmConfigDetector)
        self.groupBoxDetectorParams.setObjectName(u"groupBoxDetectorParams")
        self.gridLayout_2 = QGridLayout(self.groupBoxDetectorParams)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.verticalSpacer = QSpacerItem(20, 314, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer, 0, 0, 1, 1)


        self.verticalLayout.addWidget(self.groupBoxDetectorParams)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.pushButtonOk = QPushButton(FrmConfigDetector)
        self.pushButtonOk.setObjectName(u"pushButtonOk")

        self.horizontalLayout.addWidget(self.pushButtonOk)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)


        self.retranslateUi(FrmConfigDetector)

        QMetaObject.connectSlotsByName(FrmConfigDetector)
    # setupUi

    def retranslateUi(self, FrmConfigDetector):
        FrmConfigDetector.setWindowTitle(QCoreApplication.translate("FrmConfigDetector", u"Frame", None))
        self.labelDetector.setText(QCoreApplication.translate("FrmConfigDetector", u"\u0414\u0435\u0442\u0435\u043a\u0442\u043e\u0440 R-\u043f\u0438\u043a\u043e\u0432 \u042d\u041a\u0413:", None))
        self.groupBoxDetectorParams.setTitle(QCoreApplication.translate("FrmConfigDetector", u"\u041f\u0430\u0440\u0430\u043c\u0435\u0442\u0440\u044b \u0434\u0435\u0442\u0435\u043a\u0442\u043e\u0440\u0430", None))
        self.pushButtonOk.setText(QCoreApplication.translate("FrmConfigDetector", u"\u041f\u0440\u0438\u043c\u0435\u043d\u0438\u0442\u044c", None))
    # retranslateUi

