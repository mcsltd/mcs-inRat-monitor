# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_windowqoxNpP.ui'
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
        MainWindow.resize(1084, 824)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        font = QFont()
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.label_4)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.labelDevice = QLabel(self.centralwidget)
        self.labelDevice.setObjectName(u"labelDevice")
        self.labelDevice.setFont(font)

        self.horizontalLayout_3.addWidget(self.labelDevice)

        self.comboBoxDevice = QComboBox(self.centralwidget)
        self.comboBoxDevice.setObjectName(u"comboBoxDevice")
        self.comboBoxDevice.setFont(font)

        self.horizontalLayout_3.addWidget(self.comboBoxDevice)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.pushButtonConnect = QPushButton(self.centralwidget)
        self.pushButtonConnect.setObjectName(u"pushButtonConnect")
        self.pushButtonConnect.setFont(font)

        self.verticalLayout.addWidget(self.pushButtonConnect)

        self.pushButtonDisconnect = QPushButton(self.centralwidget)
        self.pushButtonDisconnect.setObjectName(u"pushButtonDisconnect")
        self.pushButtonDisconnect.setFont(font)

        self.verticalLayout.addWidget(self.pushButtonDisconnect)

        self.line_3 = QFrame(self.centralwidget)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.Shape.HLine)
        self.line_3.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line_3)

        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font)
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.label_3)

        self.pushButtonStart = QPushButton(self.centralwidget)
        self.pushButtonStart.setObjectName(u"pushButtonStart")
        self.pushButtonStart.setEnabled(False)
        self.pushButtonStart.setFont(font)

        self.verticalLayout.addWidget(self.pushButtonStart)

        self.pushButtonStop = QPushButton(self.centralwidget)
        self.pushButtonStop.setObjectName(u"pushButtonStop")
        self.pushButtonStop.setEnabled(False)
        self.pushButtonStop.setFont(font)

        self.verticalLayout.addWidget(self.pushButtonStop)

        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.labelDataStorage = QLabel(self.centralwidget)
        self.labelDataStorage.setObjectName(u"labelDataStorage")
        self.labelDataStorage.setFont(font)
        self.labelDataStorage.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.labelDataStorage)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.gridLayout_7 = QGridLayout()
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.lineEditSave = QLineEdit(self.centralwidget)
        self.lineEditSave.setObjectName(u"lineEditSave")
        self.lineEditSave.setEnabled(False)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditSave.sizePolicy().hasHeightForWidth())
        self.lineEditSave.setSizePolicy(sizePolicy)
        self.lineEditSave.setFont(font)

        self.gridLayout_7.addWidget(self.lineEditSave, 1, 1, 1, 1)

        self.labelRT = QLabel(self.centralwidget)
        self.labelRT.setObjectName(u"labelRT")
        self.labelRT.setFont(font)
        self.labelRT.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_7.addWidget(self.labelRT, 3, 0, 1, 1)

        self.pushButtonSelectDirSave = QPushButton(self.centralwidget)
        self.pushButtonSelectDirSave.setObjectName(u"pushButtonSelectDirSave")
        self.pushButtonSelectDirSave.setEnabled(True)
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.pushButtonSelectDirSave.sizePolicy().hasHeightForWidth())
        self.pushButtonSelectDirSave.setSizePolicy(sizePolicy1)
        self.pushButtonSelectDirSave.setMinimumSize(QSize(5, 0))
        self.pushButtonSelectDirSave.setFont(font)

        self.gridLayout_7.addWidget(self.pushButtonSelectDirSave, 1, 2, 1, 1)

        self.comboBoxFormat = QComboBox(self.centralwidget)
        self.comboBoxFormat.addItem("")
        self.comboBoxFormat.addItem("")
        self.comboBoxFormat.setObjectName(u"comboBoxFormat")
        self.comboBoxFormat.setEnabled(False)
        self.comboBoxFormat.setFont(font)

        self.gridLayout_7.addWidget(self.comboBoxFormat, 2, 1, 1, 1)

        self.labelDirSave = QLabel(self.centralwidget)
        self.labelDirSave.setObjectName(u"labelDirSave")
        self.labelDirSave.setFont(font)
        self.labelDirSave.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_7.addWidget(self.labelDirSave, 1, 0, 1, 1)

        self.labelRTvalue = QLabel(self.centralwidget)
        self.labelRTvalue.setObjectName(u"labelRTvalue")
        self.labelRTvalue.setFont(font)
        self.labelRTvalue.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_7.addWidget(self.labelRTvalue, 3, 1, 1, 1)

        self.labelFormat = QLabel(self.centralwidget)
        self.labelFormat.setObjectName(u"labelFormat")
        self.labelFormat.setFont(font)
        self.labelFormat.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_7.addWidget(self.labelFormat, 2, 0, 1, 1)


        self.horizontalLayout_2.addLayout(self.gridLayout_7)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.pushButtonRecording = QPushButton(self.centralwidget)
        self.pushButtonRecording.setObjectName(u"pushButtonRecording")
        self.pushButtonRecording.setEnabled(False)
        self.pushButtonRecording.setFont(font)

        self.verticalLayout.addWidget(self.pushButtonRecording)

        self.pushButtonShowRecords = QPushButton(self.centralwidget)
        self.pushButtonShowRecords.setObjectName(u"pushButtonShowRecords")
        self.pushButtonShowRecords.setEnabled(True)
        self.pushButtonShowRecords.setFont(font)

        self.verticalLayout.addWidget(self.pushButtonShowRecords)

        self.line_2 = QFrame(self.centralwidget)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line_2)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font)
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.label_2)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.comboBoxTimebase = QComboBox(self.centralwidget)
        self.comboBoxTimebase.setObjectName(u"comboBoxTimebase")
        self.comboBoxTimebase.setFont(font)

        self.gridLayout_2.addWidget(self.comboBoxTimebase, 0, 1, 1, 1)

        self.labelPage = QLabel(self.centralwidget)
        self.labelPage.setObjectName(u"labelPage")
        self.labelPage.setFont(font)

        self.gridLayout_2.addWidget(self.labelPage, 0, 2, 1, 1)

        self.labelTimebase = QLabel(self.centralwidget)
        self.labelTimebase.setObjectName(u"labelTimebase")
        self.labelTimebase.setFont(font)

        self.gridLayout_2.addWidget(self.labelTimebase, 0, 0, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout_2)

        self.line_4 = QFrame(self.centralwidget)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.Shape.HLine)
        self.line_4.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line_4)

        self.labelDeviceInformation = QLabel(self.centralwidget)
        self.labelDeviceInformation.setObjectName(u"labelDeviceInformation")
        self.labelDeviceInformation.setFont(font)
        self.labelDeviceInformation.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.labelDeviceInformation)

        self.gridLayout_5 = QGridLayout()
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.labelSFValue = QLabel(self.centralwidget)
        self.labelSFValue.setObjectName(u"labelSFValue")
        self.labelSFValue.setFont(font)

        self.gridLayout_5.addWidget(self.labelSFValue, 4, 1, 1, 1)

        self.labelStatus = QLabel(self.centralwidget)
        self.labelStatus.setObjectName(u"labelStatus")
        self.labelStatus.setFont(font)

        self.gridLayout_5.addWidget(self.labelStatus, 3, 0, 1, 1)

        self.labelSerialNumberValue = QLabel(self.centralwidget)
        self.labelSerialNumberValue.setObjectName(u"labelSerialNumberValue")
        self.labelSerialNumberValue.setFont(font)

        self.gridLayout_5.addWidget(self.labelSerialNumberValue, 1, 1, 1, 1)

        self.labelFirmware = QLabel(self.centralwidget)
        self.labelFirmware.setObjectName(u"labelFirmware")
        self.labelFirmware.setFont(font)

        self.gridLayout_5.addWidget(self.labelFirmware, 5, 0, 1, 1)

        self.labelModelValue = QLabel(self.centralwidget)
        self.labelModelValue.setObjectName(u"labelModelValue")
        self.labelModelValue.setFont(font)

        self.gridLayout_5.addWidget(self.labelModelValue, 2, 1, 1, 1)

        self.labelName = QLabel(self.centralwidget)
        self.labelName.setObjectName(u"labelName")
        self.labelName.setFont(font)

        self.gridLayout_5.addWidget(self.labelName, 0, 0, 1, 1)

        self.labelNameValue = QLabel(self.centralwidget)
        self.labelNameValue.setObjectName(u"labelNameValue")
        self.labelNameValue.setFont(font)

        self.gridLayout_5.addWidget(self.labelNameValue, 0, 1, 1, 1)

        self.labelSF = QLabel(self.centralwidget)
        self.labelSF.setObjectName(u"labelSF")
        self.labelSF.setFont(font)

        self.gridLayout_5.addWidget(self.labelSF, 4, 0, 1, 1)

        self.labelModel = QLabel(self.centralwidget)
        self.labelModel.setObjectName(u"labelModel")
        self.labelModel.setFont(font)

        self.gridLayout_5.addWidget(self.labelModel, 2, 0, 1, 1)

        self.labelStatusValue = QLabel(self.centralwidget)
        self.labelStatusValue.setObjectName(u"labelStatusValue")
        self.labelStatusValue.setFont(font)

        self.gridLayout_5.addWidget(self.labelStatusValue, 3, 1, 1, 1)

        self.labelSerialNumber = QLabel(self.centralwidget)
        self.labelSerialNumber.setObjectName(u"labelSerialNumber")
        self.labelSerialNumber.setFont(font)

        self.gridLayout_5.addWidget(self.labelSerialNumber, 1, 0, 1, 1)

        self.labelHardware = QLabel(self.centralwidget)
        self.labelHardware.setObjectName(u"labelHardware")
        self.labelHardware.setFont(font)

        self.gridLayout_5.addWidget(self.labelHardware, 6, 0, 1, 1)

        self.labelFirmwareValue = QLabel(self.centralwidget)
        self.labelFirmwareValue.setObjectName(u"labelFirmwareValue")
        self.labelFirmwareValue.setFont(font)

        self.gridLayout_5.addWidget(self.labelFirmwareValue, 5, 1, 1, 1)

        self.labelHardwareValue = QLabel(self.centralwidget)
        self.labelHardwareValue.setObjectName(u"labelHardwareValue")
        self.labelHardwareValue.setFont(font)

        self.gridLayout_5.addWidget(self.labelHardwareValue, 6, 1, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout_5)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.gridLayout.addLayout(self.verticalLayout, 0, 1, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.plotWidget = PlotWidget(self.centralwidget)
        self.plotWidget.setObjectName(u"plotWidget")
        self.plotWidget.setFont(font)

        self.horizontalLayout.addWidget(self.plotWidget)


        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1084, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Device connection", None))
        self.labelDevice.setText(QCoreApplication.translate("MainWindow", u"Device:", None))
        self.pushButtonConnect.setText(QCoreApplication.translate("MainWindow", u"Connect", None))
        self.pushButtonDisconnect.setText(QCoreApplication.translate("MainWindow", u"Disconnect", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Device control", None))
        self.pushButtonStart.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.pushButtonStop.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
        self.labelDataStorage.setText(QCoreApplication.translate("MainWindow", u"Data storage", None))
        self.labelRT.setText(QCoreApplication.translate("MainWindow", u"Recording time:", None))
        self.pushButtonSelectDirSave.setText(QCoreApplication.translate("MainWindow", u"Change", None))
        self.comboBoxFormat.setItemText(0, QCoreApplication.translate("MainWindow", u"WFDB", None))
        self.comboBoxFormat.setItemText(1, QCoreApplication.translate("MainWindow", u"EDF", None))

        self.labelDirSave.setText(QCoreApplication.translate("MainWindow", u"Save in:", None))
        self.labelRTvalue.setText(QCoreApplication.translate("MainWindow", u"00:00:00", None))
        self.labelFormat.setText(QCoreApplication.translate("MainWindow", u"Format:", None))
        self.pushButtonRecording.setText(QCoreApplication.translate("MainWindow", u"Start Recording", None))
        self.pushButtonShowRecords.setText(QCoreApplication.translate("MainWindow", u"Show Records", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Display", None))
        self.labelPage.setText(QCoreApplication.translate("MainWindow", u"/ Page", None))
        self.labelTimebase.setText(QCoreApplication.translate("MainWindow", u"Timebase", None))
        self.labelDeviceInformation.setText(QCoreApplication.translate("MainWindow", u"Device information", None))
        self.labelSFValue.setText(QCoreApplication.translate("MainWindow", u"None", None))
        self.labelStatus.setText(QCoreApplication.translate("MainWindow", u"Status:", None))
        self.labelSerialNumberValue.setText(QCoreApplication.translate("MainWindow", u"None", None))
        self.labelFirmware.setText(QCoreApplication.translate("MainWindow", u"Firmware:", None))
        self.labelModelValue.setText(QCoreApplication.translate("MainWindow", u"None", None))
        self.labelName.setText(QCoreApplication.translate("MainWindow", u"Name:", None))
        self.labelNameValue.setText(QCoreApplication.translate("MainWindow", u"None", None))
        self.labelSF.setText(QCoreApplication.translate("MainWindow", u"Sample Frequency:", None))
        self.labelModel.setText(QCoreApplication.translate("MainWindow", u"Model:", None))
        self.labelStatusValue.setText(QCoreApplication.translate("MainWindow", u"Not connected", None))
        self.labelSerialNumber.setText(QCoreApplication.translate("MainWindow", u"Serial:", None))
        self.labelHardware.setText(QCoreApplication.translate("MainWindow", u"Hardware:", None))
        self.labelFirmwareValue.setText(QCoreApplication.translate("MainWindow", u"None", None))
        self.labelHardwareValue.setText(QCoreApplication.translate("MainWindow", u"None", None))
    # retranslateUi

