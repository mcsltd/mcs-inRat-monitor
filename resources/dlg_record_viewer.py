# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dlg_record_vieweriXoNAC.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QMetaObject, QSize)
from PySide6.QtGui import (QIcon)
from PySide6.QtWidgets import (QGridLayout, QVBoxLayout)


class Ui_DlgRecordViewer(object):
    def setupUi(self, DlgRecordViewer):
        if not DlgRecordViewer.objectName():
            DlgRecordViewer.setObjectName(u"DlgRecordViewer")
        DlgRecordViewer.resize(1131, 730)
        icon = QIcon()
        icon.addFile(u":/iconMCS.ico", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        DlgRecordViewer.setWindowIcon(icon)
        self.gridLayout = QGridLayout(DlgRecordViewer)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayoutDisplay = QVBoxLayout()
        self.verticalLayoutDisplay.setObjectName(u"verticalLayoutDisplay")

        self.gridLayout.addLayout(self.verticalLayoutDisplay, 0, 0, 1, 1)


        self.retranslateUi(DlgRecordViewer)

        QMetaObject.connectSlotsByName(DlgRecordViewer)
    # setupUi

    def retranslateUi(self, DlgRecordViewer):
        DlgRecordViewer.setWindowTitle(QCoreApplication.translate("DlgRecordViewer", u"Dialog", None))
    # retranslateUi

