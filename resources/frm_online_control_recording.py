# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'frm_online_control_recordingiXneTI.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFormLayout, QFrame,
    QGridLayout, QGroupBox, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QVBoxLayout, QWidget)

class Ui_FrmOnlineControlRecording(object):
    def setupUi(self, FrmOnlineControlRecording):
        if not FrmOnlineControlRecording.objectName():
            FrmOnlineControlRecording.setObjectName(u"FrmOnlineControlRecording")
        FrmOnlineControlRecording.resize(370, 217)
        FrmOnlineControlRecording.setFrameShape(QFrame.Shape.Panel)
        FrmOnlineControlRecording.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_2 = QGridLayout(FrmOnlineControlRecording)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.groupBox = QGroupBox(FrmOnlineControlRecording)
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
        self.gridLayout = QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.labelFormat = QLabel(self.groupBox)
        self.labelFormat.setObjectName(u"labelFormat")
        self.labelFormat.setFont(font)

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.labelFormat)

        self.comboBoxFormat = QComboBox(self.groupBox)
        self.comboBoxFormat.setObjectName(u"comboBoxFormat")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.comboBoxFormat.sizePolicy().hasHeightForWidth())
        self.comboBoxFormat.setSizePolicy(sizePolicy1)
        self.comboBoxFormat.setFont(font)

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.comboBoxFormat)

        self.labelTime = QLabel(self.groupBox)
        self.labelTime.setObjectName(u"labelTime")
        self.labelTime.setFont(font)

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.labelTime)

        self.labelRTValue = QLabel(self.groupBox)
        self.labelRTValue.setObjectName(u"labelRTValue")
        self.labelRTValue.setFont(font)
        self.labelRTValue.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.labelRTValue)


        self.verticalLayout.addLayout(self.formLayout)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pushButtonStartRecording = QPushButton(self.groupBox)
        self.pushButtonStartRecording.setObjectName(u"pushButtonStartRecording")
        self.pushButtonStartRecording.setEnabled(False)
        self.pushButtonStartRecording.setFont(font)

        self.horizontalLayout.addWidget(self.pushButtonStartRecording)

        self.pushButtonStopRecording = QPushButton(self.groupBox)
        self.pushButtonStopRecording.setObjectName(u"pushButtonStopRecording")
        self.pushButtonStopRecording.setEnabled(False)
        self.pushButtonStopRecording.setFont(font)

        self.horizontalLayout.addWidget(self.pushButtonStopRecording)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)


        self.gridLayout_2.addWidget(self.groupBox, 0, 0, 1, 1)


        self.retranslateUi(FrmOnlineControlRecording)

        QMetaObject.connectSlotsByName(FrmOnlineControlRecording)
    # setupUi

    def retranslateUi(self, FrmOnlineControlRecording):
        FrmOnlineControlRecording.setWindowTitle(QCoreApplication.translate("FrmOnlineControlRecording", u"Frame", None))
        self.groupBox.setTitle(QCoreApplication.translate("FrmOnlineControlRecording", u"\u0417\u0430\u043f\u0438\u0441\u044c \u0441\u0438\u0433\u043d\u0430\u043b\u0430 \u042d\u041a\u0413", None))
        self.labelFormat.setText(QCoreApplication.translate("FrmOnlineControlRecording", u"\u0424\u043e\u0440\u043c\u0430\u0442 \u0437\u0430\u043f\u0438\u0441\u0438", None))
        self.labelTime.setText(QCoreApplication.translate("FrmOnlineControlRecording", u"\u0412\u0440\u0435\u043c\u044f \u0437\u0430\u043f\u0438\u0441\u0438", None))
        self.labelRTValue.setText(QCoreApplication.translate("FrmOnlineControlRecording", u"00:00:00", None))
        self.pushButtonStartRecording.setText(QCoreApplication.translate("FrmOnlineControlRecording", u"\u041d\u0430\u0447\u0430\u0442\u044c \u0437\u0430\u043f\u0438\u0441\u044c", None))
        self.pushButtonStopRecording.setText(QCoreApplication.translate("FrmOnlineControlRecording", u"\u041e\u0441\u0442\u0430\u043d\u043e\u0432\u0438\u0442\u044c \u0437\u0430\u043f\u0438\u0441\u044c", None))
    # retranslateUi

