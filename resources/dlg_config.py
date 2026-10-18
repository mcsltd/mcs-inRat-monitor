# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dlg_confignWBBBc.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QGridLayout, QSizePolicy,
    QTabWidget, QVBoxLayout, QWidget)
import resources.resources_rc

class Ui_DlgConfig(object):
    def setupUi(self, DlgConfig):
        if not DlgConfig.objectName():
            DlgConfig.setObjectName(u"DlgConfig")
        DlgConfig.resize(756, 558)
        icon = QIcon()
        icon.addFile(u":/images/icon.ico", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        DlgConfig.setWindowIcon(icon)
        self.gridLayout = QGridLayout(DlgConfig)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tabWidget = QTabWidget(DlgConfig)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab1 = QWidget()
        self.tab1.setObjectName(u"tab1")
        self.tabWidget.addTab(self.tab1, "")

        self.verticalLayout.addWidget(self.tabWidget)


        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)


        self.retranslateUi(DlgConfig)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(DlgConfig)
    # setupUi

    def retranslateUi(self, DlgConfig):
        DlgConfig.setWindowTitle(QCoreApplication.translate("DlgConfig", u"\u041d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0430", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab1), QCoreApplication.translate("DlgConfig", u"\u0421\u0442\u0440\u0430\u043d\u0438\u0446\u0430", None))
    # retranslateUi

