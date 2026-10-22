# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dlg_infooiyEzF.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QFormLayout, QGridLayout,
    QLabel, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)
import resources.resources_rc

class Ui_DlgDeviceInfo(object):
    def setupUi(self, DlgDeviceInfo):
        if not DlgDeviceInfo.objectName():
            DlgDeviceInfo.setObjectName(u"DlgDeviceInfo")
        DlgDeviceInfo.resize(447, 328)
        DlgDeviceInfo.setMaximumSize(QSize(600, 400))
        icon = QIcon()
        icon.addFile(u":/images/icon.ico", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        DlgDeviceInfo.setWindowIcon(icon)
        self.gridLayout = QGridLayout(DlgDeviceInfo)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayoutDeviceInfo = QVBoxLayout()
        self.verticalLayoutDeviceInfo.setObjectName(u"verticalLayoutDeviceInfo")
        self.labelDevice = QLabel(DlgDeviceInfo)
        self.labelDevice.setObjectName(u"labelDevice")
        font = QFont()
        font.setBold(True)
        self.labelDevice.setFont(font)
        self.labelDevice.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.verticalLayoutDeviceInfo.addWidget(self.labelDevice)

        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.labelName = QLabel(DlgDeviceInfo)
        self.labelName.setObjectName(u"labelName")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelName.sizePolicy().hasHeightForWidth())
        self.labelName.setSizePolicy(sizePolicy)
        self.labelName.setMinimumSize(QSize(150, 0))

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.labelName)

        self.labelNameValue = QLabel(DlgDeviceInfo)
        self.labelNameValue.setObjectName(u"labelNameValue")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.labelNameValue)

        self.labelModel = QLabel(DlgDeviceInfo)
        self.labelModel.setObjectName(u"labelModel")
        sizePolicy.setHeightForWidth(self.labelModel.sizePolicy().hasHeightForWidth())
        self.labelModel.setSizePolicy(sizePolicy)
        self.labelModel.setMinimumSize(QSize(150, 0))

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.labelModel)

        self.labelSn = QLabel(DlgDeviceInfo)
        self.labelSn.setObjectName(u"labelSn")
        sizePolicy.setHeightForWidth(self.labelSn.sizePolicy().hasHeightForWidth())
        self.labelSn.setSizePolicy(sizePolicy)
        self.labelSn.setMinimumSize(QSize(150, 0))

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.labelSn)

        self.labelSnValue = QLabel(DlgDeviceInfo)
        self.labelSnValue.setObjectName(u"labelSnValue")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.labelSnValue)

        self.labelModelValue = QLabel(DlgDeviceInfo)
        self.labelModelValue.setObjectName(u"labelModelValue")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.labelModelValue)

        self.labelFirm = QLabel(DlgDeviceInfo)
        self.labelFirm.setObjectName(u"labelFirm")
        sizePolicy.setHeightForWidth(self.labelFirm.sizePolicy().hasHeightForWidth())
        self.labelFirm.setSizePolicy(sizePolicy)
        self.labelFirm.setMinimumSize(QSize(150, 0))

        self.formLayout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.labelFirm)

        self.labelFirmValue = QLabel(DlgDeviceInfo)
        self.labelFirmValue.setObjectName(u"labelFirmValue")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.FieldRole, self.labelFirmValue)

        self.labelHard = QLabel(DlgDeviceInfo)
        self.labelHard.setObjectName(u"labelHard")
        sizePolicy.setHeightForWidth(self.labelHard.sizePolicy().hasHeightForWidth())
        self.labelHard.setSizePolicy(sizePolicy)
        self.labelHard.setMinimumSize(QSize(150, 0))

        self.formLayout.setWidget(4, QFormLayout.ItemRole.LabelRole, self.labelHard)

        self.labelHardValue = QLabel(DlgDeviceInfo)
        self.labelHardValue.setObjectName(u"labelHardValue")

        self.formLayout.setWidget(4, QFormLayout.ItemRole.FieldRole, self.labelHardValue)


        self.verticalLayoutDeviceInfo.addLayout(self.formLayout)

        self.labelWorkingTime = QLabel(DlgDeviceInfo)
        self.labelWorkingTime.setObjectName(u"labelWorkingTime")
        self.labelWorkingTime.setFont(font)

        self.verticalLayoutDeviceInfo.addWidget(self.labelWorkingTime)

        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.labelAdv = QLabel(DlgDeviceInfo)
        self.labelAdv.setObjectName(u"labelAdv")
        sizePolicy.setHeightForWidth(self.labelAdv.sizePolicy().hasHeightForWidth())
        self.labelAdv.setSizePolicy(sizePolicy)
        self.labelAdv.setMinimumSize(QSize(150, 0))

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.LabelRole, self.labelAdv)

        self.labelAdvValue = QLabel(DlgDeviceInfo)
        self.labelAdvValue.setObjectName(u"labelAdvValue")

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.FieldRole, self.labelAdvValue)

        self.labelConn = QLabel(DlgDeviceInfo)
        self.labelConn.setObjectName(u"labelConn")
        sizePolicy.setHeightForWidth(self.labelConn.sizePolicy().hasHeightForWidth())
        self.labelConn.setSizePolicy(sizePolicy)
        self.labelConn.setMinimumSize(QSize(150, 0))

        self.formLayout_2.setWidget(1, QFormLayout.ItemRole.LabelRole, self.labelConn)

        self.labelConnValue = QLabel(DlgDeviceInfo)
        self.labelConnValue.setObjectName(u"labelConnValue")

        self.formLayout_2.setWidget(1, QFormLayout.ItemRole.FieldRole, self.labelConnValue)

        self.labelData = QLabel(DlgDeviceInfo)
        self.labelData.setObjectName(u"labelData")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.labelData.sizePolicy().hasHeightForWidth())
        self.labelData.setSizePolicy(sizePolicy1)
        self.labelData.setMinimumSize(QSize(150, 0))
        self.labelData.setMaximumSize(QSize(100, 16777215))

        self.formLayout_2.setWidget(2, QFormLayout.ItemRole.LabelRole, self.labelData)

        self.labelDataValue = QLabel(DlgDeviceInfo)
        self.labelDataValue.setObjectName(u"labelDataValue")

        self.formLayout_2.setWidget(2, QFormLayout.ItemRole.FieldRole, self.labelDataValue)

        self.labelPowerOnCnt = QLabel(DlgDeviceInfo)
        self.labelPowerOnCnt.setObjectName(u"labelPowerOnCnt")
        self.labelPowerOnCnt.setMinimumSize(QSize(150, 0))

        self.formLayout_2.setWidget(3, QFormLayout.ItemRole.LabelRole, self.labelPowerOnCnt)

        self.labelPowerOnCntValue = QLabel(DlgDeviceInfo)
        self.labelPowerOnCntValue.setObjectName(u"labelPowerOnCntValue")

        self.formLayout_2.setWidget(3, QFormLayout.ItemRole.FieldRole, self.labelPowerOnCntValue)


        self.verticalLayoutDeviceInfo.addLayout(self.formLayout_2)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayoutDeviceInfo.addItem(self.verticalSpacer)


        self.gridLayout.addLayout(self.verticalLayoutDeviceInfo, 0, 0, 1, 1)


        self.retranslateUi(DlgDeviceInfo)

        QMetaObject.connectSlotsByName(DlgDeviceInfo)
    # setupUi

    def retranslateUi(self, DlgDeviceInfo):
        DlgDeviceInfo.setWindowTitle(QCoreApplication.translate("DlgDeviceInfo", u"\u0418\u043d\u0444\u043e\u0440\u043c\u0430\u0446\u0438\u044f \u043e\u0431 \u0443\u0441\u0442\u0440\u043e\u0439\u0441\u0442\u0432\u0435", None))
        self.labelDevice.setText(QCoreApplication.translate("DlgDeviceInfo", u"\u0423\u0441\u0442\u0440\u043e\u0439\u0441\u0442\u0432\u043e:", None))
        self.labelName.setText(QCoreApplication.translate("DlgDeviceInfo", u"\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435", None))
        self.labelNameValue.setText(QCoreApplication.translate("DlgDeviceInfo", u"undefine", None))
        self.labelModel.setText(QCoreApplication.translate("DlgDeviceInfo", u"\u041c\u043e\u0434\u0435\u043b\u044c", None))
        self.labelSn.setText(QCoreApplication.translate("DlgDeviceInfo", u"SN", None))
        self.labelSnValue.setText(QCoreApplication.translate("DlgDeviceInfo", u"undefine", None))
        self.labelModelValue.setText(QCoreApplication.translate("DlgDeviceInfo", u"undefine", None))
        self.labelFirm.setText(QCoreApplication.translate("DlgDeviceInfo", u"Frimware", None))
        self.labelFirmValue.setText(QCoreApplication.translate("DlgDeviceInfo", u"undefine", None))
        self.labelHard.setText(QCoreApplication.translate("DlgDeviceInfo", u"Hardware", None))
        self.labelHardValue.setText(QCoreApplication.translate("DlgDeviceInfo", u"undefine", None))
        self.labelWorkingTime.setText(QCoreApplication.translate("DlgDeviceInfo", u"\u0412\u0440\u0435\u043c\u044f \u0440\u0430\u0431\u043e\u0442\u044b:", None))
        self.labelAdv.setText(QCoreApplication.translate("DlgDeviceInfo", u"\u0420\u0435\u043a\u043b\u0430\u043c\u0430", None))
        self.labelAdvValue.setText(QCoreApplication.translate("DlgDeviceInfo", u"undefine", None))
        self.labelConn.setText(QCoreApplication.translate("DlgDeviceInfo", u"\u0421\u043e\u0435\u0434\u0438\u043d\u0435\u043d\u0438\u0435", None))
        self.labelConnValue.setText(QCoreApplication.translate("DlgDeviceInfo", u"undefine", None))
        self.labelData.setText(QCoreApplication.translate("DlgDeviceInfo", u"\u041f\u0435\u0440\u0435\u0434\u0430\u0447\u0430 \u0434\u0430\u043d\u043d\u044b\u0445", None))
        self.labelDataValue.setText(QCoreApplication.translate("DlgDeviceInfo", u"undefine", None))
        self.labelPowerOnCnt.setText(QCoreApplication.translate("DlgDeviceInfo", u"\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u0432\u043a\u043b\u044e\u0447\u0435\u043d\u0438\u0439", None))
        self.labelPowerOnCntValue.setText(QCoreApplication.translate("DlgDeviceInfo", u"undefine", None))
    # retranslateUi

