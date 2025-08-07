# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_windowfqUZiN.ui'
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
    QHBoxLayout, QLabel, QLineEdit, QMainWindow,
    QMenuBar, QPushButton, QSizePolicy, QSpacerItem,
    QStatusBar, QVBoxLayout, QWidget)

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
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.labelDevice = QLabel(self.centralwidget)
        self.labelDevice.setObjectName(u"labelDevice")

        self.horizontalLayout_3.addWidget(self.labelDevice)

        self.comboBoxDevice = QComboBox(self.centralwidget)
        self.comboBoxDevice.setObjectName(u"comboBoxDevice")

        self.horizontalLayout_3.addWidget(self.comboBoxDevice)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.pushButtonConnect = QPushButton(self.centralwidget)
        self.pushButtonConnect.setObjectName(u"pushButtonConnect")

        self.verticalLayout.addWidget(self.pushButtonConnect)

        self.pushButtonDisconnect = QPushButton(self.centralwidget)
        self.pushButtonDisconnect.setObjectName(u"pushButtonDisconnect")

        self.verticalLayout.addWidget(self.pushButtonDisconnect)

        self.line_3 = QFrame(self.centralwidget)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.Shape.HLine)
        self.line_3.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line_3)

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
        self.gridLayout_7 = QGridLayout()
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.labelDirSave = QLabel(self.centralwidget)
        self.labelDirSave.setObjectName(u"labelDirSave")
        self.labelDirSave.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_7.addWidget(self.labelDirSave, 0, 0, 1, 1)

        self.labelRT = QLabel(self.centralwidget)
        self.labelRT.setObjectName(u"labelRT")
        self.labelRT.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_7.addWidget(self.labelRT, 2, 0, 1, 1)

        self.labelFormat = QLabel(self.centralwidget)
        self.labelFormat.setObjectName(u"labelFormat")
        self.labelFormat.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_7.addWidget(self.labelFormat, 1, 0, 1, 1)

        self.labelRTvalue = QLabel(self.centralwidget)
        self.labelRTvalue.setObjectName(u"labelRTvalue")
        self.labelRTvalue.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_7.addWidget(self.labelRTvalue, 2, 1, 1, 1)

        self.comboBoxFormat = QComboBox(self.centralwidget)
        self.comboBoxFormat.addItem("")
        self.comboBoxFormat.addItem("")
        self.comboBoxFormat.setObjectName(u"comboBoxFormat")
        self.comboBoxFormat.setEnabled(False)

        self.gridLayout_7.addWidget(self.comboBoxFormat, 1, 1, 1, 1)

        self.lineEditSave = QLineEdit(self.centralwidget)
        self.lineEditSave.setObjectName(u"lineEditSave")
        self.lineEditSave.setEnabled(False)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditSave.sizePolicy().hasHeightForWidth())
        self.lineEditSave.setSizePolicy(sizePolicy)

        self.gridLayout_7.addWidget(self.lineEditSave, 0, 1, 1, 1)

        self.pushButtonSelectDirSave = QPushButton(self.centralwidget)
        self.pushButtonSelectDirSave.setObjectName(u"pushButtonSelectDirSave")
        self.pushButtonSelectDirSave.setEnabled(False)
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.pushButtonSelectDirSave.sizePolicy().hasHeightForWidth())
        self.pushButtonSelectDirSave.setSizePolicy(sizePolicy1)
        self.pushButtonSelectDirSave.setMinimumSize(QSize(5, 0))

        self.gridLayout_7.addWidget(self.pushButtonSelectDirSave, 0, 2, 1, 1)


        self.horizontalLayout_2.addLayout(self.gridLayout_7)


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
        self.labelDeviceInformation.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.labelDeviceInformation)

        self.gridLayout_5 = QGridLayout()
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.labelStatus = QLabel(self.centralwidget)
        self.labelStatus.setObjectName(u"labelStatus")

        self.gridLayout_5.addWidget(self.labelStatus, 3, 0, 1, 1)

        self.labelSerialNumberValue = QLabel(self.centralwidget)
        self.labelSerialNumberValue.setObjectName(u"labelSerialNumberValue")

        self.gridLayout_5.addWidget(self.labelSerialNumberValue, 1, 1, 1, 1)

        self.labelSerialNumber = QLabel(self.centralwidget)
        self.labelSerialNumber.setObjectName(u"labelSerialNumber")

        self.gridLayout_5.addWidget(self.labelSerialNumber, 1, 0, 1, 1)

        self.labelStatusValue = QLabel(self.centralwidget)
        self.labelStatusValue.setObjectName(u"labelStatusValue")

        self.gridLayout_5.addWidget(self.labelStatusValue, 3, 1, 1, 1)

        self.labelModel = QLabel(self.centralwidget)
        self.labelModel.setObjectName(u"labelModel")

        self.gridLayout_5.addWidget(self.labelModel, 2, 0, 1, 1)

        self.labelModelValue = QLabel(self.centralwidget)
        self.labelModelValue.setObjectName(u"labelModelValue")

        self.gridLayout_5.addWidget(self.labelModelValue, 2, 1, 1, 1)

        self.labelName = QLabel(self.centralwidget)
        self.labelName.setObjectName(u"labelName")

        self.gridLayout_5.addWidget(self.labelName, 0, 0, 1, 1)

        self.labelNameValue = QLabel(self.centralwidget)
        self.labelNameValue.setObjectName(u"labelNameValue")

        self.gridLayout_5.addWidget(self.labelNameValue, 0, 1, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout_5)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.gridLayout.addLayout(self.verticalLayout, 0, 1, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.plotWidget = PlotWidget(self.centralwidget)
        self.plotWidget.setObjectName(u"plotWidget")

        self.horizontalLayout.addWidget(self.plotWidget)


        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)

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
        self.labelDevice.setText(QCoreApplication.translate("MainWindow", u"Device:", None))
        self.pushButtonConnect.setText(QCoreApplication.translate("MainWindow", u"Connect", None))
        self.pushButtonDisconnect.setText(QCoreApplication.translate("MainWindow", u"Disconnect", None))
        self.pushButtonStart.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.pushButtonStop.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
        self.labelDirSave.setText(QCoreApplication.translate("MainWindow", u"Save in:", None))
        self.labelRT.setText(QCoreApplication.translate("MainWindow", u"Recording time:", None))
        self.labelFormat.setText(QCoreApplication.translate("MainWindow", u"Format:", None))
        self.labelRTvalue.setText(QCoreApplication.translate("MainWindow", u"[00:00:00]", None))
        self.comboBoxFormat.setItemText(0, QCoreApplication.translate("MainWindow", u"WFDB", None))
        self.comboBoxFormat.setItemText(1, QCoreApplication.translate("MainWindow", u"EDF", None))

        self.pushButtonSelectDirSave.setText(QCoreApplication.translate("MainWindow", u"Change", None))
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

