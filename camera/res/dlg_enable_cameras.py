# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dlg_enable_camerasuVUeZy.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QGridLayout, QHBoxLayout,
    QLabel, QListWidget, QListWidgetItem, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_DlgCameras(object):
    def setupUi(self, DlgCameras):
        if not DlgCameras.objectName():
            DlgCameras.setObjectName(u"DlgCameras")
        DlgCameras.resize(314, 421)
        self.gridLayout = QGridLayout(DlgCameras)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(DlgCameras)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.listWidgetFoundCameras = QListWidget(DlgCameras)
        self.listWidgetFoundCameras.setObjectName(u"listWidgetFoundCameras")

        self.verticalLayout.addWidget(self.listWidgetFoundCameras)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.pushButtonOpen = QPushButton(DlgCameras)
        self.pushButtonOpen.setObjectName(u"pushButtonOpen")
        self.pushButtonOpen.setEnabled(False)

        self.horizontalLayout.addWidget(self.pushButtonOpen)

        self.pushButtonReset = QPushButton(DlgCameras)
        self.pushButtonReset.setObjectName(u"pushButtonReset")
        self.pushButtonReset.setEnabled(False)

        self.horizontalLayout.addWidget(self.pushButtonReset)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)


        self.retranslateUi(DlgCameras)

        QMetaObject.connectSlotsByName(DlgCameras)
    # setupUi

    def retranslateUi(self, DlgCameras):
        DlgCameras.setWindowTitle(QCoreApplication.translate("DlgCameras", u"\u041f\u043e\u0438\u0441\u043a \u0438 \u043f\u043e\u0434\u043a\u043b\u044e\u0447\u0435\u043d\u0438\u0435", None))
        self.label.setText(QCoreApplication.translate("DlgCameras", u"\u0414\u043e\u0441\u0442\u0443\u043f\u043d\u044b\u0435 \u043a\u0430\u043c\u0435\u0440\u044b:", None))
        self.pushButtonOpen.setText(QCoreApplication.translate("DlgCameras", u"\u041e\u0442\u043a\u0440\u044b\u0442\u044c", None))
        self.pushButtonReset.setText(QCoreApplication.translate("DlgCameras", u"\u041e\u0447\u0438\u0441\u0442\u0438\u0442\u044c", None))
    # retranslateUi

