# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'frm_control_xy_rangeCHvbEF.ui'
##
## Created by: Qt User Interface Compiler version 6.9.2
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
    QHBoxLayout, QLabel, QSizePolicy, QWidget)

class Ui_FrmControlXYRange(object):
    def setupUi(self, FrmControlXYRange):
        if not FrmControlXYRange.objectName():
            FrmControlXYRange.setObjectName(u"FrmControlXYRange")
        FrmControlXYRange.resize(261, 41)
        self.gridLayout = QGridLayout(FrmControlXYRange)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(5)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.labelXRange = QLabel(FrmControlXYRange)
        self.labelXRange.setObjectName(u"labelXRange")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelXRange.sizePolicy().hasHeightForWidth())
        self.labelXRange.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.labelXRange)

        self.comboBoxXRange = QComboBox(FrmControlXYRange)
        self.comboBoxXRange.setObjectName(u"comboBoxXRange")
        sizePolicy.setHeightForWidth(self.comboBoxXRange.sizePolicy().hasHeightForWidth())
        self.comboBoxXRange.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.comboBoxXRange)

        self.labelYRange = QLabel(FrmControlXYRange)
        self.labelYRange.setObjectName(u"labelYRange")
        sizePolicy.setHeightForWidth(self.labelYRange.sizePolicy().hasHeightForWidth())
        self.labelYRange.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.labelYRange)

        self.comboBoxYRange = QComboBox(FrmControlXYRange)
        self.comboBoxYRange.setObjectName(u"comboBoxYRange")
        sizePolicy.setHeightForWidth(self.comboBoxYRange.sizePolicy().hasHeightForWidth())
        self.comboBoxYRange.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.comboBoxYRange)


        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)


        self.retranslateUi(FrmControlXYRange)

        QMetaObject.connectSlotsByName(FrmControlXYRange)
    # setupUi

    def retranslateUi(self, FrmControlXYRange):
        FrmControlXYRange.setWindowTitle(QCoreApplication.translate("FrmControlXYRange", u"FrmControlXYRange", None))
        self.labelXRange.setText(QCoreApplication.translate("FrmControlXYRange", u"\u041e\u0441\u044c X:", None))
        self.labelYRange.setText(QCoreApplication.translate("FrmControlXYRange", u"\u041e\u0441\u044c Y:", None))
    # retranslateUi

