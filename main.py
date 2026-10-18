import logging
import sys

from PySide6 import QtAsyncio
from PySide6.QtCore import Qt, QSettings, QTimer
from PySide6.QtWidgets import (
    QMainWindow, QApplication, QMessageBox, QHBoxLayout, QVBoxLayout,
    QFrame, QSplitter, QWidget,
)

from camera.camera import Camera
from detector.peak_detector import QrsDetector
from device.device import inRatDevice
from device.enums import TypeSignal
from ble_scanner.scanner import BleScanner
from events import DeviceEvent
from stream_viewer.stream_viewer import StreamViewer, TempStreamViewer, FrmControlXYRange
from ui.dlg_about import AboutDialog
from ui.dlg_config import DlgConfig
from utils.check_bluetooth import check_bluetooth_status
from storage.storage import Storage
from resources.main_window_v1 import Ui_MainWindow
from widget import WaitingDialog


# constants
COMPANY_NAME = "Medical Computer Systems Ltd"
APP_NAME = "inRat monitor"
__version__ = "1.2.5"

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, qt_loop: QtAsyncio.QAsyncioEventLoop, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.setWindowTitle(f"{APP_NAME} v{__version__}")

        # settings
        self.settings = QSettings("MCS.ltd", "inRat monitor")

        # hide
        # self.pushButtonDisconnect.hide()
        self.qt_loop = qt_loop

        # флаг отложенного завершения приложения
        self._closing = False

        # main classes
        self.device = inRatDevice(qt_loop)
        self.scanner = BleScanner(qt_loop)
        self.storage = Storage(self.settings)
        self.camera = Camera()
        self._detector = QrsDetector()

        # отображение сигнала exg
        self.layout_control_pane_exg = QHBoxLayout()
        self.control_pane_sig = FrmControlXYRange(
            parent=self,
            x_values=[("1 c", 1), ("5 c", 5), ("10 c", 10), ("30 c", 30), ("60 c", 60)], default_idx_x=2,
            y_values=[("АРУ", None), ("±0.3 мВ", 0.3 * 1e-3), ("±0.5 мВ", 0.5 * 1e-3),
                      ("±1 мВ", 1 * 1e-3), ("±1.5 мВ", 1.5 * 1e-3), ("±2 мВ", 2 * 1e-3)], default_idx_y=0,
        )
        self.display_sig = StreamViewer(TypeSignal.ECG.value)
        self.display_sig.set_hr_enabled(self._detector.enable)
        self._detector.signal_enable_changed.connect(self.display_sig.set_hr_enabled)
        self.control_pane_sig.signal_x_changed.connect(self.display_sig.set_x_range)
        self.control_pane_sig.signal_y_changed.connect(self.display_sig.set_y_range)
        self.layout_control_pane_exg.addStretch()
        self.layout_control_pane_exg.addWidget(self.control_pane_sig)
        self.section_exg = QWidget()
        self._fill_section(self.section_exg, self.layout_control_pane_exg, self.display_sig)

        # отображение сигнала акселерометра
        self.layout_control_pane_acc = QHBoxLayout()
        self.control_pane_acc = FrmControlXYRange(
            parent=self,
            x_values=[("1 c", 1), ("5 c", 5), ("10 c", 10), ("30 c", 30), ("60 c", 60)],
            default_idx_x=2,
            y_values=[("АРУ", None), ("±1 G", 1), ("±2 G", 2.0), ("±4 G", 4.0), ("±8 G", 8.0), ("±16 G", 16.0)],
            default_idx_y=0,
        )
        self.display_acc = StreamViewer(TypeSignal.ACC.value)
        self.control_pane_acc.signal_x_changed.connect(self.display_acc.set_x_range)
        self.control_pane_acc.signal_y_changed.connect(self.display_acc.set_y_range)
        self.layout_control_pane_acc.addStretch()
        self.layout_control_pane_acc.addWidget(self.control_pane_acc)
        self.section_acc = QWidget()
        self._fill_section(self.section_acc, self.layout_control_pane_acc, self.display_acc)

        # отображение сигнала температуры
        self.display_temp = TempStreamViewer(left_label="temp", units="°C")
        self.device.add_receiver_data(self.storage)

        # вертикальный сплиттер секций графиков (перетаскиваемая высота)
        self.graphs_splitter = QSplitter(Qt.Orientation.Vertical)
        self.graphs_splitter.addWidget(self.section_exg)
        self.graphs_splitter.addWidget(self.section_acc)
        self.graphs_splitter.addWidget(self.display_temp)
        self.graphs_splitter.setSizes([260, 220, 140])
        self.graphs_splitter.setStretchFactor(0, 1)
        self.graphs_splitter.setStretchFactor(1, 1)
        self.graphs_splitter.setStretchFactor(2, 1)
        self.graphs_splitter.setChildrenCollapsible(False)
        self.graphs_splitter.setHandleWidth(6)

        # горизонтальный сплиттер: [графики | видео] (перетаскиваемая ширина)
        self.main_splitter = QSplitter(Qt.Orientation.Horizontal)
        self.main_splitter.addWidget(self.graphs_splitter)
        self.main_splitter.addWidget(self.camera.output_pane)
        self.main_splitter.setSizes([600, 600])
        self.main_splitter.setStretchFactor(0, 1)
        self.main_splitter.setStretchFactor(1, 1)
        self.main_splitter.setChildrenCollapsible(False)
        self.main_splitter.setHandleWidth(6)

        # заменяем статичные layout'ы области отображения сплиттером
        for _ in range(self.horizontalLayout_2.count()):
            self.horizontalLayout_2.removeItem(self.horizontalLayout_2.itemAt(0))
        self.horizontalLayout_2.addWidget(self.main_splitter)

        # область графиков забирает свободное место
        self.verticalLayout.setStretchFactor(self.horizontalLayout_2, 1)

        self.enable_display_sig(False)
        self.enable_display_acc(False)
        self.enable_display_temp(False)

        self.horizontalLayoutStatusBar.insertWidget(0, self.storage.info_pane)
        self.horizontalLayoutStatusBar.addWidget(self.device.battery_pane)
        self.device.battery_pane.setVisible(False)

        # фиксируем высоту строки состояния по самому высокому виджету
        status_widgets = (self.storage.info_pane, self.device.battery_pane)
        self.widgetStatusBar.setFixedHeight(
            max(widget.sizeHint().height() for widget in status_widgets)
        )

        # connection
        self.device.signal_enable_sig.connect(self.enable_display_sig)
        self.device.signal_enable_acc.connect(self.enable_display_acc)
        self.device.signal_enable_temp.connect(self.enable_display_temp)

        self.device.event.connect(self.process_event)
        # DevicePropertyEvent от устройства → Storage (имя устройства для папки записей)
        self.device.event.connect(self.storage.process_event)

        self.scanner.signal_connect.connect(self.device.process_connect)
        self.scanner.signal_scan_requested.connect(self.on_scan_requested)
        self.scanner.signal_scan_finished.connect(self.on_scan_finished)
        self.scanner.signal_found.connect(self.device.config_pane.add_device)
        self.pushButtonConfig.clicked.connect(self.on_config_clicked)

        # управление подключением из окна настроек устройства
        device_pane = self.device.config_pane
        device_pane.signal_connect_requested.connect(self.on_device_connect_requested)
        device_pane.signal_disconnect_requested.connect(self.on_device_disconnect_requested)
        device_pane.signal_device_selected.connect(self.on_device_selected)

        # применение настроек модулей (подключение один раз)
        device_pane.signal_apply.connect(self.device.process_update)
        self.storage.config_pane.signal_apply.connect(self.storage.process_update)
        self._detector.config_pane.signal_apply.connect(self._detector.process_update)
        self.camera.config_pane.signal_apply.connect(self.camera.process_update)

        # запись видео синхронна с записью сигналов (тот же старт/стоп/ролловер)
        self.camera.set_video_file_provider(self.storage.make_video_file_path)
        self.storage.signal_recording_started.connect(
            lambda *_: self.camera.start_video_recording()
        )
        self.storage.signal_recording_new_file.connect(
            lambda *_: self.camera.rotate_video_recording()
        )
        self.storage.signal_recording_stopped.connect(self.camera.stop_video_recording)

        # настройки доступны всегда: подключение/отключение устройства выполняется в них
        self.pushButtonConfig.setEnabled(True)

        # ui elements
        self._waiting_connection_dlg = WaitingDialog(self)

        self.actionAbout.triggered.connect(self._on_about_clicked)
        self.actionExit.triggered.connect(self.close)

        modules = [
            self.scanner.control_pane,
            self.device.control_pane,
            self.storage.control_pane,
        ]
        row = []
        for idx, pane in enumerate(modules):
            if idx > 0:
                row.append(self._make_module_separator())
            row.append(pane)
        for item in reversed(row):
            self.horizontalLayoutControlPane.insertWidget(0, item)

    def _make_module_separator(self) -> QFrame:
        """ вертикальный разделитель между панелями управления модулями """
        line = QFrame(self)
        line.setFrameShape(QFrame.Shape.VLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        return line

    @staticmethod
    def _fill_section(section: QWidget, control_layout, plot) -> None:
        """ наполнение секции сплиттера: строка управления + график """
        layout = QVBoxLayout(section)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)
        layout.addLayout(control_layout)
        layout.addWidget(plot, 1)


    def process_event(self, event):
        """ обработка приходящих событий от модулей """
        if isinstance(event, DeviceEvent):
            self.__process_event_device(event)

    def __process_event_device(self, event: DeviceEvent):
        """
        Логика поведения главного окна при событиях устройства
         """

        if event.type == "ConnectStart":
            self.pushButtonConfig.setEnabled(True)
            self._waiting_connection_dlg.show()
        elif event.type == "ConnectStop":
            self._waiting_connection_dlg.close()
            self.device.battery_pane.setVisible(True)
        elif event.type == "ConnectError":
            self._waiting_connection_dlg.close()
            self.device.battery_pane.setVisible(False)
            self.pushButtonConfig.setEnabled(True)
            self.scanner.set_enabled(True)
            self._offer_reconnect()

        if event.type == "AcquisitionStart":
            self.pushButtonConfig.setEnabled(False)
            self.scanner.set_enabled(False)
        if event.type == "AcquisitionStop":
            self.pushButtonConfig.setEnabled(True)
            self.scanner.set_enabled(True)
        if event.type == "Disconnect":
            self.device.stop()
            self.device.process_disconnect()
            self.pushButtonConfig.setEnabled(True)
            self._waiting_connection_dlg.close()
            self.device.battery_pane.setVisible(False)
        if event.type == "Disconnected":
            self._waiting_connection_dlg.close()
            self.device.battery_pane.setVisible(False)
            self.pushButtonConfig.setEnabled(True)
            self.scanner.set_enabled(True)
        if event.type == "ConnectionLost":
            self.device.battery_pane.setVisible(False)
            self.pushButtonConfig.setEnabled(True)
            self.scanner.set_enabled(True)
            QMessageBox.critical(
                self, "Потеря соединения",
                f"Потеряно соединение с устройством «{self.device.name}».",
            )

    def enable_display_acc(self, state: bool):
        logger.debug(f"Окно отображения сигналов акселерометра: {state}")
        if state:
            self.device.add_receiver_acc(self.display_acc)
            self.section_acc.setVisible(True)
        else:
            self.device.remove_receiver_acc(self.display_acc)
            self.section_acc.setVisible(False)

    def enable_display_sig(self, state: bool):
        logger.debug(f"Окно отображения сигналов ЭКГ/ЭМГ: {state}")
        if state:
            self.device.add_receiver_exg(self.display_sig)
            self.display_sig.add_receiver(self._detector)
            self.storage.add_receiver(self._detector)

            self.section_exg.setVisible(True)
        else:
            self.device.remove_receiver_sig(self.display_sig)
            self.display_sig.remove_receiver(self._detector)
            self.storage.remove_receiver(self._detector)
            self.section_exg.setVisible(False)

    def enable_display_temp(self, state: bool):
        logger.debug(f"Окно отображения сигнала температуры: {state}")
        if state:
            self.device.add_receiver_temp(self.display_temp)
            self.display_temp.setVisible(True)
        else:
            self.device.remove_receiver_temp()
            self.display_temp.setVisible(False)

    def show_message_error(self, msg: str):
        QMessageBox.critical(self,"Ошибка", msg, QMessageBox.StandardButton.Ok)

    def _offer_reconnect(self):
        """ предложение повторить неудачное подключение """
        box = QMessageBox(self)
        box.setIcon(QMessageBox.Icon.Warning)
        box.setWindowTitle("Ошибка подключения")
        box.setText(f"Не удалось подключиться к устройству «{self.device.name}».")
        box.setInformativeText("Повторить попытку подключения?")
        box.setStandardButtons(
            QMessageBox.StandardButton.Retry | QMessageBox.StandardButton.Cancel
        )
        box.button(QMessageBox.StandardButton.Retry).setText("Повторить")
        box.button(QMessageBox.StandardButton.Cancel).setText("Отмена")
        if box.exec() == QMessageBox.StandardButton.Retry:
            self.device.retry_connect()

    def closeEvent(self, event):
        # save basic settings
        self.storage.save_settings()

        if self._closing:
            event.accept()
            return

        # остановка поиска BLE (с ожиданием завершения корутины)
        scan_future = self.scanner.shutdown()

        # остановка приёма и отсоединение BLE-клиента
        disconnect_future = None
        if self.device.is_connected() or self.device.is_running():
            self.device.stop()
            disconnect_future = self.device.process_disconnect()

        pending = [f for f in (scan_future, disconnect_future) if f is not None]
        if not pending:
            event.accept()
            return

        # отложенное завершение: закрываем цикл только после отсоединения BLE,
        # иначе bleak обращается к уже закрытому циклу событий
        self._closing = True
        event.ignore()
        self.hide()

        remaining = {"count": len(pending)}

        def _on_done(_future):
            try:
                if not _future.cancelled():
                    _future.exception()
            except Exception:
                pass
            remaining["count"] -= 1
            if remaining["count"] <= 0:
                QTimer.singleShot(0, QApplication.instance().quit)

        for future in pending:
            future.add_done_callback(_on_done)

        # страховка на случай зависшего отсоединения
        QTimer.singleShot(3000, self._force_quit)

    def _force_quit(self):
        """ принудительное завершение приложения """
        QApplication.instance().quit()

    def on_config_clicked(self):
        """ открытие окна настроек """
        dlg = DlgConfig()

        pane_device = self.device.config_pane
        if pane_device:
            dlg.add_pane(pane_device)

        pane_storage = self.storage.config_pane
        pane_storage.set_default()
        dlg.add_pane(pane_storage)

        pane_detector = self._detector.config_pane
        dlg.add_pane(pane_detector)

        pane_camera = self.camera.config_pane
        pane_camera.set_default(
            self.camera.is_enabled, self.camera.camera_name
        )
        dlg.add_pane(pane_camera)

        try:
            dlg.exec()
        finally:
            if pane_device:
                pane_device.setParent(None)
            pane_detector.setParent(None)
            pane_storage.setParent(None)
            pane_camera.setParent(None)

    def on_scan_requested(self):
        """ обработка запроса поиска и подключения нового устройства """
        if not self.device.is_connected():
            self.scanner.start_scan()
            return

        if not self._confirm_disconnect_for_scan():
            return

        self._disconnect_then(self.scanner.start_scan)

    def on_device_connect_requested(self):
        """ включение устройства в настройках: запуск поиска устройств """
        if self.device.is_connected():
            return
        self.scanner.start_scan()

    def on_device_disconnect_requested(self):
        """ отключение устройства в настройках """
        if self.device.is_running():
            self.device.stop()
        if self.device.is_connected():
            self.device.process_disconnect()
        else:
            self.device.config_pane.set_connection_state(False)

    def on_device_selected(self, device):
        """ подключение к устройству, выбранному в настройках """
        if not device:
            return

        if self.device.is_connected():
            if self.device.name == device.name:
                return
            if not self._confirm_disconnect_for_scan(new_name=device.name):
                # выбор отменен - возврат к состоянию подключенного устройства
                self.device.config_pane.set_connection_state(True, self.device.name)
                return
            self._disconnect_then(lambda: self.device.process_connect(device))
            return

        self.device.process_connect(device)

    def on_scan_finished(self, selected: bool):
        """ обработка результата окна поиска """
        if not selected and not self.device.is_connected():
            # поиск закрыт без выбора устройства - возврат статуса в настройках
            self.device.config_pane.set_connection_state(False)

    def _confirm_disconnect_for_scan(self, new_name: str | None = None) -> bool:
        """ подтверждение разрыва текущего соединения ради нового подключения """
        if new_name:
            text = (
                f"Подключено устройство {self.device.name}. "
                f"Подключение к {new_name} разорвёт текущее соединение. Продолжить?"
            )
        else:
            text = (
                f"Подключено устройство {self.device.name}. "
                "Поиск нового устройства разорвёт текущее соединение. Продолжить?"
            )
        box = QMessageBox(self)
        box.setIcon(QMessageBox.Icon.Question)
        box.setWindowTitle("Новое подключение")
        box.setText(text)
        box.setStandardButtons(
            QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel
        )
        box.button(QMessageBox.StandardButton.Ok).setText("Продолжить")
        box.button(QMessageBox.StandardButton.Cancel).setText("Отмена")
        return box.exec() == QMessageBox.StandardButton.Ok

    def _disconnect_then(self, on_done):
        """ отключение устройства с последующим вызовом on_done """
        future = self.device.process_disconnect()
        if future is None:
            on_done()
        else:
            future.add_done_callback(lambda _: on_done())

    def _on_about_clicked(self):
        """ обработка нажатия на вкладку о Программе """
        dlg = AboutDialog(version=__version__, parent=self)
        dlg.show()

if __name__ == "__main__":
    app = QApplication([])
    loop = QtAsyncio.QAsyncioEventLoop(application=app)

    try:
        from bleak.backends.winrt.util import allow_sta
        allow_sta()
    except ImportError:
        pass

    from config import BLE_KEY
    if BLE_KEY is None:
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Critical)
        msg_box.setWindowTitle("Ошибка подключения")
        msg_box.setText("Отсутствует ключ для подключения к устройствам")
        msg_box.setInformativeText(
            "Ключ BLE_KEY не обнаружен в системных переменных.\n"
            "Пожалуйста, переустановите приложение, используя установщик."
        )
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.exec()

        app.quit()
        sys.exit(1)

    try:
        check_bluetooth_status()
    except Exception as exc:
        info = QMessageBox().information(
            None,
            "Bluetooth error",
            f"Bluetooth error\n\nInfo:\n{exc}",
            QMessageBox.StandardButton.Ok
        )
        app.quit()
    else:
        window = MainWindow(loop)
        window.showMaximized()

        try:
            loop.run_forever()
        except Exception as err:
            logger.error(f"Ошибка в цикле событий: {err}")
        finally:
            if loop.is_running():
                loop.stop()
