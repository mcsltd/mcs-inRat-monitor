# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'frm_control_recordingjKZBdr.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
    QLabel, QPushButton, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_frmControlRecording(object):
    def setupUi(self, frmControlRecording):
        if not frmControlRecording.objectName():
            frmControlRecording.setObjectName(u"frmControlRecording")
        frmControlRecording.resize(196, 124)
        self.gridLayout = QGridLayout(frmControlRecording)
        self.gridLayout.setObjectName(u"gridLayout")
        self.line_2 = QFrame(frmControlRecording)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)
        self.line_2.setFrameShape(QFrame.Shape.VLine)

        self.gridLayout.addWidget(self.line_2, 0, 0, 1, 1)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(3)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pushButtonStart = QPushButton(frmControlRecording)
        self.pushButtonStart.setObjectName(u"pushButtonStart")
        self.pushButtonStart.setEnabled(False)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonStart.sizePolicy().hasHeightForWidth())
        self.pushButtonStart.setSizePolicy(sizePolicy)
        self.pushButtonStart.setMaximumSize(QSize(75, 75))
        font = QFont()
        font.setPointSize(12)
        self.pushButtonStart.setFont(font)

        self.horizontalLayout.addWidget(self.pushButtonStart)

        self.pushButtonStop = QPushButton(frmControlRecording)
        self.pushButtonStop.setObjectName(u"pushButtonStop")
        self.pushButtonStop.setEnabled(False)
        sizePolicy.setHeightForWidth(self.pushButtonStop.sizePolicy().hasHeightForWidth())
        self.pushButtonStop.setSizePolicy(sizePolicy)
        self.pushButtonStop.setMaximumSize(QSize(75, 75))
        self.pushButtonStop.setFont(font)

        self.horizontalLayout.addWidget(self.pushButtonStop)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.label = QLabel(frmControlRecording)
        self.label.setObjectName(u"label")
        self.label.setMaximumSize(QSize(16777215, 15))
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.label)


        self.gridLayout.addLayout(self.verticalLayout, 0, 1, 1, 1)

        self.line = QFrame(frmControlRecording)
        self.line.setObjectName(u"line")
        self.line.setFrameShadow(QFrame.Shadow.Sunken)
        self.line.setFrameShape(QFrame.Shape.VLine)

        self.gridLayout.addWidget(self.line, 0, 2, 1, 1)


        self.retranslateUi(frmControlRecording)

        QMetaObject.connectSlotsByName(frmControlRecording)
    # setupUi

    def retranslateUi(self, frmControlRecording):
        frmControlRecording.setWindowTitle(QCoreApplication.translate("frmControlRecording", u"Frame", None))
        self.pushButtonStart.setText(QCoreApplication.translate("frmControlRecording", u"\u041d\u0430\u0447\u0430\u0442\u044c \n"
"\u0437\u0430\u043f\u0438\u0441\u044c", None))
        self.pushButtonStop.setText(QCoreApplication.translate("frmControlRecording", u"\u041e\u0441\u0442\u0430\u043d\u043e\u0432\u0438\u0442\u044c \n"
"\u0437\u0430\u043f\u0438\u0441\u044c", None))
        self.label.setText(QCoreApplication.translate("frmControlRecording", u"\u0417\u0430\u043f\u0438\u0441\u044c", None))
    # retranslateUi

