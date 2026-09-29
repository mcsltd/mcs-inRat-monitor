# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'frm_control_scannerUwyxVP.ui'
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

class Ui_FrmControlScanner(object):
    def setupUi(self, FrmControlScanner):
        if not FrmControlScanner.objectName():
            FrmControlScanner.setObjectName(u"FrmControlScanner")
        FrmControlScanner.resize(100, 125)
        self.horizontalLayout_2 = QHBoxLayout(FrmControlScanner)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.pushButtonStart = QPushButton(FrmControlScanner)
        self.pushButtonStart.setObjectName(u"pushButtonStart")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonStart.sizePolicy().hasHeightForWidth())
        self.pushButtonStart.setSizePolicy(sizePolicy)
        self.pushButtonStart.setMinimumSize(QSize(75, 75))
        self.pushButtonStart.setMaximumSize(QSize(75, 75))

        self.verticalLayout.addWidget(self.pushButtonStart)

        self.labelSearch = QLabel(FrmControlScanner)
        self.labelSearch.setObjectName(u"labelSearch")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.labelSearch.sizePolicy().hasHeightForWidth())
        self.labelSearch.setSizePolicy(sizePolicy1)
        self.labelSearch.setMaximumSize(QSize(16777215, 15))
        self.labelSearch.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.labelSearch)


        self.horizontalLayout_2.addLayout(self.verticalLayout)


        self.retranslateUi(FrmControlScanner)

        QMetaObject.connectSlotsByName(FrmControlScanner)
    # setupUi

    def retranslateUi(self, FrmControlScanner):
        FrmControlScanner.setWindowTitle(QCoreApplication.translate("FrmControlScanner", u"Frame", None))
        self.pushButtonStart.setText(QCoreApplication.translate("FrmControlScanner", u"\u041f\u043e\u0438\u0441\u043a", None))
        self.labelSearch.setText(QCoreApplication.translate("FrmControlScanner", u"\u041f\u043e\u0438\u0441\u043a", None))
    # retranslateUi

