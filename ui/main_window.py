# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_windowECowQS.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFormLayout,
    QFrame, QGridLayout, QHBoxLayout, QLabel,
    QLineEdit, QMainWindow, QMenuBar, QPushButton,
    QSizePolicy, QSpacerItem, QStatusBar, QVBoxLayout,
    QWidget)

from pyqtgraph import PlotWidget
import ui.resources

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1084, 890)
        icon = QIcon()
        icon.addFile(u":/iconMCS.ico", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        MainWindow.setWindowIcon(icon)
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

        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.labelActivated = QLabel(self.centralwidget)
        self.labelActivated.setObjectName(u"labelActivated")
        self.labelActivated.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelActivated.sizePolicy().hasHeightForWidth())
        self.labelActivated.setSizePolicy(sizePolicy)
        self.labelActivated.setMinimumSize(QSize(100, 0))
        self.labelActivated.setMaximumSize(QSize(100, 100))
        self.labelActivated.setFont(font)
        self.labelActivated.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.labelActivated)

        self.checkBoxActivated = QCheckBox(self.centralwidget)
        self.checkBoxActivated.setObjectName(u"checkBoxActivated")
        self.checkBoxActivated.setEnabled(False)
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.checkBoxActivated.sizePolicy().hasHeightForWidth())
        self.checkBoxActivated.setSizePolicy(sizePolicy1)
        self.checkBoxActivated.setFont(font)
        self.checkBoxActivated.setIconSize(QSize(32, 32))

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.checkBoxActivated)


        self.verticalLayout.addLayout(self.formLayout)

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
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.lineEditSave.sizePolicy().hasHeightForWidth())
        self.lineEditSave.setSizePolicy(sizePolicy2)
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
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.pushButtonSelectDirSave.sizePolicy().hasHeightForWidth())
        self.pushButtonSelectDirSave.setSizePolicy(sizePolicy3)
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

        self.line_2 = QFrame(self.centralwidget)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line_2)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.label)

        self.pushButtonViewRecording = QPushButton(self.centralwidget)
        self.pushButtonViewRecording.setObjectName(u"pushButtonViewRecording")
        self.pushButtonViewRecording.setFont(font)

        self.verticalLayout.addWidget(self.pushButtonViewRecording)

        self.line_5 = QFrame(self.centralwidget)
        self.line_5.setObjectName(u"line_5")
        self.line_5.setFrameShape(QFrame.Shape.HLine)
        self.line_5.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line_5)

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

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.gridLayout.addLayout(self.verticalLayout, 0, 1, 1, 1)

        self.verticalLayoutDisplay = QVBoxLayout()
        self.verticalLayoutDisplay.setObjectName(u"verticalLayoutDisplay")
        self.plotWidget = PlotWidget(self.centralwidget)
        self.plotWidget.setObjectName(u"plotWidget")
        self.plotWidget.setFont(font)

        self.verticalLayoutDisplay.addWidget(self.plotWidget)


        self.gridLayout.addLayout(self.verticalLayoutDisplay, 0, 0, 1, 1)

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
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"inRat monitor", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Device connection", None))
        self.labelDevice.setText(QCoreApplication.translate("MainWindow", u"Device:", None))
        self.pushButtonConnect.setText(QCoreApplication.translate("MainWindow", u"Connect", None))
        self.pushButtonDisconnect.setText(QCoreApplication.translate("MainWindow", u"Disconnect", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Device control", None))
        self.pushButtonStart.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.pushButtonStop.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
        self.labelActivated.setText(QCoreApplication.translate("MainWindow", u"Activated", None))
        self.checkBoxActivated.setText("")
        self.labelDataStorage.setText(QCoreApplication.translate("MainWindow", u"Data storage", None))
        self.labelRT.setText(QCoreApplication.translate("MainWindow", u"Recording time:", None))
        self.pushButtonSelectDirSave.setText(QCoreApplication.translate("MainWindow", u"Change", None))
        self.comboBoxFormat.setItemText(0, QCoreApplication.translate("MainWindow", u"WFDB", None))
        self.comboBoxFormat.setItemText(1, QCoreApplication.translate("MainWindow", u"EDF", None))

        self.labelDirSave.setText(QCoreApplication.translate("MainWindow", u"Save in:", None))
        self.labelRTvalue.setText(QCoreApplication.translate("MainWindow", u"00:00:00", None))
        self.labelFormat.setText(QCoreApplication.translate("MainWindow", u"Format:", None))
        self.pushButtonRecording.setText(QCoreApplication.translate("MainWindow", u"Start Recording", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Viewer", None))
        self.pushButtonViewRecording.setText(QCoreApplication.translate("MainWindow", u"View Recording", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Display", None))
        self.labelPage.setText(QCoreApplication.translate("MainWindow", u"/ Page", None))
        self.labelTimebase.setText(QCoreApplication.translate("MainWindow", u"Timebase", None))
    # retranslateUi

