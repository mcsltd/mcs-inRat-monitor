# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dlg_inrat_configYcCbLW.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDialog,
    QFormLayout, QGridLayout, QGroupBox, QHBoxLayout,
    QLabel, QPushButton, QSizePolicy, QSpacerItem,
    QWidget)
import resources.resources_rc

class Ui_DlgDeviceConfig(object):
    def setupUi(self, DlgDeviceConfig):
        if not DlgDeviceConfig.objectName():
            DlgDeviceConfig.setObjectName(u"DlgDeviceConfig")
        DlgDeviceConfig.resize(676, 424)
        icon = QIcon()
        icon.addFile(u":/images/icon.ico", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        DlgDeviceConfig.setWindowIcon(icon)
        self.gridLayout = QGridLayout(DlgDeviceConfig)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.pushButtonOk = QPushButton(DlgDeviceConfig)
        self.pushButtonOk.setObjectName(u"pushButtonOk")

        self.horizontalLayout.addWidget(self.pushButtonOk)

        self.pushButtonCancel = QPushButton(DlgDeviceConfig)
        self.pushButtonCancel.setObjectName(u"pushButtonCancel")

        self.horizontalLayout.addWidget(self.pushButtonCancel)


        self.gridLayout.addLayout(self.horizontalLayout, 5, 0, 1, 1)

        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.comboBoxMode = QComboBox(DlgDeviceConfig)
        self.comboBoxMode.setObjectName(u"comboBoxMode")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBoxMode.sizePolicy().hasHeightForWidth())
        self.comboBoxMode.setSizePolicy(sizePolicy)
        self.comboBoxMode.setMinimumSize(QSize(150, 0))
        self.comboBoxMode.setMaximumSize(QSize(150, 16777215))

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.comboBoxMode)

        self.labelSampleRate = QLabel(DlgDeviceConfig)
        self.labelSampleRate.setObjectName(u"labelSampleRate")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.labelSampleRate)

        self.comboBoxSampleRate = QComboBox(DlgDeviceConfig)
        self.comboBoxSampleRate.setObjectName(u"comboBoxSampleRate")
        sizePolicy.setHeightForWidth(self.comboBoxSampleRate.sizePolicy().hasHeightForWidth())
        self.comboBoxSampleRate.setSizePolicy(sizePolicy)
        self.comboBoxSampleRate.setMinimumSize(QSize(150, 0))
        self.comboBoxSampleRate.setMaximumSize(QSize(150, 16777215))

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.comboBoxSampleRate)

        self.labelFullScaleAccelerometer = QLabel(DlgDeviceConfig)
        self.labelFullScaleAccelerometer.setObjectName(u"labelFullScaleAccelerometer")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.labelFullScaleAccelerometer)

        self.comboBoxFullScaleAccelerometer = QComboBox(DlgDeviceConfig)
        self.comboBoxFullScaleAccelerometer.setObjectName(u"comboBoxFullScaleAccelerometer")
        sizePolicy.setHeightForWidth(self.comboBoxFullScaleAccelerometer.sizePolicy().hasHeightForWidth())
        self.comboBoxFullScaleAccelerometer.setSizePolicy(sizePolicy)
        self.comboBoxFullScaleAccelerometer.setMinimumSize(QSize(150, 0))

        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.comboBoxFullScaleAccelerometer)

        self.labelActivityThreshold = QLabel(DlgDeviceConfig)
        self.labelActivityThreshold.setObjectName(u"labelActivityThreshold")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.labelActivityThreshold)

        self.comboBoxActivityThreshold = QComboBox(DlgDeviceConfig)
        self.comboBoxActivityThreshold.setObjectName(u"comboBoxActivityThreshold")
        sizePolicy.setHeightForWidth(self.comboBoxActivityThreshold.sizePolicy().hasHeightForWidth())
        self.comboBoxActivityThreshold.setSizePolicy(sizePolicy)
        self.comboBoxActivityThreshold.setMinimumSize(QSize(150, 0))

        self.formLayout.setWidget(3, QFormLayout.ItemRole.FieldRole, self.comboBoxActivityThreshold)

        self.labelMode = QLabel(DlgDeviceConfig)
        self.labelMode.setObjectName(u"labelMode")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.labelMode)


        self.gridLayout.addLayout(self.formLayout, 0, 0, 1, 1)

        self.groupBoxEnabledEvents = QGroupBox(DlgDeviceConfig)
        self.groupBoxEnabledEvents.setObjectName(u"groupBoxEnabledEvents")
        self.groupBoxEnabledEvents.setFlat(False)
        self.groupBoxEnabledEvents.setCheckable(False)
        self.gridLayout_2 = QGridLayout(self.groupBoxEnabledEvents)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayoutEvents = QGridLayout()
        self.gridLayoutEvents.setObjectName(u"gridLayoutEvents")
        self.checkBoxOrientation = QCheckBox(self.groupBoxEnabledEvents)
        self.checkBoxOrientation.setObjectName(u"checkBoxOrientation")

        self.gridLayoutEvents.addWidget(self.checkBoxOrientation, 4, 0, 1, 1)

        self.checkBoxFreefall = QCheckBox(self.groupBoxEnabledEvents)
        self.checkBoxFreefall.setObjectName(u"checkBoxFreefall")

        self.gridLayoutEvents.addWidget(self.checkBoxFreefall, 3, 0, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayoutEvents.addItem(self.horizontalSpacer_2, 0, 2, 1, 1)

        self.checkBoxActivity = QCheckBox(self.groupBoxEnabledEvents)
        self.checkBoxActivity.setObjectName(u"checkBoxActivity")

        self.gridLayoutEvents.addWidget(self.checkBoxActivity, 0, 0, 1, 1)

        self.labelInfoOrientation = QLabel(self.groupBoxEnabledEvents)
        self.labelInfoOrientation.setObjectName(u"labelInfoOrientation")

        self.gridLayoutEvents.addWidget(self.labelInfoOrientation, 4, 1, 1, 1)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayoutEvents.addItem(self.horizontalSpacer_5, 5, 2, 1, 1)

        self.checkBoxTemp = QCheckBox(self.groupBoxEnabledEvents)
        self.checkBoxTemp.setObjectName(u"checkBoxTemp")

        self.gridLayoutEvents.addWidget(self.checkBoxTemp, 5, 0, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayoutEvents.addItem(self.horizontalSpacer_4, 4, 2, 1, 1)

        self.labelInfoFreefall = QLabel(self.groupBoxEnabledEvents)
        self.labelInfoFreefall.setObjectName(u"labelInfoFreefall")

        self.gridLayoutEvents.addWidget(self.labelInfoFreefall, 3, 1, 1, 1)

        self.labelInfoTemperature = QLabel(self.groupBoxEnabledEvents)
        self.labelInfoTemperature.setObjectName(u"labelInfoTemperature")

        self.gridLayoutEvents.addWidget(self.labelInfoTemperature, 5, 1, 1, 1)

        self.labelInfoActivity = QLabel(self.groupBoxEnabledEvents)
        self.labelInfoActivity.setObjectName(u"labelInfoActivity")

        self.gridLayoutEvents.addWidget(self.labelInfoActivity, 0, 1, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayoutEvents.addItem(self.horizontalSpacer_3, 3, 2, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayoutEvents, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.groupBoxEnabledEvents, 2, 0, 1, 1)

        self.groupBox = QGroupBox(DlgDeviceConfig)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout_4 = QGridLayout(self.groupBox)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.checkBoxSignal = QCheckBox(self.groupBox)
        self.checkBoxSignal.setObjectName(u"checkBoxSignal")

        self.gridLayout_3.addWidget(self.checkBoxSignal, 0, 0, 1, 1)

        self.checkBox_2 = QCheckBox(self.groupBox)
        self.checkBox_2.setObjectName(u"checkBox_2")

        self.gridLayout_3.addWidget(self.checkBox_2, 1, 0, 1, 1)


        self.gridLayout_4.addLayout(self.gridLayout_3, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.groupBox, 1, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 3, 0, 1, 1)


        self.retranslateUi(DlgDeviceConfig)

        QMetaObject.connectSlotsByName(DlgDeviceConfig)
    # setupUi

    def retranslateUi(self, DlgDeviceConfig):
        DlgDeviceConfig.setWindowTitle(QCoreApplication.translate("DlgDeviceConfig", u"\u041d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0430 inRat", None))
        self.pushButtonOk.setText(QCoreApplication.translate("DlgDeviceConfig", u"\u041e\u043a", None))
        self.pushButtonCancel.setText(QCoreApplication.translate("DlgDeviceConfig", u"\u041e\u0442\u043c\u0435\u043d\u0430", None))
        self.labelSampleRate.setText(QCoreApplication.translate("DlgDeviceConfig", u"\u0427\u0430\u0441\u0442\u043e\u0442\u0430 \u043e\u0446\u0438\u0444\u0440\u043e\u0432\u043a\u0438, \u0413\u0446", None))
        self.labelFullScaleAccelerometer.setText(QCoreApplication.translate("DlgDeviceConfig", u"\u0410\u043a\u0441\u0435\u043b\u0435\u0440\u043e\u043c\u0435\u0442\u0440, \u00b1g", None))
        self.labelActivityThreshold.setText(QCoreApplication.translate("DlgDeviceConfig", u"\u041f\u043e\u0440\u043e\u0433 \u0440\u0435\u0433\u0438\u0441\u0442\u0440\u0430\u0446\u0438\u0438 \u0430\u043a\u0442\u0438\u0432\u043d\u043e\u0441\u0442\u0438", None))
        self.labelMode.setText(QCoreApplication.translate("DlgDeviceConfig", u"\u0420\u0435\u0436\u0438\u043c \u0441\u044a\u0435\u043c\u0430", None))
        self.groupBoxEnabledEvents.setTitle(QCoreApplication.translate("DlgDeviceConfig", u"\u0421\u043e\u0431\u044b\u0442\u0438\u044f", None))
        self.checkBoxOrientation.setText(QCoreApplication.translate("DlgDeviceConfig", u"\u041e\u0440\u0438\u0435\u043d\u0442\u0430\u0446\u0438\u0438 (O)", None))
        self.checkBoxFreefall.setText(QCoreApplication.translate("DlgDeviceConfig", u"\u041f\u0440\u044b\u0436\u043e\u043a (F)", None))
        self.checkBoxActivity.setText(QCoreApplication.translate("DlgDeviceConfig", u"\u0410\u043a\u0442\u0438\u0432\u043d\u043e\u0441\u0442\u044c (A)", None))
#if QT_CONFIG(tooltip)
        self.labelInfoOrientation.setToolTip(QCoreApplication.translate("DlgDeviceConfig", u"<html><head/><body><p>\u0421\u043e\u0431\u044b\u0442\u0438\u0435 &quot;\u0421\u043c\u0435\u043d\u0430 \u043e\u0440\u0438\u0435\u043d\u0442\u0430\u0446\u0438\u0438&quot;</p><p>\u0424\u043e\u0440\u043c\u0430\u0442 \u0437\u0430\u043f\u0438\u0441\u0438: O {code}</p><p>\u041a\u043e\u0434\u044b \u043e\u0440\u0438\u0435\u043d\u0442\u0430\u0446\u0438\u0438:</p><p><span style=\" font-family:'Courier New';\">- x+</span> \u2014 \u0434\u0430\u0442\u0447\u0438\u043a \u043d\u0430 \u043b\u0435\u0432\u043e\u043c \u0431\u043e\u043a\u0443</p><p><span style=\" font-family:'Courier New';\">- x-</span> \u2014 \u0434\u0430\u0442\u0447\u0438\u043a \u043d\u0430 \u043f\u0440\u0430\u0432\u043e\u043c \u0431\u043e\u043a\u0443</p><p><span style=\" font-family:'Courier New';\">- y+</span> \u2014 \u0434\u0430\u0442\u0447\u0438\u043a \u0432\u0435\u0440\u0442\u0438\u043a\u0430\u043b\u044c\u043d\u043e</p><p><span style=\" font-family:'Courier New';\">- y-</span> \u2014 \u0434\u0430\u0442\u0447\u0438\u043a \u043f\u0435\u0440\u0435\u0432\u0451\u0440"
                        "\u043d\u0443\u0442</p><p><span style=\" font-family:'Courier New';\">- z+</span> \u2014 \u0434\u0430\u0442\u0447\u0438\u043a \u043b\u0438\u0446\u043e\u043c \u0432\u0432\u0435\u0440\u0445</p><p><span style=\" font-family:'Courier New';\">- z-</span> \u2014 \u0434\u0430\u0442\u0447\u0438\u043a \u043b\u0438\u0446\u043e\u043c \u0432\u043d\u0438\u0437</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.labelInfoOrientation.setText(QCoreApplication.translate("DlgDeviceConfig", u"?", None))
#if QT_CONFIG(tooltip)
        self.checkBoxTemp.setToolTip(QCoreApplication.translate("DlgDeviceConfig", u"\u0420\u0435\u0433\u0438\u0441\u0442\u0440\u0430\u0446\u0438\u044f \u0441\u043e\u0431\u044b\u0442\u0438\u044f \u0442\u0435\u043c\u043f\u0435\u0440\u0430\u0442\u0443\u0440\u044b\n"
"", None))
#endif // QT_CONFIG(tooltip)
        self.checkBoxTemp.setText(QCoreApplication.translate("DlgDeviceConfig", u"\u0422\u0435\u043c\u043f\u0435\u0440\u0430\u0442\u0443\u0440\u0430 (T)", None))
#if QT_CONFIG(tooltip)
        self.labelInfoFreefall.setToolTip(QCoreApplication.translate("DlgDeviceConfig", u"<html><head/><body><p>\u0421\u043e\u0431\u044b\u0442\u0438\u0435 &quot;\u041f\u0440\u044b\u0436\u043e\u043a&quot;</p><p>\u0423\u0441\u043b\u043e\u0432\u0438\u0435 \u0441\u0440\u0430\u0431\u0430\u0442\u044b\u0432\u0430\u043d\u0438\u044f: \u0443\u0441\u043a\u043e\u0440\u0435\u043d\u0438\u0435 \u043f\u043e \u043e\u0441\u044f\u043c X, Y, Z \u0431\u043b\u0438\u0437\u043a\u043e \u043a 0.</p><p>\u0424\u043e\u0440\u043c\u0430\u0442 \u0437\u0430\u043f\u0438\u0441\u0438: &quot;F&quot;</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.labelInfoFreefall.setText(QCoreApplication.translate("DlgDeviceConfig", u"?", None))
#if QT_CONFIG(tooltip)
        self.labelInfoTemperature.setToolTip(QCoreApplication.translate("DlgDeviceConfig", u"<html><head/><body><p>\u0421\u043e\u0431\u044b\u0442\u0438\u0435 &quot;\u0422\u0435\u043c\u043f\u0435\u0440\u0430\u0442\u0443\u0440\u0430&quot;</p><p>\u0415\u0434\u0438\u043d\u0438\u0446\u044b \u0438\u0437\u043c\u0435\u0440\u0435\u043d\u0438\u044f: \u0433\u0440\u0430\u0434\u0443\u0441\u044b \u0426\u0435\u043b\u044c\u0441\u0438\u044f (\u00b0C)<br/>\u0424\u043e\u0440\u043c\u0430\u0442 \u0437\u0430\u043f\u0438\u0441\u0438: T {\u0437\u043d\u0430\u0447\u0435\u043d\u0438\u0435}</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.labelInfoTemperature.setText(QCoreApplication.translate("DlgDeviceConfig", u"?", None))
#if QT_CONFIG(tooltip)
        self.labelInfoActivity.setToolTip(QCoreApplication.translate("DlgDeviceConfig", u"<html><head/><body><p>\u0421\u043e\u0431\u044b\u0442\u0438\u0435 &quot;\u0410\u043a\u0442\u0438\u0432\u043d\u043e\u0441\u0442\u044c&quot;</p><p>\u0423\u0441\u043b\u043e\u0432\u0438\u0435 \u0441\u0440\u0430\u0431\u0430\u0442\u044b\u0432\u0430\u043d\u0438\u044f: \u043f\u0440\u0435\u0432\u044b\u0448\u0435\u043d\u0438\u0435 \u043f\u043e\u0440\u043e\u0433\u0430 \u0443\u0441\u043a\u043e\u0440\u0435\u043d\u0438\u044f \u043f\u043e \u043e\u0434\u043d\u043e\u0439 \u0438\u0437 \u043e\u0441\u0435\u0439.<br/>\u0424\u043e\u0440\u043c\u0430\u0442 \u0437\u0430\u043f\u0438\u0441\u0438: A {x} {y} {z}</p><p> - \u0443\u0441\u043a\u043e\u0440\u0435\u043d\u0438\u0435 \u0432 \u043c\u0438\u043b\u043b\u0438-g (mg) \u043f\u043e \u043e\u0441\u044f\u043c X, Y, Z.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.labelInfoActivity.setText(QCoreApplication.translate("DlgDeviceConfig", u"?", None))
        self.groupBox.setTitle(QCoreApplication.translate("DlgDeviceConfig", u"\u041a\u0430\u043d\u0430\u043b\u044b", None))
        self.checkBoxSignal.setText(QCoreApplication.translate("DlgDeviceConfig", u"\u042d\u041a\u0413", None))
        self.checkBox_2.setText(QCoreApplication.translate("DlgDeviceConfig", u"\u0410\u043a\u0441\u0435\u043b\u0435\u0440\u043e\u043c\u0435\u0442\u0440", None))
    # retranslateUi

