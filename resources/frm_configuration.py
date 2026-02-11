# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'frm_configurationJWoPdF.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QGridLayout, QSizePolicy, QTabWidget, QWidget)

class Ui_frmConfiguration(object):
    def setupUi(self, frmConfiguration):
        if not frmConfiguration.objectName():
            frmConfiguration.setObjectName(u"frmConfiguration")
        frmConfiguration.resize(659, 416)
        self.gridLayout = QGridLayout(frmConfiguration)
        self.gridLayout.setObjectName(u"gridLayout")
        self.tabWidget = QTabWidget(frmConfiguration)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.tabWidget.addTab(self.tab, "")

        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)

        self.buttonBox = QDialogButtonBox(frmConfiguration)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Ok)

        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)


        self.retranslateUi(frmConfiguration)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(frmConfiguration)
    # setupUi

    def retranslateUi(self, frmConfiguration):
        frmConfiguration.setWindowTitle(QCoreApplication.translate("frmConfiguration", u"Configuration", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("frmConfiguration", u"Tab 1", None))
    # retranslateUi

