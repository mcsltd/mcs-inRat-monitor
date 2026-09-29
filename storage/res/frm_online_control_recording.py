# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'frm_online_control_recordingFLRMKd.ui'
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
from PySide6.QtWidgets import (QApplication, QFormLayout, QFrame, QGridLayout,
    QGroupBox, QHBoxLayout, QLabel, QPushButton,
    QSizePolicy, QVBoxLayout, QWidget)

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

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.labelFormat)

        self.labelTime = QLabel(self.groupBox)
        self.labelTime.setObjectName(u"labelTime")
        self.labelTime.setFont(font)

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.labelTime)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.labelRecordingTime = QLabel(self.groupBox)
        self.labelRecordingTime.setObjectName(u"labelRecordingTime")
        self.labelRecordingTime.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_2.addWidget(self.labelRecordingTime)


        self.formLayout.setLayout(2, QFormLayout.ItemRole.FieldRole, self.horizontalLayout_2)

        self.labelFormatValue = QLabel(self.groupBox)
        self.labelFormatValue.setObjectName(u"labelFormatValue")
        self.labelFormatValue.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.labelFormatValue)

        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label_2)

        self.pushButtonSelectSaveDir = QPushButton(self.groupBox)
        self.pushButtonSelectSaveDir.setObjectName(u"pushButtonSelectSaveDir")
        self.pushButtonSelectSaveDir.setEnabled(False)

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.pushButtonSelectSaveDir)

        self.labelCounter = QLabel(self.groupBox)
        self.labelCounter.setObjectName(u"labelCounter")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.labelCounter)

        self.labelFileCounter = QLabel(self.groupBox)
        self.labelFileCounter.setObjectName(u"labelFileCounter")
        self.labelFileCounter.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.formLayout.setWidget(3, QFormLayout.ItemRole.FieldRole, self.labelFileCounter)


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

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.pushButtonOpenArchive = QPushButton(self.groupBox)
        self.pushButtonOpenArchive.setObjectName(u"pushButtonOpenArchive")
        self.pushButtonOpenArchive.setEnabled(False)

        self.verticalLayout_2.addWidget(self.pushButtonOpenArchive)


        self.verticalLayout.addLayout(self.verticalLayout_2)


        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)


        self.gridLayout_2.addWidget(self.groupBox, 0, 0, 1, 1)


        self.retranslateUi(FrmOnlineControlRecording)

        QMetaObject.connectSlotsByName(FrmOnlineControlRecording)
    # setupUi

    def retranslateUi(self, FrmOnlineControlRecording):
        FrmOnlineControlRecording.setWindowTitle(QCoreApplication.translate("FrmOnlineControlRecording", u"Frame", None))
        self.groupBox.setTitle(QCoreApplication.translate("FrmOnlineControlRecording", u"\u0417\u0430\u043f\u0438\u0441\u044c \u0434\u0430\u043d\u043d\u044b\u0445", None))
        self.labelFormat.setText(QCoreApplication.translate("FrmOnlineControlRecording", u"\u0424\u043e\u0440\u043c\u0430\u0442 \u0437\u0430\u043f\u0438\u0441\u0438", None))
        self.labelTime.setText(QCoreApplication.translate("FrmOnlineControlRecording", u"\u0412\u0440\u0435\u043c\u044f \u0437\u0430\u043f\u0438\u0441\u0438", None))
        self.labelRecordingTime.setText(QCoreApplication.translate("FrmOnlineControlRecording", u"00:00:00", None))
        self.labelFormatValue.setText(QCoreApplication.translate("FrmOnlineControlRecording", u"EDF", None))
        self.label_2.setText(QCoreApplication.translate("FrmOnlineControlRecording", u"\u041c\u0435\u0441\u0442\u043e \u0441\u043e\u0445\u0440\u0430\u043d\u0435\u043d\u0438\u044f", None))
        self.pushButtonSelectSaveDir.setText(QCoreApplication.translate("FrmOnlineControlRecording", u"\u0412\u044b\u0431\u0440\u0430\u0442\u044c", None))
        self.labelCounter.setText(QCoreApplication.translate("FrmOnlineControlRecording", u"\u0417\u0430\u043f\u0438\u0441\u0435\u0439", None))
        self.labelFileCounter.setText(QCoreApplication.translate("FrmOnlineControlRecording", u"000", None))
        self.pushButtonStartRecording.setText(QCoreApplication.translate("FrmOnlineControlRecording", u"\u041d\u0430\u0447\u0430\u0442\u044c \u0437\u0430\u043f\u0438\u0441\u044c", None))
        self.pushButtonStopRecording.setText(QCoreApplication.translate("FrmOnlineControlRecording", u"\u041e\u0441\u0442\u0430\u043d\u043e\u0432\u0438\u0442\u044c \u0437\u0430\u043f\u0438\u0441\u044c", None))
        self.pushButtonOpenArchive.setText(QCoreApplication.translate("FrmOnlineControlRecording", u"\u0417\u0430\u043f\u0438\u0441\u0438", None))
    # retranslateUi

