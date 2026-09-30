# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'frm_control_recordingXcUxLy.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QVBoxLayout, QWidget)

class Ui_frmControlRecording(object):
    def setupUi(self, frmControlRecording):
        if not frmControlRecording.objectName():
            frmControlRecording.setObjectName(u"frmControlRecording")
        frmControlRecording.resize(178, 124)
        self.verticalLayout_2 = QVBoxLayout(frmControlRecording)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pushButtonStartRecord = QPushButton(frmControlRecording)
        self.pushButtonStartRecord.setObjectName(u"pushButtonStartRecord")
        self.pushButtonStartRecord.setEnabled(False)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonStartRecord.sizePolicy().hasHeightForWidth())
        self.pushButtonStartRecord.setSizePolicy(sizePolicy)
        self.pushButtonStartRecord.setMaximumSize(QSize(75, 75))

        self.horizontalLayout.addWidget(self.pushButtonStartRecord)

        self.pushButtonStopRecord = QPushButton(frmControlRecording)
        self.pushButtonStopRecord.setObjectName(u"pushButtonStopRecord")
        self.pushButtonStopRecord.setEnabled(False)
        sizePolicy.setHeightForWidth(self.pushButtonStopRecord.sizePolicy().hasHeightForWidth())
        self.pushButtonStopRecord.setSizePolicy(sizePolicy)
        self.pushButtonStopRecord.setMaximumSize(QSize(75, 75))

        self.horizontalLayout.addWidget(self.pushButtonStopRecord)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.label = QLabel(frmControlRecording)
        self.label.setObjectName(u"label")
        self.label.setMaximumSize(QSize(16777215, 15))
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.label)


        self.verticalLayout_2.addLayout(self.verticalLayout)


        self.retranslateUi(frmControlRecording)

        QMetaObject.connectSlotsByName(frmControlRecording)
    # setupUi

    def retranslateUi(self, frmControlRecording):
        frmControlRecording.setWindowTitle(QCoreApplication.translate("frmControlRecording", u"Frame", None))
        self.pushButtonStartRecord.setText(QCoreApplication.translate("frmControlRecording", u"\u041d\u0430\u0447\u0430\u0442\u044c \n"
"\u0437\u0430\u043f\u0438\u0441\u044c", None))
        self.pushButtonStopRecord.setText(QCoreApplication.translate("frmControlRecording", u"\u041e\u0441\u0442\u0430\u043d\u043e\u0432\u0438\u0442\u044c \n"
"\u0437\u0430\u043f\u0438\u0441\u044c", None))
        self.label.setText(QCoreApplication.translate("frmControlRecording", u"\u0417\u0430\u043f\u0438\u0441\u044c", None))
    # retranslateUi

