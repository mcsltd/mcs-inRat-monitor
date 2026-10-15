# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'frm_config_detectorOwUFiF.ui'
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
    QLineEdit, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

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

        self.labelObject = QLabel(FrmConfigDetector)
        self.labelObject.setObjectName(u"labelObject")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.labelObject)

        self.comboBoxObject = QComboBox(FrmConfigDetector)
        self.comboBoxObject.setObjectName(u"comboBoxObject")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.comboBoxObject)


        self.verticalLayout.addLayout(self.formLayout)

        self.groupBoxDetectorParams = QGroupBox(FrmConfigDetector)
        self.groupBoxDetectorParams.setObjectName(u"groupBoxDetectorParams")
        self.groupBoxDetectorParams.setEnabled(False)
        self.gridLayout_2 = QGridLayout(self.groupBoxDetectorParams)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.verticalSpacer = QSpacerItem(20, 314, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer, 1, 0, 1, 1)

        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.horizontalLayoutBpf = QHBoxLayout()
        self.horizontalLayoutBpf.setObjectName(u"horizontalLayoutBpf")
        self.lineEditLowHz = QLineEdit(self.groupBoxDetectorParams)
        self.lineEditLowHz.setObjectName(u"lineEditLowHz")

        self.horizontalLayoutBpf.addWidget(self.lineEditLowHz)

        self.labelLowHz = QLabel(self.groupBoxDetectorParams)
        self.labelLowHz.setObjectName(u"labelLowHz")

        self.horizontalLayoutBpf.addWidget(self.labelLowHz)

        self.labelLine = QLabel(self.groupBoxDetectorParams)
        self.labelLine.setObjectName(u"labelLine")

        self.horizontalLayoutBpf.addWidget(self.labelLine)

        self.lineEditHighHz = QLineEdit(self.groupBoxDetectorParams)
        self.lineEditHighHz.setObjectName(u"lineEditHighHz")

        self.horizontalLayoutBpf.addWidget(self.lineEditHighHz)

        self.labelHighHz = QLabel(self.groupBoxDetectorParams)
        self.labelHighHz.setObjectName(u"labelHighHz")

        self.horizontalLayoutBpf.addWidget(self.labelHighHz)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayoutBpf.addItem(self.horizontalSpacer_5)


        self.gridLayout_3.addLayout(self.horizontalLayoutBpf, 0, 1, 1, 1)

        self.labelTWaveWin = QLabel(self.groupBoxDetectorParams)
        self.labelTWaveWin.setObjectName(u"labelTWaveWin")

        self.gridLayout_3.addWidget(self.labelTWaveWin, 3, 0, 1, 1)

        self.labelIntegWin = QLabel(self.groupBoxDetectorParams)
        self.labelIntegWin.setObjectName(u"labelIntegWin")

        self.gridLayout_3.addWidget(self.labelIntegWin, 1, 0, 1, 1)

        self.labelBpf = QLabel(self.groupBoxDetectorParams)
        self.labelBpf.setObjectName(u"labelBpf")

        self.gridLayout_3.addWidget(self.labelBpf, 0, 0, 1, 1)

        self.labelRefract = QLabel(self.groupBoxDetectorParams)
        self.labelRefract.setObjectName(u"labelRefract")

        self.gridLayout_3.addWidget(self.labelRefract, 2, 0, 1, 1)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.lineEditIntegrWin = QLineEdit(self.groupBoxDetectorParams)
        self.lineEditIntegrWin.setObjectName(u"lineEditIntegrWin")

        self.horizontalLayout_5.addWidget(self.lineEditIntegrWin)

        self.label_8 = QLabel(self.groupBoxDetectorParams)
        self.label_8.setObjectName(u"label_8")

        self.horizontalLayout_5.addWidget(self.label_8)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_2)


        self.gridLayout_3.addLayout(self.horizontalLayout_5, 1, 1, 1, 1)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.lineEditRef = QLineEdit(self.groupBoxDetectorParams)
        self.lineEditRef.setObjectName(u"lineEditRef")

        self.horizontalLayout_6.addWidget(self.lineEditRef)

        self.labelRefSec = QLabel(self.groupBoxDetectorParams)
        self.labelRefSec.setObjectName(u"labelRefSec")

        self.horizontalLayout_6.addWidget(self.labelRefSec)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_3)


        self.gridLayout_3.addLayout(self.horizontalLayout_6, 2, 1, 1, 1)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.lineEditTwave = QLineEdit(self.groupBoxDetectorParams)
        self.lineEditTwave.setObjectName(u"lineEditTwave")

        self.horizontalLayout_7.addWidget(self.lineEditTwave)

        self.label_10 = QLabel(self.groupBoxDetectorParams)
        self.label_10.setObjectName(u"label_10")

        self.horizontalLayout_7.addWidget(self.label_10)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_4)


        self.gridLayout_3.addLayout(self.horizontalLayout_7, 3, 1, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout_3, 0, 0, 1, 1)


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
        FrmConfigDetector.setWindowTitle(QCoreApplication.translate("FrmConfigDetector", u"\u0414\u0435\u0442\u0435\u043a\u0442\u043e\u0440 R-\u043f\u0438\u043a\u043e\u0432", None))
        self.labelDetector.setText(QCoreApplication.translate("FrmConfigDetector", u"\u0414\u0435\u0442\u0435\u043a\u0442\u043e\u0440 R-\u043f\u0438\u043a\u043e\u0432 \u042d\u041a\u0413:", None))
        self.labelObject.setText(QCoreApplication.translate("FrmConfigDetector", u"\u041e\u0431\u044a\u0435\u043a\u0442:", None))
        self.groupBoxDetectorParams.setTitle(QCoreApplication.translate("FrmConfigDetector", u"\u041f\u0430\u0440\u0430\u043c\u0435\u0442\u0440\u044b \u0434\u0435\u0442\u0435\u043a\u0442\u043e\u0440\u0430", None))
        self.labelLowHz.setText(QCoreApplication.translate("FrmConfigDetector", u"\u0413\u0446", None))
        self.labelLine.setText(QCoreApplication.translate("FrmConfigDetector", u"\u2014", None))
        self.labelHighHz.setText(QCoreApplication.translate("FrmConfigDetector", u"\u0413\u0446", None))
        self.labelTWaveWin.setText(QCoreApplication.translate("FrmConfigDetector", u"\u0414\u043b\u0438\u0442\u0435\u043b\u044c\u043d\u043e\u0441\u0442\u044c T-\u0432\u043e\u043b\u043d\u044b:", None))
        self.labelIntegWin.setText(QCoreApplication.translate("FrmConfigDetector", u"\u041e\u043a\u043d\u043e \u0438\u043d\u0442\u0435\u0433\u0440\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044f:", None))
        self.labelBpf.setText(QCoreApplication.translate("FrmConfigDetector", u"\u041f\u043e\u043b\u043e\u0441\u043d\u043e-\u043f\u0440\u043e\u043f\u0443\u0441\u043a\u0430\u044e\u0449\u0438\u0439 \u0444\u0438\u043b\u044c\u0442\u0440:", None))
        self.labelRefract.setText(QCoreApplication.translate("FrmConfigDetector", u"\u0420\u0435\u0444\u0440\u0430\u043a\u0442\u0435\u0440\u043d\u044b\u0439 \u043f\u0435\u0440\u0438\u043e\u0434:", None))
        self.label_8.setText(QCoreApplication.translate("FrmConfigDetector", u"\u0441", None))
        self.labelRefSec.setText(QCoreApplication.translate("FrmConfigDetector", u"\u0441", None))
        self.label_10.setText(QCoreApplication.translate("FrmConfigDetector", u"\u0441", None))
        self.pushButtonOk.setText(QCoreApplication.translate("FrmConfigDetector", u"\u041f\u0440\u0438\u043c\u0435\u043d\u0438\u0442\u044c", None))
    # retranslateUi

