# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'frm_online_displaypBXaVW.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QGridLayout,
    QGroupBox, QLabel, QSizePolicy, QWidget)

class Ui_FrmDisplay(object):
    def setupUi(self, FrmDisplay):
        if not FrmDisplay.objectName():
            FrmDisplay.setObjectName(u"FrmDisplay")
        FrmDisplay.resize(384, 148)
        self.gridLayout_3 = QGridLayout(FrmDisplay)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(5, 5, 5, 5)
        self.groupBox = QGroupBox(FrmDisplay)
        self.groupBox.setObjectName(u"groupBox")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setMinimumSize(QSize(350, 120))
        font = QFont()
        font.setPointSize(12)
        self.groupBox.setFont(font)
        self.gridLayout_2 = QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_Display = QGridLayout()
        self.gridLayout_Display.setObjectName(u"gridLayout_Display")
        self.gridLayout_Display.setContentsMargins(10, 10, 10, 10)
        self.labelTimebase = QLabel(self.groupBox)
        self.labelTimebase.setObjectName(u"labelTimebase")

        self.gridLayout_Display.addWidget(self.labelTimebase, 0, 0, 1, 1)

        self.comboBoxTimebase = QComboBox(self.groupBox)
        self.comboBoxTimebase.setObjectName(u"comboBoxTimebase")

        self.gridLayout_Display.addWidget(self.comboBoxTimebase, 0, 1, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout_Display, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)


        self.gridLayout_3.addLayout(self.gridLayout, 0, 0, 1, 1)


        self.retranslateUi(FrmDisplay)

        QMetaObject.connectSlotsByName(FrmDisplay)
    # setupUi

    def retranslateUi(self, FrmDisplay):
        FrmDisplay.setWindowTitle(QCoreApplication.translate("FrmDisplay", u"Frame", None))
        self.groupBox.setTitle(QCoreApplication.translate("FrmDisplay", u"\u0414\u0438\u0441\u043f\u043b\u0435\u0439", None))
        self.labelTimebase.setText(QCoreApplication.translate("FrmDisplay", u"\u041e\u0441\u044c \"t\"", None))
    # retranslateUi

