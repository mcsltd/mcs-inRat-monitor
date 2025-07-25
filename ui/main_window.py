# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_windowDdXqbP.ui'
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
        self.pushButtonFind = QPushButton(self.centralwidget)
        self.pushButtonFind.setObjectName(u"pushButtonFind")

        self.verticalLayout.addWidget(self.pushButtonFind)

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
        self.pushButtonFind.setText(QCoreApplication.translate("MainWindow", u"Find", None))
        self.pushButtonStart.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.pushButtonStop.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Format:", None))
        self.comboBoxFormat.setItemText(0, QCoreApplication.translate("MainWindow", u"WFDB", None))
        self.comboBoxFormat.setItemText(1, QCoreApplication.translate("MainWindow", u"EDF", None))

        self.pushButtonRecording.setText(QCoreApplication.translate("MainWindow", u"Start Recording", None))
    # retranslateUi
