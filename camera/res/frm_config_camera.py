# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'frm_config_cameragQqXBn.ui'
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
    QGridLayout, QHBoxLayout, QLabel, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_FrmConfigCamera(object):
    def setupUi(self, FrmConfigCamera):
        if not FrmConfigCamera.objectName():
            FrmConfigCamera.setObjectName(u"FrmConfigCamera")
        FrmConfigCamera.resize(577, 449)
        self.gridLayout = QGridLayout(FrmConfigCamera)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.labelCamera = QLabel(FrmConfigCamera)
        self.labelCamera.setObjectName(u"labelCamera")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.labelCamera)

        self.comboBoxSwitch = QComboBox(FrmConfigCamera)
        self.comboBoxSwitch.setObjectName(u"comboBoxSwitch")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.comboBoxSwitch)

        self.comboBoxCameras = QComboBox(FrmConfigCamera)
        self.comboBoxCameras.setObjectName(u"comboBoxCameras")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.comboBoxCameras)

        self.labelEnabledCamera = QLabel(FrmConfigCamera)
        self.labelEnabledCamera.setObjectName(u"labelEnabledCamera")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.labelEnabledCamera)


        self.verticalLayout.addLayout(self.formLayout)

        self.label = QLabel(FrmConfigCamera)
        self.label.setObjectName(u"label")
        self.label.setStyleSheet(u"color: #7f8c8d; font-style: italic; font-size: 11px;")

        self.verticalLayout.addWidget(self.label)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.pushButtonOk = QPushButton(FrmConfigCamera)
        self.pushButtonOk.setObjectName(u"pushButtonOk")

        self.horizontalLayout.addWidget(self.pushButtonOk)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)


        self.retranslateUi(FrmConfigCamera)

        QMetaObject.connectSlotsByName(FrmConfigCamera)
    # setupUi

    def retranslateUi(self, FrmConfigCamera):
        FrmConfigCamera.setWindowTitle(QCoreApplication.translate("FrmConfigCamera", u"\u041a\u0430\u043c\u0435\u0440\u0430", None))
        self.labelCamera.setText(QCoreApplication.translate("FrmConfigCamera", u"\u0421\u0442\u0430\u0442\u0443\u0441 \u043a\u0430\u043c\u0435\u0440\u044b:", None))
        self.labelEnabledCamera.setText(QCoreApplication.translate("FrmConfigCamera", u"\u0414\u043e\u0441\u0442\u0443\u043f\u043d\u044b\u0435 \u043a\u0430\u043c\u0435\u0440\u044b:", None))
        self.label.setText(QCoreApplication.translate("FrmConfigCamera", u"* \u0417\u0430\u043f\u0438\u0441\u044c \u0441 \u043a\u0430\u043c\u0435\u0440\u044b \u0432\u0435\u0434\u0451\u0442\u0441\u044f \u0441\u0438\u043d\u0445\u0440\u043e\u043d\u043d\u043e \u0441 \u0437\u0430\u043f\u0438\u0441\u044c\u044e \u0441\u0438\u0433\u043d\u0430\u043b\u043e\u0432 \u0438 \u0441\u043e\u0445\u0440\u0430\u043d\u044f\u0435\u0442\u0441\u044f \u0432 \u0442\u0443 \u0436\u0435 \u043f\u0430\u043f\u043a\u0443.", None))
        self.pushButtonOk.setText(QCoreApplication.translate("FrmConfigCamera", u"\u041f\u0440\u0438\u043c\u0435\u043d\u0438\u0442\u044c", None))
    # retranslateUi

