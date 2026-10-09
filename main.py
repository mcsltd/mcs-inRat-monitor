import logging
import sys

from PySide6 import QtAsyncio
from PySide6.QtCore import QSettings
from PySide6.QtWidgets import QMainWindow, QApplication, QMessageBox, QHBoxLayout, QFrame
from bleak import BLEDevice

from detector.peak_detector import RPeakDetector
from device.device import inRatDevice
from device.enums import TypeSignal
from ble_scanner.scanner import BleScanner
from events import DeviceEvent
from stream_viewer.stream_viewer import StreamViewer, TempStreamViewer, FrmControlXYRange
from ui.dlg_config import DlgConfig
from utils.check_bluetooth import check_bluetooth_status
from storage.storage import Storage
from resources.main_window_v1 import Ui_MainWindow
from widget import WaitingDialog


# constants
COMPANY_NAME = "Medical Computer Systems Ltd"
APP_NAME = "inRat monitor"
__version__ = "1.2.4"

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

        # main classes
        self.device = inRatDevice(qt_loop)
        self.scanner = BleScanner(qt_loop)
        self.storage = Storage(self.settings)
        self._detector = RPeakDetector()

        # отображение сигнала exg
        self.layout_control_pane_exg = QHBoxLayout()
        self.control_pane_sig = FrmControlXYRange(
            parent=self,
            x_values=[("1 c", 1), ("5 c", 5), ("10 c", 10), ("30 c", 30), ("60 c", 60)], default_idx_x=2,
            y_values=[("АРУ", None), ("±0.3 мВ", 0.3 * 1e-3), ("±0.5 мВ", 0.5 * 1e-3),
                      ("±1 мВ", 1 * 1e-3), ("±1.5 мВ", 1.5 * 1e-3), ("±2 мВ", 2 * 1e-3)], default_idx_y=0,
        )
        self.display_sig = StreamViewer(TypeSignal.ECG.value)
        self.control_pane_sig.signal_x_changed.connect(self.display_sig.set_x_range)
        self.control_pane_sig.signal_y_changed.connect(self.display_sig.set_y_range)
        self.layout_control_pane_exg.addStretch()
        self.layout_control_pane_exg.addWidget(self.control_pane_sig)
        self.verticalLayoutDisplay.addLayout(self.layout_control_pane_exg)
        self.verticalLayoutDisplay.addWidget(self.display_sig)

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
        self.verticalLayoutDisplay.addLayout(self.layout_control_pane_acc)
        self.verticalLayoutDisplay.addWidget(self.display_acc)

        # отображение сигнала температуры
        self.display_temp = TempStreamViewer(left_label="temp", units="°C")
        self.device.add_receiver_data(self.storage)
        self.verticalLayoutDisplay.addWidget(self.display_temp)

        self.enable_display_sig(False)
        self.enable_display_acc(False)
        self.enable_display_temp(False)

        self.horizontalLayoutStatusBar.addWidget(self.device.battery_pane)
        self.device.battery_pane.setVisible(False)

        # connection
        self.device.signal_enable_sig.connect(self.enable_display_sig)
        self.device.signal_enable_acc.connect(self.enable_display_acc)
        self.device.signal_enable_temp.connect(self.enable_display_temp)

        self.device.event.connect(self.process_event)

        self.scanner.signal_connect.connect(self.device.process_connect)
        self.pushButtonConfig.clicked.connect(self.on_config_clicked)

        # ui elements
        self._waiting_connection_dlg = WaitingDialog(self)

        self.actionExit.triggered.connect(self.close)
        self.horizontalLayoutControlPane.insertWidget(0, self.scanner.control_pane)
        self.horizontalLayoutControlPane.insertWidget(1, self.device.control_pane)
        self.horizontalLayoutControlPane.insertWidget(2, self.storage.control_pane)

    def process_event(self, event):
        """ обработка приходящих событий от модулей """
        if isinstance(event, DeviceEvent):
            self.__process_event_device(event)

    def __process_event_device(self, event: DeviceEvent):
        """
        Логика поведения главного окна при событиях устройства
        Виды событий:

        - ConnectionStart
        - ConnectionStop
        - ConnectionError
        - ConnectionLost - для случая переподключения

        - AcquisitionStart
        - AcquisitionStop
        - AcquisitionError

        - Disconnect
         """
        if event.type == "ConnectStart":
            self.pushButtonConfig.setEnabled(True)
            self._waiting_connection_dlg.show()
        elif event.type == "ConnectStop":
            self._waiting_connection_dlg.close()
            self.device.battery_pane.setVisible(True)

        # todo add event - ConnectionStart, ConnectionStop, ConnectionError, ConnectionLost, \
        if event.type == "AcquisitionStart":
            self.pushButtonConfig.setEnabled(False)
        if event.type == "AcquisitionStop":
            self.pushButtonConfig.setEnabled(True)
        if event.type == "Disconnect":
            self.device.stop()
            self.device.process_disconnect()
            self.pushButtonConfig.setEnabled(False)
            self._waiting_connection_dlg.close()
            self.device.battery_pane.setVisible(False)
        if event.type == "ConnectionLost":
            self.device.stop()
            self.pushButtonConfig.setEnabled(False)

    def enable_display_acc(self, state: bool):
        logger.debug("Активация окна отображения сигналов ЭКГ/ЭМГ")
        if state:
            self.device.add_receiver_acc(self.display_acc)
            self.display_acc.setVisible(True)
            self.control_pane_acc.setVisible(True)
        else:
            self.device.remove_receiver_acc(self.display_acc)
            self.display_acc.setVisible(False)
            self.control_pane_acc.setVisible(False)

    def enable_display_sig(self, state: bool):
        logger.debug("Активация окна отображения сигналов ЭКГ/ЭМГ")
        if state:
            self.device.add_receiver_exg(self.display_sig)
            self.display_sig.add_receiver(self._detector)
            self._detector.add_receiver(self.storage)

            self.display_sig.setVisible(True)
            self.control_pane_sig.setVisible(True)
        else:
            self.device.remove_receiver_sig(self.display_sig)
            self.display_sig.setVisible(False)
            self.control_pane_sig.setVisible(False)

    def enable_display_temp(self, state: bool):
        logger.debug("Активация окна отображения сигналов ЭКГ/ЭМГ")
        if state:
            self.device.add_receiver_temp(self.display_temp)
            self.display_temp.setVisible(True)
        else:
            self.device.remove_receiver_temp()
            self.display_temp.setVisible(False)

    def show_message_error(self, msg: str):
        QMessageBox.critical(self,"Ошибка", msg, QMessageBox.StandardButton.Ok)

    def closeEvent(self, event):
        self.scanner.stop()
        if self.device.is_running():
            self.device.stop()

        # save basic settings
        self.storage.save_settings()

    def on_config_clicked(self):
        """ открытие окна настроек """
        dlg = DlgConfig()
        pane = self.device.config_pane
        dlg.add_pane(pane)
        try:
            dlg.exec()
        finally:
            pane.setParent(None)


if __name__ == "__main__":
    app = QApplication([])
    loop = QtAsyncio.QAsyncioEventLoop(application=app)

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
