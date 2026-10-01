from PySide6.QtWidgets import QDialog, QFrame, QWidget, QGridLayout

from resources.dlg_config import Ui_DlgConfig


class DlgConfig(QDialog, Ui_DlgConfig):
    """ Диалоговое окно настройки модулей """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.panes = []

    def add_pane(self, pane: QFrame):
        """ добавление панелей для настройки модулей приложения """
        if not pane:
            return

        if self.panes:
            tab = QWidget()
            self.tabWidget.addTab(tab, "")
            gridlayout = QGridLayout(tab)
        else:
            tab = self.tab1
            gridlayout = tab.layout()
            if gridlayout is None:
                gridlayout = QGridLayout(tab)

        gridlayout.addWidget(pane)
        self.panes.append(pane)
        self.tabWidget.setTabText(self.tabWidget.indexOf(tab), pane.windowTitle())