# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'frm_control_scannerIxWGiZ.ui'
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
import resources.resources_rc

class Ui_FrmControlScanner(object):
    def setupUi(self, FrmControlScanner):
        if not FrmControlScanner.objectName():
            FrmControlScanner.setObjectName(u"FrmControlScanner")
        FrmControlScanner.resize(114, 116)
        self.horizontalLayout_2 = QHBoxLayout(FrmControlScanner)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.pushButtonStart = QPushButton(FrmControlScanner)
        self.pushButtonStart.setObjectName(u"pushButtonStart")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonStart.sizePolicy().hasHeightForWidth())
        self.pushButtonStart.setSizePolicy(sizePolicy)
        self.pushButtonStart.setMinimumSize(QSize(75, 75))
        self.pushButtonStart.setMaximumSize(QSize(75, 75))
        self.pushButtonStart.setStyleSheet(u"QPushButton {\n"
"    background-color: transparent;\n"
"    border: none;\n"
"}")
        icon = QIcon()
        icon.addFile(u":/images/search.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButtonStart.setIcon(icon)
        self.pushButtonStart.setIconSize(QSize(50, 50))
        self.pushButtonStart.setAutoRepeat(False)

        self.verticalLayout.addWidget(self.pushButtonStart)

        self.labelSearch = QLabel(FrmControlScanner)
        self.labelSearch.setObjectName(u"labelSearch")
        sizePolicy.setHeightForWidth(self.labelSearch.sizePolicy().hasHeightForWidth())
        self.labelSearch.setSizePolicy(sizePolicy)
        self.labelSearch.setMaximumSize(QSize(16777215, 15))
        self.labelSearch.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.labelSearch)


        self.horizontalLayout_2.addLayout(self.verticalLayout)


        self.retranslateUi(FrmControlScanner)

        QMetaObject.connectSlotsByName(FrmControlScanner)
    # setupUi

    def retranslateUi(self, FrmControlScanner):
        FrmControlScanner.setWindowTitle(QCoreApplication.translate("FrmControlScanner", u"Frame", None))
        self.pushButtonStart.setText("")
        self.labelSearch.setText(QCoreApplication.translate("FrmControlScanner", u"\u041f\u043e\u0438\u0441\u043a", None))
    # retranslateUi

