# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window_v1NdKbXk.ui'
##
## Created by: Qt User Interface Compiler version 6.12.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
    QLabel, QMainWindow, QMenu, QMenuBar,
    QPushButton, QSizePolicy, QSpacerItem, QTabWidget,
    QVBoxLayout, QWidget)
import resources.resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(999, 575)
        font = QFont()
        font.setPointSize(11)
        MainWindow.setFont(font)
        icon = QIcon()
        icon.addFile(u":/images/icon.ico", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setTabShape(QTabWidget.TabShape.Rounded)
        self.actionExit = QAction(MainWindow)
        self.actionExit.setObjectName(u"actionExit")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(-1, 0, -1, -1)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(3)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayoutControlPane = QHBoxLayout()
        self.horizontalLayoutControlPane.setSpacing(2)
        self.horizontalLayoutControlPane.setObjectName(u"horizontalLayoutControlPane")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayoutControlPane.addItem(self.horizontalSpacer)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.pushButtonConfig = QPushButton(self.centralwidget)
        self.pushButtonConfig.setObjectName(u"pushButtonConfig")
        self.pushButtonConfig.setEnabled(False)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonConfig.sizePolicy().hasHeightForWidth())
        self.pushButtonConfig.setSizePolicy(sizePolicy)
        self.pushButtonConfig.setMinimumSize(QSize(75, 75))
        self.pushButtonConfig.setMaximumSize(QSize(75, 75))
        self.pushButtonConfig.setStyleSheet(u"QPushButton {\n"
"    background-color: transparent;\n"
"    border: none;\n"
"}")
        icon1 = QIcon()
        icon1.addFile(u":/images/settings.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButtonConfig.setIcon(icon1)
        self.pushButtonConfig.setIconSize(QSize(50, 50))

        self.verticalLayout_2.addWidget(self.pushButtonConfig)

        self.labelConfigDesc = QLabel(self.centralwidget)
        self.labelConfigDesc.setObjectName(u"labelConfigDesc")
        self.labelConfigDesc.setMaximumSize(QSize(16777215, 20))
        self.labelConfigDesc.setFont(font)
        self.labelConfigDesc.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_2.addWidget(self.labelConfigDesc)


        self.horizontalLayoutControlPane.addLayout(self.verticalLayout_2)


        self.verticalLayout.addLayout(self.horizontalLayoutControlPane)

        self.line_2 = QFrame(self.centralwidget)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line_2)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayoutDisplay = QVBoxLayout()
        self.verticalLayoutDisplay.setObjectName(u"verticalLayoutDisplay")
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayoutDisplay.addItem(self.verticalSpacer)


        self.horizontalLayout_2.addLayout(self.verticalLayoutDisplay)

        self.verticalLayoutCamera = QVBoxLayout()
        self.verticalLayoutCamera.setObjectName(u"verticalLayoutCamera")

        self.horizontalLayout_2.addLayout(self.verticalLayoutCamera)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.widgetStatusBar = QWidget(self.centralwidget)
        self.widgetStatusBar.setObjectName(u"widgetStatusBar")
        self.horizontalLayoutStatusBar = QHBoxLayout(self.widgetStatusBar)
        self.horizontalLayoutStatusBar.setObjectName(u"horizontalLayoutStatusBar")
        self.horizontalLayoutStatusBar.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayoutStatusBar.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addWidget(self.widgetStatusBar)


        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 999, 33))
        self.menu = QMenu(self.menubar)
        self.menu.setObjectName(u"menu")
        MainWindow.setMenuBar(self.menubar)

        self.menubar.addAction(self.menu.menuAction())
        self.menu.addAction(self.actionExit)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"inRat monitor", None))
        self.actionExit.setText(QCoreApplication.translate("MainWindow", u"\u0412\u044b\u0439\u0442\u0438", None))
        self.pushButtonConfig.setText("")
        self.labelConfigDesc.setText(QCoreApplication.translate("MainWindow", u"\u041d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0438", None))
        self.menu.setTitle(QCoreApplication.translate("MainWindow", u"\u0424\u0430\u0439\u043b", None))
    # retranslateUi

