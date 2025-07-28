# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_windoweNiSRi.ui'
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
    QHBoxLayout, QLabel, QMainWindow, QMenuBar,
    QPushButton, QSizePolicy, QSpacerItem, QStatusBar,
    QVBoxLayout, QWidget)

from pyqtgraph import PlotWidget

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(796, 592)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.plotWidget = PlotWidget(self.centralwidget)
        self.plotWidget.setObjectName(u"plotWidget")

        self.horizontalLayout.addWidget(self.plotWidget)


        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.pushButtonManage = QPushButton(self.centralwidget)
        self.pushButtonManage.setObjectName(u"pushButtonManage")

        self.verticalLayout.addWidget(self.pushButtonManage)

        self.pushButtonStart = QPushButton(self.centralwidget)
        self.pushButtonStart.setObjectName(u"pushButtonStart")
        self.pushButtonStart.setEnabled(False)

        self.verticalLayout.addWidget(self.pushButtonStart)

        self.pushButtonStop = QPushButton(self.centralwidget)
        self.pushButtonStop.setObjectName(u"pushButtonStop")
        self.pushButtonStop.setEnabled(False)

        self.verticalLayout.addWidget(self.pushButtonStop)

        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_2.addWidget(self.label)

        self.comboBoxFormat = QComboBox(self.centralwidget)
        self.comboBoxFormat.addItem("")
        self.comboBoxFormat.addItem("")
        self.comboBoxFormat.setObjectName(u"comboBoxFormat")
        self.comboBoxFormat.setEnabled(False)

        self.horizontalLayout_2.addWidget(self.comboBoxFormat)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.pushButtonRecording = QPushButton(self.centralwidget)
        self.pushButtonRecording.setObjectName(u"pushButtonRecording")
        self.pushButtonRecording.setEnabled(False)

        self.verticalLayout.addWidget(self.pushButtonRecording)

        self.line_2 = QFrame(self.centralwidget)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line_2)

        self.labelDeviceInformation = QLabel(self.centralwidget)
        self.labelDeviceInformation.setObjectName(u"labelDeviceInformation")

        self.verticalLayout.addWidget(self.labelDeviceInformation)

        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.labelStatus = QLabel(self.centralwidget)
        self.labelStatus.setObjectName(u"labelStatus")

        self.gridLayout_3.addWidget(self.labelStatus, 3, 0, 1, 1)

        self.labelSerialNumberValue = QLabel(self.centralwidget)
        self.labelSerialNumberValue.setObjectName(u"labelSerialNumberValue")

        self.gridLayout_3.addWidget(self.labelSerialNumberValue, 1, 1, 1, 1)

        self.labelSerialNumber = QLabel(self.centralwidget)
        self.labelSerialNumber.setObjectName(u"labelSerialNumber")

        self.gridLayout_3.addWidget(self.labelSerialNumber, 1, 0, 1, 1)

        self.labelStatusValue = QLabel(self.centralwidget)
        self.labelStatusValue.setObjectName(u"labelStatusValue")

        self.gridLayout_3.addWidget(self.labelStatusValue, 3, 1, 1, 1)

        self.labelModel = QLabel(self.centralwidget)
        self.labelModel.setObjectName(u"labelModel")

        self.gridLayout_3.addWidget(self.labelModel, 2, 0, 1, 1)

        self.labelModelValue = QLabel(self.centralwidget)
        self.labelModelValue.setObjectName(u"labelModelValue")

        self.gridLayout_3.addWidget(self.labelModelValue, 2, 1, 1, 1)

        self.labelName = QLabel(self.centralwidget)
        self.labelName.setObjectName(u"labelName")

        self.gridLayout_3.addWidget(self.labelName, 0, 0, 1, 1)

        self.labelNameValue = QLabel(self.centralwidget)
        self.labelNameValue.setObjectName(u"labelNameValue")

        self.gridLayout_3.addWidget(self.labelNameValue, 0, 1, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout_3)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.gridLayout.addLayout(self.verticalLayout, 0, 1, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 796, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.pushButtonManage.setText(QCoreApplication.translate("MainWindow", u"Connect", None))
        self.pushButtonStart.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.pushButtonStop.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Format:", None))
        self.comboBoxFormat.setItemText(0, QCoreApplication.translate("MainWindow", u"WFDB", None))
        self.comboBoxFormat.setItemText(1, QCoreApplication.translate("MainWindow", u"EDF", None))

        self.pushButtonRecording.setText(QCoreApplication.translate("MainWindow", u"Start Recording", None))
        self.labelDeviceInformation.setText(QCoreApplication.translate("MainWindow", u"Device Information", None))
        self.labelStatus.setText(QCoreApplication.translate("MainWindow", u"Status:", None))
        self.labelSerialNumberValue.setText(QCoreApplication.translate("MainWindow", u"None", None))
        self.labelSerialNumber.setText(QCoreApplication.translate("MainWindow", u"Serial:", None))
        self.labelStatusValue.setText(QCoreApplication.translate("MainWindow", u"Not connected", None))
        self.labelModel.setText(QCoreApplication.translate("MainWindow", u"Model:", None))
        self.labelModelValue.setText(QCoreApplication.translate("MainWindow", u"None", None))
        self.labelName.setText(QCoreApplication.translate("MainWindow", u"Name:", None))
        self.labelNameValue.setText(QCoreApplication.translate("MainWindow", u"None", None))
    # retranslateUi

