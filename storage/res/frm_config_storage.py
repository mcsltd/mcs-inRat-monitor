# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'frm_config_storageISbqib.ui'
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
from PySide6.QtWidgets import (QApplication, QFormLayout, QFrame, QGridLayout,
    QGroupBox, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QSpinBox,
    QVBoxLayout, QWidget)

class Ui_FrmConfigStoragePane(object):
    def setupUi(self, FrmConfigStoragePane):
        if not FrmConfigStoragePane.objectName():
            FrmConfigStoragePane.setObjectName(u"FrmConfigStoragePane")
        FrmConfigStoragePane.resize(570, 508)
        self.gridLayout = QGridLayout(FrmConfigStoragePane)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBoxPath = QGroupBox(FrmConfigStoragePane)
        self.groupBoxPath.setObjectName(u"groupBoxPath")
        self.gridLayout_2 = QGridLayout(self.groupBoxPath)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.lineEditPath = QLineEdit(self.groupBoxPath)
        self.lineEditPath.setObjectName(u"lineEditPath")
        self.lineEditPath.setReadOnly(True)

        self.horizontalLayout_2.addWidget(self.lineEditPath)

        self.pushButtonPath = QPushButton(self.groupBoxPath)
        self.pushButtonPath.setObjectName(u"pushButtonPath")

        self.horizontalLayout_2.addWidget(self.pushButtonPath)


        self.gridLayout_2.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)


        self.verticalLayout.addWidget(self.groupBoxPath)

        self.groupBox_2 = QGroupBox(FrmConfigStoragePane)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.gridLayout_3 = QGridLayout(self.groupBox_2)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.labelDuration = QLabel(self.groupBox_2)
        self.labelDuration.setObjectName(u"labelDuration")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.labelDuration)

        self.spinBoxDuration = QSpinBox(self.groupBox_2)
        self.spinBoxDuration.setObjectName(u"spinBoxDuration")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.spinBoxDuration)

        self.label = QLabel(self.groupBox_2)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label)

        self.label_2 = QLabel(self.groupBox_2)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.label_2)


        self.gridLayout_3.addLayout(self.formLayout, 0, 0, 1, 1)


        self.verticalLayout.addWidget(self.groupBox_2)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_3)

        self.pushButtonOk = QPushButton(FrmConfigStoragePane)
        self.pushButtonOk.setObjectName(u"pushButtonOk")

        self.horizontalLayout.addWidget(self.pushButtonOk)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)


        self.retranslateUi(FrmConfigStoragePane)

        QMetaObject.connectSlotsByName(FrmConfigStoragePane)
    # setupUi

    def retranslateUi(self, FrmConfigStoragePane):
        FrmConfigStoragePane.setWindowTitle(QCoreApplication.translate("FrmConfigStoragePane", u"Frame", None))
        self.groupBoxPath.setTitle(QCoreApplication.translate("FrmConfigStoragePane", u"\u041c\u0435\u0441\u0442\u043e \u0441\u043e\u0445\u0440\u0430\u043d\u0435\u043d\u0438\u044f", None))
        self.pushButtonPath.setText(QCoreApplication.translate("FrmConfigStoragePane", u"\u041e\u0431\u0437\u043e\u0440", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("FrmConfigStoragePane", u"\u041f\u0430\u0440\u0430\u043c\u0435\u0442\u0440\u044b \u0437\u0430\u043f\u0438\u0441\u0438", None))
        self.labelDuration.setText(QCoreApplication.translate("FrmConfigStoragePane", u"\u0414\u043b\u0438\u0442\u0435\u043b\u044c\u043d\u043e\u0441\u0442\u044c \u0444\u0430\u0439\u043b\u0430", None))
        self.label.setText(QCoreApplication.translate("FrmConfigStoragePane", u"\u0424\u043e\u0440\u043c\u0430\u0442 \u0437\u0430\u043f\u0438\u0441\u0438", None))
        self.label_2.setText(QCoreApplication.translate("FrmConfigStoragePane", u"EDF", None))
        self.pushButtonOk.setText(QCoreApplication.translate("FrmConfigStoragePane", u"\u041f\u0440\u0438\u043c\u0435\u043d\u0438\u0442\u044c", None))
    # retranslateUi

