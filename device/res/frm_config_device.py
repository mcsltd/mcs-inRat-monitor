# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'frm_config_deviceQNNXDD.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFormLayout,
    QFrame, QGridLayout, QGroupBox, QLabel,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_FrmConfigDevicePane(object):
    def setupUi(self, FrmConfigDevicePane):
        if not FrmConfigDevicePane.objectName():
            FrmConfigDevicePane.setObjectName(u"FrmConfigDevicePane")
        FrmConfigDevicePane.resize(623, 564)
        self.gridLayout = QGridLayout(FrmConfigDevicePane)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBoxInRat = QGroupBox(FrmConfigDevicePane)
        self.groupBoxInRat.setObjectName(u"groupBoxInRat")
        self.gridLayout_7 = QGridLayout(self.groupBoxInRat)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayoutInRat = QGridLayout()
        self.gridLayoutInRat.setObjectName(u"gridLayoutInRat")
        self.checkBoxActivated = QCheckBox(self.groupBoxInRat)
        self.checkBoxActivated.setObjectName(u"checkBoxActivated")

        self.gridLayoutInRat.addWidget(self.checkBoxActivated, 0, 0, 1, 1)


        self.gridLayout_7.addLayout(self.gridLayoutInRat, 0, 0, 1, 1)


        self.verticalLayout.addWidget(self.groupBoxInRat)

        self.groupBoxExg = QGroupBox(FrmConfigDevicePane)
        self.groupBoxExg.setObjectName(u"groupBoxExg")
        self.gridLayout_2 = QGridLayout(self.groupBoxExg)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.labelExg = QLabel(self.groupBoxExg)
        self.labelExg.setObjectName(u"labelExg")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.labelExg)

        self.comboBoxExg = QComboBox(self.groupBoxExg)
        self.comboBoxExg.setObjectName(u"comboBoxExg")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.comboBoxExg)

        self.labelHpf = QLabel(self.groupBoxExg)
        self.labelHpf.setObjectName(u"labelHpf")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.labelHpf)

        self.comboBoxHpf = QComboBox(self.groupBoxExg)
        self.comboBoxHpf.setObjectName(u"comboBoxHpf")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.comboBoxHpf)

        self.labelGain = QLabel(self.groupBoxExg)
        self.labelGain.setObjectName(u"labelGain")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.labelGain)

        self.comboBoxGain = QComboBox(self.groupBoxExg)
        self.comboBoxGain.setObjectName(u"comboBoxGain")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.comboBoxGain)


        self.gridLayout_2.addLayout(self.formLayout, 1, 0, 1, 1)


        self.verticalLayout.addWidget(self.groupBoxExg)

        self.groupBoxAcc = QGroupBox(FrmConfigDevicePane)
        self.groupBoxAcc.setObjectName(u"groupBoxAcc")
        self.verticalLayout_3 = QVBoxLayout(self.groupBoxAcc)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.formLayoutAcc = QFormLayout()
        self.formLayoutAcc.setObjectName(u"formLayoutAcc")
        self.labelAcc = QLabel(self.groupBoxAcc)
        self.labelAcc.setObjectName(u"labelAcc")

        self.formLayoutAcc.setWidget(0, QFormLayout.ItemRole.LabelRole, self.labelAcc)

        self.comboBoxAcc = QComboBox(self.groupBoxAcc)
        self.comboBoxAcc.setObjectName(u"comboBoxAcc")

        self.formLayoutAcc.setWidget(0, QFormLayout.ItemRole.FieldRole, self.comboBoxAcc)

        self.labelScale = QLabel(self.groupBoxAcc)
        self.labelScale.setObjectName(u"labelScale")

        self.formLayoutAcc.setWidget(1, QFormLayout.ItemRole.LabelRole, self.labelScale)

        self.comboBoxScaleAcc = QComboBox(self.groupBoxAcc)
        self.comboBoxScaleAcc.setObjectName(u"comboBoxScaleAcc")

        self.formLayoutAcc.setWidget(1, QFormLayout.ItemRole.FieldRole, self.comboBoxScaleAcc)


        self.verticalLayout_3.addLayout(self.formLayoutAcc)


        self.verticalLayout.addWidget(self.groupBoxAcc)

        self.groupBoxTemp = QGroupBox(FrmConfigDevicePane)
        self.groupBoxTemp.setObjectName(u"groupBoxTemp")
        self.gridLayout_5 = QGridLayout(self.groupBoxTemp)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayoutTemp = QGridLayout()
        self.gridLayoutTemp.setObjectName(u"gridLayoutTemp")
        self.labelInfoTemp = QLabel(self.groupBoxTemp)
        self.labelInfoTemp.setObjectName(u"labelInfoTemp")

        self.gridLayoutTemp.addWidget(self.labelInfoTemp, 0, 1, 1, 1)

        self.checkBoxTemp = QCheckBox(self.groupBoxTemp)
        self.checkBoxTemp.setObjectName(u"checkBoxTemp")

        self.gridLayoutTemp.addWidget(self.checkBoxTemp, 0, 0, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayoutTemp.addItem(self.horizontalSpacer_2, 0, 2, 1, 1)


        self.gridLayout_5.addLayout(self.gridLayoutTemp, 0, 0, 1, 1)


        self.verticalLayout.addWidget(self.groupBoxTemp)

        self.groupBoxEv = QGroupBox(FrmConfigDevicePane)
        self.groupBoxEv.setObjectName(u"groupBoxEv")
        self.gridLayout_4 = QGridLayout(self.groupBoxEv)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayoutEv = QGridLayout()
        self.gridLayoutEv.setObjectName(u"gridLayoutEv")
        self.checkBoxActivity = QCheckBox(self.groupBoxEv)
        self.checkBoxActivity.setObjectName(u"checkBoxActivity")

        self.gridLayoutEv.addWidget(self.checkBoxActivity, 0, 0, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayoutEv.addItem(self.horizontalSpacer, 0, 2, 1, 1)

        self.labelSens = QLabel(self.groupBoxEv)
        self.labelSens.setObjectName(u"labelSens")

        self.gridLayoutEv.addWidget(self.labelSens, 3, 0, 1, 1)

        self.labelInfoOrientation = QLabel(self.groupBoxEv)
        self.labelInfoOrientation.setObjectName(u"labelInfoOrientation")

        self.gridLayoutEv.addWidget(self.labelInfoOrientation, 2, 1, 1, 1)

        self.checkBoxOrientation = QCheckBox(self.groupBoxEv)
        self.checkBoxOrientation.setObjectName(u"checkBoxOrientation")

        self.gridLayoutEv.addWidget(self.checkBoxOrientation, 2, 0, 1, 1)

        self.labelInfoActivity = QLabel(self.groupBoxEv)
        self.labelInfoActivity.setObjectName(u"labelInfoActivity")

        self.gridLayoutEv.addWidget(self.labelInfoActivity, 0, 1, 1, 1)

        self.checkBoxFreefall = QCheckBox(self.groupBoxEv)
        self.checkBoxFreefall.setObjectName(u"checkBoxFreefall")

        self.gridLayoutEv.addWidget(self.checkBoxFreefall, 1, 0, 1, 1)

        self.labelInfoFreefall = QLabel(self.groupBoxEv)
        self.labelInfoFreefall.setObjectName(u"labelInfoFreefall")

        self.gridLayoutEv.addWidget(self.labelInfoFreefall, 1, 1, 1, 1)

        self.labelInfoSens = QLabel(self.groupBoxEv)
        self.labelInfoSens.setObjectName(u"labelInfoSens")

        self.gridLayoutEv.addWidget(self.labelInfoSens, 3, 1, 1, 1)

        self.comboBoxEvSens = QComboBox(self.groupBoxEv)
        self.comboBoxEvSens.setObjectName(u"comboBoxEvSens")

        self.gridLayoutEv.addWidget(self.comboBoxEvSens, 3, 2, 1, 1)


        self.gridLayout_4.addLayout(self.gridLayoutEv, 0, 0, 1, 1)


        self.verticalLayout.addWidget(self.groupBoxEv)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)


        self.retranslateUi(FrmConfigDevicePane)

        QMetaObject.connectSlotsByName(FrmConfigDevicePane)
    # setupUi

    def retranslateUi(self, FrmConfigDevicePane):
        FrmConfigDevicePane.setWindowTitle(QCoreApplication.translate("FrmConfigDevicePane", u"Frame", None))
        self.groupBoxInRat.setTitle(QCoreApplication.translate("FrmConfigDevicePane", u"inRat-...", None))
        self.checkBoxActivated.setText(QCoreApplication.translate("FrmConfigDevicePane", u"\u0410\u043a\u0442\u0438\u0432\u0438\u0440\u043e\u0432\u0430\u043d\u043e", None))
        self.groupBoxExg.setTitle(QCoreApplication.translate("FrmConfigDevicePane", u"ExG (\u042d\u041a\u0413/\u042d\u042d\u0413)", None))
        self.labelExg.setText(QCoreApplication.translate("FrmConfigDevicePane", u"ExG, \u0413\u0446", None))
        self.labelHpf.setText(QCoreApplication.translate("FrmConfigDevicePane", u"\u0424\u0412\u0427", None))
        self.labelGain.setText(QCoreApplication.translate("FrmConfigDevicePane", u"\u0423\u0441\u0438\u043b\u0435\u043d\u0438\u0435", None))
        self.groupBoxAcc.setTitle(QCoreApplication.translate("FrmConfigDevicePane", u"\u0410\u043a\u0441\u0435\u043b\u0435\u0440\u043e\u043c\u0435\u0442\u0440", None))
        self.labelAcc.setText(QCoreApplication.translate("FrmConfigDevicePane", u"\u0410\u043a\u0441\u0435\u043b\u0435\u0440\u043e\u043c\u0435\u0442\u0440", None))
        self.labelScale.setText(QCoreApplication.translate("FrmConfigDevicePane", u"\u0414\u0438\u0430\u043f\u0430\u0437\u043e\u043d", None))
        self.groupBoxTemp.setTitle(QCoreApplication.translate("FrmConfigDevicePane", u"\u0421\u043e\u0431\u044b\u0442\u0438\u044f \u0442\u0435\u043c\u043f\u0435\u0440\u0430\u0442\u0443\u0440\u044b", None))
        self.labelInfoTemp.setText(QCoreApplication.translate("FrmConfigDevicePane", u"?", None))
        self.checkBoxTemp.setText(QCoreApplication.translate("FrmConfigDevicePane", u"\u0422\u0435\u043c\u043f\u0435\u0440\u0430\u0442\u0443\u0440\u0430 (\u0422)", None))
        self.groupBoxEv.setTitle(QCoreApplication.translate("FrmConfigDevicePane", u"\u0421\u043e\u0431\u044b\u0442\u0438\u044f \u0444\u0438\u0437\u0438\u0447\u0435\u0441\u043a\u043e\u0439 \u0430\u043a\u0442\u0438\u0432\u043d\u043e\u0441\u0442\u0438", None))
        self.checkBoxActivity.setText(QCoreApplication.translate("FrmConfigDevicePane", u"\u0410\u043a\u0442\u0438\u0432\u043d\u043e\u0441\u0442\u044c (\u0410)", None))
        self.labelSens.setText(QCoreApplication.translate("FrmConfigDevicePane", u"\u0427\u0443\u0441\u0442\u0432\u0438\u0442\u0435\u043b\u044c\u043d\u043e\u0441\u0442\u044c ", None))
        self.labelInfoOrientation.setText(QCoreApplication.translate("FrmConfigDevicePane", u"?", None))
        self.checkBoxOrientation.setText(QCoreApplication.translate("FrmConfigDevicePane", u"\u041e\u0440\u0438\u0435\u043d\u0442\u0430\u0446\u0438\u044f (\u041e)", None))
        self.labelInfoActivity.setText(QCoreApplication.translate("FrmConfigDevicePane", u"?", None))
        self.checkBoxFreefall.setText(QCoreApplication.translate("FrmConfigDevicePane", u"\u041d\u0435\u0432\u0435\u0441\u043e\u043c\u043e\u0441\u0442\u044c (\u041d)", None))
        self.labelInfoFreefall.setText(QCoreApplication.translate("FrmConfigDevicePane", u"?", None))
        self.labelInfoSens.setText(QCoreApplication.translate("FrmConfigDevicePane", u"?", None))
    # retranslateUi

