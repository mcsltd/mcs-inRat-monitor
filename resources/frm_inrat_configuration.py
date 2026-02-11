# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'frm_inrat_configurationLFOgTD.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFrame,
    QGridLayout, QHeaderView, QLabel, QSizePolicy,
    QTableView, QVBoxLayout, QWidget)

class Ui_FrmInRatConfig(object):
    def setupUi(self, FrmInRatConfig):
        if not FrmInRatConfig.objectName():
            FrmInRatConfig.setObjectName(u"FrmInRatConfig")
        FrmInRatConfig.resize(549, 356)
        self.gridLayout_2 = QGridLayout(FrmInRatConfig)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.labelSamplingRateValueDim = QLabel(FrmInRatConfig)
        self.labelSamplingRateValueDim.setObjectName(u"labelSamplingRateValueDim")

        self.gridLayout.addWidget(self.labelSamplingRateValueDim, 0, 2, 1, 1)

        self.checkBoxEnabeActivated = QCheckBox(FrmInRatConfig)
        self.checkBoxEnabeActivated.setObjectName(u"checkBoxEnabeActivated")

        self.gridLayout.addWidget(self.checkBoxEnabeActivated, 2, 1, 1, 1)

        self.comboBoxSamplingRate = QComboBox(FrmInRatConfig)
        self.comboBoxSamplingRate.addItem("")
        self.comboBoxSamplingRate.addItem("")
        self.comboBoxSamplingRate.addItem("")
        self.comboBoxSamplingRate.setObjectName(u"comboBoxSamplingRate")

        self.gridLayout.addWidget(self.comboBoxSamplingRate, 0, 1, 1, 1)

        self.labelSamplingRate = QLabel(FrmInRatConfig)
        self.labelSamplingRate.setObjectName(u"labelSamplingRate")

        self.gridLayout.addWidget(self.labelSamplingRate, 0, 0, 1, 1)

        self.labelEnableActivated = QLabel(FrmInRatConfig)
        self.labelEnableActivated.setObjectName(u"labelEnableActivated")

        self.gridLayout.addWidget(self.labelEnableActivated, 2, 0, 1, 1)

        self.labelFullScaleAcc = QLabel(FrmInRatConfig)
        self.labelFullScaleAcc.setObjectName(u"labelFullScaleAcc")

        self.gridLayout.addWidget(self.labelFullScaleAcc, 1, 0, 1, 1)

        self.comboBoxScaleAcc = QComboBox(FrmInRatConfig)
        self.comboBoxScaleAcc.addItem("")
        self.comboBoxScaleAcc.addItem("")
        self.comboBoxScaleAcc.addItem("")
        self.comboBoxScaleAcc.addItem("")
        self.comboBoxScaleAcc.setObjectName(u"comboBoxScaleAcc")

        self.gridLayout.addWidget(self.comboBoxScaleAcc, 1, 1, 1, 1)

        self.labelAccDim = QLabel(FrmInRatConfig)
        self.labelAccDim.setObjectName(u"labelAccDim")

        self.gridLayout.addWidget(self.labelAccDim, 1, 2, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)


        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.labelEvents = QLabel(FrmInRatConfig)
        self.labelEvents.setObjectName(u"labelEvents")

        self.gridLayout_2.addWidget(self.labelEvents, 1, 0, 1, 1)

        self.tableViewEvents = QTableView(FrmInRatConfig)
        self.tableViewEvents.setObjectName(u"tableViewEvents")

        self.gridLayout_2.addWidget(self.tableViewEvents, 2, 0, 1, 1)


        self.retranslateUi(FrmInRatConfig)

        QMetaObject.connectSlotsByName(FrmInRatConfig)
    # setupUi

    def retranslateUi(self, FrmInRatConfig):
        FrmInRatConfig.setWindowTitle(QCoreApplication.translate("FrmInRatConfig", u"inRat", None))
        self.labelSamplingRateValueDim.setText(QCoreApplication.translate("FrmInRatConfig", u"[\u0413\u0446]", None))
        self.checkBoxEnabeActivated.setText("")
        self.comboBoxSamplingRate.setItemText(0, QCoreApplication.translate("FrmInRatConfig", u"500", None))
        self.comboBoxSamplingRate.setItemText(1, QCoreApplication.translate("FrmInRatConfig", u"1000", None))
        self.comboBoxSamplingRate.setItemText(2, QCoreApplication.translate("FrmInRatConfig", u"2000", None))

        self.labelSamplingRate.setText(QCoreApplication.translate("FrmInRatConfig", u"\u0427\u0430\u0441\u0442\u043e\u0442\u0430 \u043e\u0446\u0438\u0444\u0440\u043e\u0432\u043a\u0438", None))
        self.labelEnableActivated.setText(QCoreApplication.translate("FrmInRatConfig", u"\u0410\u043a\u0442\u0438\u0432\u0438\u0440\u043e\u0432\u0430\u043d\u043e", None))
        self.labelFullScaleAcc.setText(QCoreApplication.translate("FrmInRatConfig", u"\u0414\u0438\u0430\u043f\u0430\u0437\u043e\u043d \u0430\u043a\u0441\u0435\u043b\u0435\u0440\u043e\u043c\u0435\u0442\u0440\u0430", None))
        self.comboBoxScaleAcc.setItemText(0, QCoreApplication.translate("FrmInRatConfig", u"\u00b12", None))
        self.comboBoxScaleAcc.setItemText(1, QCoreApplication.translate("FrmInRatConfig", u"\u00b14", None))
        self.comboBoxScaleAcc.setItemText(2, QCoreApplication.translate("FrmInRatConfig", u"\u00b18", None))
        self.comboBoxScaleAcc.setItemText(3, QCoreApplication.translate("FrmInRatConfig", u"\u00b116", None))

        self.labelAccDim.setText(QCoreApplication.translate("FrmInRatConfig", u"g", None))
        self.labelEvents.setText(QCoreApplication.translate("FrmInRatConfig", u"\u0421\u043e\u0431\u044b\u0442\u0438\u044f", None))
    # retranslateUi

