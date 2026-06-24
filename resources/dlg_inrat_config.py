# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dlg_inrat_configlFHZiE.ui'
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
    QFrame, QGridLayout, QGroupBox, QHBoxLayout,
    QLabel, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)
import resources.resources_rc

class Ui_DlgDeviceConfig(object):
    def setupUi(self, DlgDeviceConfig):
        if not DlgDeviceConfig.objectName():
            DlgDeviceConfig.setObjectName(u"DlgDeviceConfig")
        DlgDeviceConfig.resize(828, 540)
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
        font = QFont()
        font.setPointSize(12)
        self.pushButtonOk.setFont(font)

        self.horizontalLayout.addWidget(self.pushButtonOk)

        self.pushButtonCancel = QPushButton(DlgDeviceConfig)
        self.pushButtonCancel.setObjectName(u"pushButtonCancel")
        self.pushButtonCancel.setFont(font)

        self.horizontalLayout.addWidget(self.pushButtonCancel)


        self.gridLayout.addLayout(self.horizontalLayout, 8, 0, 1, 1)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.checkBoxExg = QCheckBox(DlgDeviceConfig)
        self.checkBoxExg.setObjectName(u"checkBoxExg")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkBoxExg.sizePolicy().hasHeightForWidth())
        self.checkBoxExg.setSizePolicy(sizePolicy)
        self.checkBoxExg.setMinimumSize(QSize(235, 0))
        self.checkBoxExg.setMaximumSize(QSize(400, 16777215))
        self.checkBoxExg.setFont(font)

        self.horizontalLayout_3.addWidget(self.checkBoxExg)

        self.comboBoxModeSampleRate = QComboBox(DlgDeviceConfig)
        self.comboBoxModeSampleRate.setObjectName(u"comboBoxModeSampleRate")
        self.comboBoxModeSampleRate.setEnabled(False)
        sizePolicy.setHeightForWidth(self.comboBoxModeSampleRate.sizePolicy().hasHeightForWidth())
        self.comboBoxModeSampleRate.setSizePolicy(sizePolicy)
        self.comboBoxModeSampleRate.setMinimumSize(QSize(150, 0))
        self.comboBoxModeSampleRate.setMaximumSize(QSize(150, 16777215))
        self.comboBoxModeSampleRate.setFont(font)

        self.horizontalLayout_3.addWidget(self.comboBoxModeSampleRate)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_4)

        self.labelHpf = QLabel(DlgDeviceConfig)
        self.labelHpf.setObjectName(u"labelHpf")
        self.labelHpf.setEnabled(False)
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.labelHpf.sizePolicy().hasHeightForWidth())
        self.labelHpf.setSizePolicy(sizePolicy1)
        self.labelHpf.setMinimumSize(QSize(30, 0))
        self.labelHpf.setFont(font)
        self.labelHpf.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.labelHpf.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.labelHpf)

        self.comboBoxHpf = QComboBox(DlgDeviceConfig)
        self.comboBoxHpf.setObjectName(u"comboBoxHpf")
        self.comboBoxHpf.setEnabled(False)
        self.comboBoxHpf.setMinimumSize(QSize(75, 0))
        self.comboBoxHpf.setFont(font)

        self.horizontalLayout_3.addWidget(self.comboBoxHpf)

        self.labelGain = QLabel(DlgDeviceConfig)
        self.labelGain.setObjectName(u"labelGain")
        self.labelGain.setEnabled(False)
        self.labelGain.setMinimumSize(QSize(30, 0))
        self.labelGain.setFont(font)
        self.labelGain.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.labelGain.setInputMethodHints(Qt.InputMethodHint.ImhNone)
        self.labelGain.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.labelGain)

        self.comboBoxGain = QComboBox(DlgDeviceConfig)
        self.comboBoxGain.setObjectName(u"comboBoxGain")
        self.comboBoxGain.setEnabled(False)
        sizePolicy.setHeightForWidth(self.comboBoxGain.sizePolicy().hasHeightForWidth())
        self.comboBoxGain.setSizePolicy(sizePolicy)
        self.comboBoxGain.setMinimumSize(QSize(100, 0))
        self.comboBoxGain.setMaximumSize(QSize(150, 16777215))
        self.comboBoxGain.setFont(font)

        self.horizontalLayout_3.addWidget(self.comboBoxGain)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.checkBoxAcceleration = QCheckBox(DlgDeviceConfig)
        self.checkBoxAcceleration.setObjectName(u"checkBoxAcceleration")
        sizePolicy.setHeightForWidth(self.checkBoxAcceleration.sizePolicy().hasHeightForWidth())
        self.checkBoxAcceleration.setSizePolicy(sizePolicy)
        self.checkBoxAcceleration.setMinimumSize(QSize(235, 0))
        self.checkBoxAcceleration.setMaximumSize(QSize(400, 16777215))
        self.checkBoxAcceleration.setFont(font)

        self.horizontalLayout_5.addWidget(self.checkBoxAcceleration)

        self.labelFullScale = QLabel(DlgDeviceConfig)
        self.labelFullScale.setObjectName(u"labelFullScale")
        self.labelFullScale.setEnabled(False)
        self.labelFullScale.setFont(font)

        self.horizontalLayout_5.addWidget(self.labelFullScale)

        self.comboBoxFullScaleAccelerometer = QComboBox(DlgDeviceConfig)
        self.comboBoxFullScaleAccelerometer.setObjectName(u"comboBoxFullScaleAccelerometer")
        self.comboBoxFullScaleAccelerometer.setEnabled(False)
        sizePolicy.setHeightForWidth(self.comboBoxFullScaleAccelerometer.sizePolicy().hasHeightForWidth())
        self.comboBoxFullScaleAccelerometer.setSizePolicy(sizePolicy)
        self.comboBoxFullScaleAccelerometer.setMinimumSize(QSize(150, 0))
        self.comboBoxFullScaleAccelerometer.setFont(font)

        self.horizontalLayout_5.addWidget(self.comboBoxFullScaleAccelerometer)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_3)


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.checkBoxTemp = QCheckBox(DlgDeviceConfig)
        self.checkBoxTemp.setObjectName(u"checkBoxTemp")
        sizePolicy.setHeightForWidth(self.checkBoxTemp.sizePolicy().hasHeightForWidth())
        self.checkBoxTemp.setSizePolicy(sizePolicy)
        self.checkBoxTemp.setMinimumSize(QSize(235, 0))
        self.checkBoxTemp.setMaximumSize(QSize(400, 16777215))
        self.checkBoxTemp.setFont(font)

        self.horizontalLayout_4.addWidget(self.checkBoxTemp)

        self.labelInfoTemperature = QLabel(DlgDeviceConfig)
        self.labelInfoTemperature.setObjectName(u"labelInfoTemperature")
        self.labelInfoTemperature.setFont(font)

        self.horizontalLayout_4.addWidget(self.labelInfoTemperature)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_5)


        self.verticalLayout.addLayout(self.horizontalLayout_4)


        self.gridLayout.addLayout(self.verticalLayout, 2, 0, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.labelDeviceValue = QLabel(DlgDeviceConfig)
        self.labelDeviceValue.setObjectName(u"labelDeviceValue")
        self.labelDeviceValue.setFont(font)

        self.horizontalLayout_2.addWidget(self.labelDeviceValue)

        self.labelSnValue = QLabel(DlgDeviceConfig)
        self.labelSnValue.setObjectName(u"labelSnValue")
        self.labelSnValue.setFont(font)

        self.horizontalLayout_2.addWidget(self.labelSnValue)

        self.labelModelValue = QLabel(DlgDeviceConfig)
        self.labelModelValue.setObjectName(u"labelModelValue")
        self.labelModelValue.setFont(font)

        self.horizontalLayout_2.addWidget(self.labelModelValue)

        self.labelFirmwareValue = QLabel(DlgDeviceConfig)
        self.labelFirmwareValue.setObjectName(u"labelFirmwareValue")
        self.labelFirmwareValue.setFont(font)

        self.horizontalLayout_2.addWidget(self.labelFirmwareValue)

        self.labelHardwareValue = QLabel(DlgDeviceConfig)
        self.labelHardwareValue.setObjectName(u"labelHardwareValue")
        self.labelHardwareValue.setFont(font)

        self.horizontalLayout_2.addWidget(self.labelHardwareValue)


        self.gridLayout.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)

        self.groupBoxEnabledEvents = QGroupBox(DlgDeviceConfig)
        self.groupBoxEnabledEvents.setObjectName(u"groupBoxEnabledEvents")
        self.groupBoxEnabledEvents.setFont(font)
        self.groupBoxEnabledEvents.setFlat(False)
        self.groupBoxEnabledEvents.setCheckable(False)
        self.gridLayout_2 = QGridLayout(self.groupBoxEnabledEvents)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayoutEvents = QGridLayout()
        self.gridLayoutEvents.setObjectName(u"gridLayoutEvents")
        self.checkBoxFreefall = QCheckBox(self.groupBoxEnabledEvents)
        self.checkBoxFreefall.setObjectName(u"checkBoxFreefall")
        self.checkBoxFreefall.setFont(font)

        self.gridLayoutEvents.addWidget(self.checkBoxFreefall, 4, 0, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayoutEvents.addItem(self.horizontalSpacer_2, 1, 2, 1, 1)

        self.labelInfoOrientation = QLabel(self.groupBoxEnabledEvents)
        self.labelInfoOrientation.setObjectName(u"labelInfoOrientation")
        self.labelInfoOrientation.setFont(font)

        self.gridLayoutEvents.addWidget(self.labelInfoOrientation, 5, 1, 1, 1)

        self.checkBoxActivity = QCheckBox(self.groupBoxEnabledEvents)
        self.checkBoxActivity.setObjectName(u"checkBoxActivity")
        self.checkBoxActivity.setFont(font)

        self.gridLayoutEvents.addWidget(self.checkBoxActivity, 1, 0, 1, 1)

        self.labelInfoActivity = QLabel(self.groupBoxEnabledEvents)
        self.labelInfoActivity.setObjectName(u"labelInfoActivity")
        self.labelInfoActivity.setFont(font)

        self.gridLayoutEvents.addWidget(self.labelInfoActivity, 1, 1, 1, 1)

        self.checkBoxOrientation = QCheckBox(self.groupBoxEnabledEvents)
        self.checkBoxOrientation.setObjectName(u"checkBoxOrientation")
        self.checkBoxOrientation.setFont(font)

        self.gridLayoutEvents.addWidget(self.checkBoxOrientation, 5, 0, 1, 1)

        self.labelInfoFreefall = QLabel(self.groupBoxEnabledEvents)
        self.labelInfoFreefall.setObjectName(u"labelInfoFreefall")
        self.labelInfoFreefall.setFont(font)

        self.gridLayoutEvents.addWidget(self.labelInfoFreefall, 4, 1, 1, 1)

        self.labelActivityThreshold = QLabel(self.groupBoxEnabledEvents)
        self.labelActivityThreshold.setObjectName(u"labelActivityThreshold")
        self.labelActivityThreshold.setFont(font)

        self.gridLayoutEvents.addWidget(self.labelActivityThreshold, 6, 0, 1, 1)

        self.comboBoxActivityThreshold = QComboBox(self.groupBoxEnabledEvents)
        self.comboBoxActivityThreshold.setObjectName(u"comboBoxActivityThreshold")
        self.comboBoxActivityThreshold.setEnabled(False)
        sizePolicy.setHeightForWidth(self.comboBoxActivityThreshold.sizePolicy().hasHeightForWidth())
        self.comboBoxActivityThreshold.setSizePolicy(sizePolicy)
        self.comboBoxActivityThreshold.setMinimumSize(QSize(150, 0))
        self.comboBoxActivityThreshold.setFont(font)

        self.gridLayoutEvents.addWidget(self.comboBoxActivityThreshold, 6, 2, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayoutEvents, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.groupBoxEnabledEvents, 4, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 6, 0, 1, 1)

        self.line = QFrame(DlgDeviceConfig)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout.addWidget(self.line, 1, 0, 1, 1)


        self.retranslateUi(DlgDeviceConfig)

        QMetaObject.connectSlotsByName(DlgDeviceConfig)
    # setupUi

    def retranslateUi(self, DlgDeviceConfig):
        DlgDeviceConfig.setWindowTitle(QCoreApplication.translate("DlgDeviceConfig", u"\u041d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0430 \u043f\u0430\u0440\u0430\u043c\u0435\u0442\u0440\u043e\u0432", None))
        self.pushButtonOk.setText(QCoreApplication.translate("DlgDeviceConfig", u"\u041e\u043a", None))
        self.pushButtonCancel.setText(QCoreApplication.translate("DlgDeviceConfig", u"\u041e\u0442\u043c\u0435\u043d\u0430", None))
        self.checkBoxExg.setText(QCoreApplication.translate("DlgDeviceConfig", u"ExG", None))
        self.labelHpf.setText(QCoreApplication.translate("DlgDeviceConfig", u"\u0424\u0412\u0427:", None))
        self.labelGain.setText(QCoreApplication.translate("DlgDeviceConfig", u"\u0423\u0441\u0438\u043b\u0435\u043d\u0438\u0435:", None))
        self.checkBoxAcceleration.setText(QCoreApplication.translate("DlgDeviceConfig", u"\u0410\u043a\u0441\u0435\u043b\u0435\u0440\u043e\u043c\u0435\u0442\u0440", None))
        self.labelFullScale.setText(QCoreApplication.translate("DlgDeviceConfig", u"\u041c\u0430\u0441\u0448\u0442\u0430\u0431:", None))
#if QT_CONFIG(tooltip)
        self.checkBoxTemp.setToolTip(QCoreApplication.translate("DlgDeviceConfig", u"\u0420\u0435\u0433\u0438\u0441\u0442\u0440\u0430\u0446\u0438\u044f \u0441\u043e\u0431\u044b\u0442\u0438\u044f \u0442\u0435\u043c\u043f\u0435\u0440\u0430\u0442\u0443\u0440\u044b\n"
"", None))
#endif // QT_CONFIG(tooltip)
        self.checkBoxTemp.setText(QCoreApplication.translate("DlgDeviceConfig", u"\u0422\u0435\u043c\u043f\u0435\u0440\u0430\u0442\u0443\u0440\u0430 (T)", None))
#if QT_CONFIG(tooltip)
        self.labelInfoTemperature.setToolTip(QCoreApplication.translate("DlgDeviceConfig", u"<html><head/><body><p>\u0421\u043e\u0431\u044b\u0442\u0438\u0435 &quot;\u0422\u0435\u043c\u043f\u0435\u0440\u0430\u0442\u0443\u0440\u0430&quot;</p><p>\u0415\u0434\u0438\u043d\u0438\u0446\u044b \u0438\u0437\u043c\u0435\u0440\u0435\u043d\u0438\u044f: \u0433\u0440\u0430\u0434\u0443\u0441\u044b \u0426\u0435\u043b\u044c\u0441\u0438\u044f (\u00b0C)<br/>\u0424\u043e\u0440\u043c\u0430\u0442 \u0437\u0430\u043f\u0438\u0441\u0438: T {\u0437\u043d\u0430\u0447\u0435\u043d\u0438\u0435}</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.labelInfoTemperature.setText(QCoreApplication.translate("DlgDeviceConfig", u"?", None))
        self.labelDeviceValue.setText(QCoreApplication.translate("DlgDeviceConfig", u"inRat-1", None))
        self.labelSnValue.setText(QCoreApplication.translate("DlgDeviceConfig", u"SN ...", None))
        self.labelModelValue.setText(QCoreApplication.translate("DlgDeviceConfig", u"Model ...", None))
        self.labelFirmwareValue.setText(QCoreApplication.translate("DlgDeviceConfig", u"Firmware ...", None))
        self.labelHardwareValue.setText(QCoreApplication.translate("DlgDeviceConfig", u"Hardware ...", None))
        self.groupBoxEnabledEvents.setTitle(QCoreApplication.translate("DlgDeviceConfig", u"\u0421\u043e\u0431\u044b\u0442\u0438\u044f", None))
        self.checkBoxFreefall.setText(QCoreApplication.translate("DlgDeviceConfig", u"\u041d\u0435\u0432\u0435\u0441\u043e\u043c\u043e\u0441\u0442\u044c (F)", None))
#if QT_CONFIG(tooltip)
        self.labelInfoOrientation.setToolTip(QCoreApplication.translate("DlgDeviceConfig", u"<html><head/><body><p>\u0421\u043e\u0431\u044b\u0442\u0438\u0435 &quot;\u0421\u043c\u0435\u043d\u0430 \u043e\u0440\u0438\u0435\u043d\u0442\u0430\u0446\u0438\u0438&quot;</p><p>\u0424\u043e\u0440\u043c\u0430\u0442 \u0437\u0430\u043f\u0438\u0441\u0438: O {code}</p><p>\u041a\u043e\u0434\u044b \u043e\u0440\u0438\u0435\u043d\u0442\u0430\u0446\u0438\u0438:</p><p><span style=\" font-family:'Courier New';\">- x+</span> \u2014 \u0434\u0430\u0442\u0447\u0438\u043a \u043d\u0430 \u043b\u0435\u0432\u043e\u043c \u0431\u043e\u043a\u0443</p><p><span style=\" font-family:'Courier New';\">- x-</span> \u2014 \u0434\u0430\u0442\u0447\u0438\u043a \u043d\u0430 \u043f\u0440\u0430\u0432\u043e\u043c \u0431\u043e\u043a\u0443</p><p><span style=\" font-family:'Courier New';\">- y+</span> \u2014 \u0434\u0430\u0442\u0447\u0438\u043a \u0432\u0435\u0440\u0442\u0438\u043a\u0430\u043b\u044c\u043d\u043e</p><p><span style=\" font-family:'Courier New';\">- y-</span> \u2014 \u0434\u0430\u0442\u0447\u0438\u043a \u043f\u0435\u0440\u0435\u0432\u0451\u0440"
                        "\u043d\u0443\u0442</p><p><span style=\" font-family:'Courier New';\">- z+</span> \u2014 \u0434\u0430\u0442\u0447\u0438\u043a \u043b\u0438\u0446\u043e\u043c \u0432\u0432\u0435\u0440\u0445</p><p><span style=\" font-family:'Courier New';\">- z-</span> \u2014 \u0434\u0430\u0442\u0447\u0438\u043a \u043b\u0438\u0446\u043e\u043c \u0432\u043d\u0438\u0437</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.labelInfoOrientation.setText(QCoreApplication.translate("DlgDeviceConfig", u"?", None))
        self.checkBoxActivity.setText(QCoreApplication.translate("DlgDeviceConfig", u"\u0410\u043a\u0442\u0438\u0432\u043d\u043e\u0441\u0442\u044c (A)", None))
#if QT_CONFIG(tooltip)
        self.labelInfoActivity.setToolTip(QCoreApplication.translate("DlgDeviceConfig", u"<html><head/><body><p>\u0421\u043e\u0431\u044b\u0442\u0438\u0435 &quot;\u0410\u043a\u0442\u0438\u0432\u043d\u043e\u0441\u0442\u044c&quot;</p><p>\u0423\u0441\u043b\u043e\u0432\u0438\u0435 \u0441\u0440\u0430\u0431\u0430\u0442\u044b\u0432\u0430\u043d\u0438\u044f: \u043f\u0440\u0435\u0432\u044b\u0448\u0435\u043d\u0438\u0435 \u043f\u043e\u0440\u043e\u0433\u0430 \u0443\u0441\u043a\u043e\u0440\u0435\u043d\u0438\u044f \u043f\u043e \u043e\u0434\u043d\u043e\u0439 \u0438\u0437 \u043e\u0441\u0435\u0439.<br/>\u0424\u043e\u0440\u043c\u0430\u0442 \u0437\u0430\u043f\u0438\u0441\u0438: A {x} {y} {z}</p><p> - \u0443\u0441\u043a\u043e\u0440\u0435\u043d\u0438\u0435 \u0432 \u043c\u0438\u043b\u043b\u0438-g (mg) \u043f\u043e \u043e\u0441\u044f\u043c X, Y, Z.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.labelInfoActivity.setText(QCoreApplication.translate("DlgDeviceConfig", u"?", None))
        self.checkBoxOrientation.setText(QCoreApplication.translate("DlgDeviceConfig", u"\u041e\u0440\u0438\u0435\u043d\u0442\u0430\u0446\u0438\u044f (O)", None))
#if QT_CONFIG(tooltip)
        self.labelInfoFreefall.setToolTip(QCoreApplication.translate("DlgDeviceConfig", u"<html><head/><body><p>\u0421\u043e\u0431\u044b\u0442\u0438\u0435 &quot;\u041f\u0440\u044b\u0436\u043e\u043a&quot;</p><p>\u0423\u0441\u043b\u043e\u0432\u0438\u0435 \u0441\u0440\u0430\u0431\u0430\u0442\u044b\u0432\u0430\u043d\u0438\u044f: \u0443\u0441\u043a\u043e\u0440\u0435\u043d\u0438\u0435 \u043f\u043e \u043e\u0441\u044f\u043c X, Y, Z \u0431\u043b\u0438\u0437\u043a\u043e \u043a 0.</p><p>\u0424\u043e\u0440\u043c\u0430\u0442 \u0437\u0430\u043f\u0438\u0441\u0438: &quot;F&quot;</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.labelInfoFreefall.setText(QCoreApplication.translate("DlgDeviceConfig", u"?", None))
        self.labelActivityThreshold.setText(QCoreApplication.translate("DlgDeviceConfig", u"\u0427\u0443\u0441\u0442\u0432\u0438\u0442\u0435\u043b\u044c\u043d\u043e\u0441\u0442\u044c \u0440\u0435\u0433\u0438\u0441\u0442\u0440\u0430\u0446\u0438\u0438 ", None))
    # retranslateUi

