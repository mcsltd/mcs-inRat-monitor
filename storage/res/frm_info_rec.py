# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'frm_info_reckrBMJK.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QWidget)
import resources.resources_rc

class Ui_FrmInfoRecording(object):
    def setupUi(self, FrmInfoRecording):
        if not FrmInfoRecording.objectName():
            FrmInfoRecording.setObjectName(u"FrmInfoRecording")
        FrmInfoRecording.resize(240, 45)
        self.horizontalLayout_2 = QHBoxLayout(FrmInfoRecording)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pushButton = QPushButton(FrmInfoRecording)
        self.pushButton.setObjectName(u"pushButton")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setMaximumSize(QSize(25, 25))
        font = QFont()
        font.setPointSize(11)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet(u"QPushButton {\n"
"    background-color: transparent;\n"
"    border: none;\n"
"}")
        icon = QIcon()
        icon.addFile(u":/images/record.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton.setIcon(icon)

        self.horizontalLayout.addWidget(self.pushButton)

        self.labelRecTime = QLabel(FrmInfoRecording)
        self.labelRecTime.setObjectName(u"labelRecTime")
        self.labelRecTime.setFont(font)
        self.labelRecTime.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout.addWidget(self.labelRecTime)

        self.labelFileCnt = QLabel(FrmInfoRecording)
        self.labelFileCnt.setObjectName(u"labelFileCnt")
        self.labelFileCnt.setFont(font)
        self.labelFileCnt.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout.addWidget(self.labelFileCnt)


        self.horizontalLayout_2.addLayout(self.horizontalLayout)


        self.retranslateUi(FrmInfoRecording)

        QMetaObject.connectSlotsByName(FrmInfoRecording)
    # setupUi

    def retranslateUi(self, FrmInfoRecording):
        FrmInfoRecording.setWindowTitle(QCoreApplication.translate("FrmInfoRecording", u"Frame", None))
        self.pushButton.setText("")
        self.labelRecTime.setText(QCoreApplication.translate("FrmInfoRecording", u"00:00/00:00", None))
        self.labelFileCnt.setText(QCoreApplication.translate("FrmInfoRecording", u"0", None))
    # retranslateUi

