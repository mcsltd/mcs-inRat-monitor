from PySide6.QtCore import Signal
from PySide6.QtWidgets import QFrame, QFileDialog

from storage.models import StorageConfig
from storage.res.frm_config_storage import Ui_FrmConfigStoragePane


class FrmConfigStorage(QFrame, Ui_FrmConfigStoragePane):
    """ виджет для настройки параметров сохранения записей """
    signal_apply = Signal(object)

    def __init__(self, storage=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.setWindowTitle("Запись")

        self._storage = storage

        self.spinBoxDuration.setRange(1, 30)
        self.spinBoxDuration.setSuffix(" мин")

        self.set_default()

        self.pushButtonPath.clicked.connect(self._on_path_clicked)
        self.pushButtonOk.clicked.connect(self._on_ok_clicked)

    def set_default(self):
        """ установка текущих параметров записи """
        path = self._storage.write_dir if self._storage else None
        self.lineEditPath.setText(path or "")

        duration = self._storage.duration_min if self._storage else 20
        self.spinBoxDuration.setValue(duration)

    def _on_path_clicked(self):
        """ выбор места сохранения записей edf """
        path = QFileDialog.getExistingDirectory(
            self,
            "Выберите папку для сохранения записей",
            self.lineEditPath.text(),
            QFileDialog.Option.ShowDirsOnly | QFileDialog.Option.DontResolveSymlinks,
        )
        if path:
            self.lineEditPath.setText(path)

    def _on_ok_clicked(self):
        """ обработка нажатия кнопки применить """
        config = StorageConfig(
            write_dir=self.lineEditPath.text() or None,
            duration_min=self.spinBoxDuration.value(),
        )
        self.signal_apply.emit(config)
