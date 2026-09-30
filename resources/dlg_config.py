# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dlg_configMMmnCN.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QGridLayout, QHBoxLayout,
    QPushButton, QSizePolicy, QSpacerItem, QTabWidget,
    QVBoxLayout, QWidget)

class Ui_DlgConfig(object):
    def setupUi(self, DlgConfig):
        if not DlgConfig.objectName():
            DlgConfig.setObjectName(u"DlgConfig")
        DlgConfig.resize(756, 558)
        self.gridLayout = QGridLayout(DlgConfig)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tabWidget = QTabWidget(DlgConfig)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabDevice = QWidget()
        self.tabDevice.setObjectName(u"tabDevice")
        self.gridLayout_2 = QGridLayout(self.tabDevice)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")

        self.gridLayout_2.addLayout(self.verticalLayout_2, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tabDevice, "")
        self.tabStorage = QWidget()
        self.tabStorage.setObjectName(u"tabStorage")
        self.gridLayout_3 = QGridLayout(self.tabStorage)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")

        self.gridLayout_3.addLayout(self.verticalLayout_3, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tabStorage, "")

        self.verticalLayout.addWidget(self.tabWidget)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.pushButtonCancel = QPushButton(DlgConfig)
        self.pushButtonCancel.setObjectName(u"pushButtonCancel")

        self.horizontalLayout.addWidget(self.pushButtonCancel)

        self.pushButtonOk = QPushButton(DlgConfig)
        self.pushButtonOk.setObjectName(u"pushButtonOk")

        self.horizontalLayout.addWidget(self.pushButtonOk)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)


        self.retranslateUi(DlgConfig)

        self.tabWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(DlgConfig)
    # setupUi

    def retranslateUi(self, DlgConfig):
        DlgConfig.setWindowTitle(QCoreApplication.translate("DlgConfig", u"\u041d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0430", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabDevice), QCoreApplication.translate("DlgConfig", u"inRat", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabStorage), QCoreApplication.translate("DlgConfig", u"\u0417\u0430\u043f\u0438\u0441\u044c", None))
        self.pushButtonCancel.setText(QCoreApplication.translate("DlgConfig", u"\u041e\u043a", None))
        self.pushButtonOk.setText(QCoreApplication.translate("DlgConfig", u"\u041e\u0442\u043c\u0435\u043d\u0438\u0442\u044c", None))
    # retranslateUi

