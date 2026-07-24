import logging

from PySide6 import QtAsyncio
from PySide6.QtWidgets import QMainWindow, QApplication, QMessageBox, QComboBox, QHBoxLayout
from bleak import BLEDevice

from device.device import inRatDevice
from device.enums import TypeSignal
from scanner import BLEScannerWorker
from stream_displays import StreamViewer, TempStreamViewer, FrmControlXYRange
from utils.check_bluetooth import check_bluetooth_status
from storage import DataStorage
from resources.main_window import Ui_MainWindow
from widget import WaitingDialog

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, qt_loop: QtAsyncio.QAsyncioEventLoop, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)

        # hide
        self.pushButtonDisconnect.hide()
        self.qt_loop = qt_loop

        # main classes
        self.device = inRatDevice(qt_loop)
        self.scanner = BLEScannerWorker()
        self.storage = DataStorage()

        # отображение сигнала exg
        self.layout_control_pane_exg = QHBoxLayout()
        self.control_pane_sig = FrmControlXYRange(
            parent=self,
            x_values=[("1 c", 1), ("5 c", 5), ("10 c", 10), ("30 c", 30), ("60 c", 60)],
            y_values=[("±0.3 мВ", 0.3 * 1e-3), ("±0.5 мВ", 0.5 * 1e-3),
                      ("±1 мВ", 1 * 1e-3), ("±1.5 мВ", 1.5 * 1e-3), ("±2 мВ", 2 * 1e-3)]
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
            y_values=[("±1 G", 1), ("±2 G", 2.0), ("±4 G", 4.0), ("±8 G", 8.0), ("±16 G", 16.0)]
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

        # create scanner and run it
        self.scanner.run(self.qt_loop)
        self.scanner.signal_found.connect(self.set_combobox_items)
        self.pushButtonConnect.setEnabled(False)

        # setup combobox
        self.comboBoxDevice.setDuplicatesEnabled(False)
        self.comboBoxDevice.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)

        self.verticalLayout.insertWidget(4, self.device.control_pane)
        self.verticalLayout.insertWidget(5, self.storage.control_pane)

        self.enable_display_sig(False)
        self.enable_display_acc(False)
        self.enable_display_temp(False)

        # connection
        self.pushButtonConnect.clicked.connect(self.on_connect_clicked)
        self.pushButtonDisconnect.clicked.connect(self.on_disconnect_clicked)
        self.device.signal_connected.connect(self.on_device_connected)
        self.device.signal_disconnected.connect(self.on_device_disconnected)
        self.device.signal_error.connect(self.show_message_error)

        self.device.signal_enable_sig.connect(self.enable_display_sig)
        self.device.signal_enable_acc.connect(self.enable_display_acc)
        self.device.signal_enable_temp.connect(self.enable_display_temp)

        # ui elements
        self._waiting_connection_dlg = WaitingDialog(self)

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
            self.device.add_receiver_sig(self.display_sig)
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

    def on_connect_clicked(self):
        """ обработка нажатия кнопки открытия устройства """
        self._waiting_connection_dlg.show()
        self.scanner.stop()

        device = self.comboBoxDevice.currentData()
        self.device.process_connect(device)

        self.comboBoxDevice.setDisabled(True)
        self.pushButtonConnect.setDisabled(True)

    def on_device_connected(self):
        """ обработка случая подключения устройства """
        self._waiting_connection_dlg.close()
        self.pushButtonConnect.hide()
        self.pushButtonDisconnect.setVisible(True)
        self.pushButtonDisconnect.setEnabled(True)

    def on_disconnect_clicked(self):
        """ обработка нажатия кнопки отсоединения от устройства """
        self.scanner.run(self.qt_loop)
        if self.device.is_running():
            self.device.stop()
        self.device.process_disconnect()

    def on_device_disconnected(self):
        """ обработка случая если устройство отсоединено """
        if not self.scanner.is_running():
            self.scanner.run(self.qt_loop)

        self._waiting_connection_dlg.close()
        self.pushButtonDisconnect.hide()
        self.pushButtonConnect.setVisible(True)
        self.comboBoxDevice.clear()
        self.comboBoxDevice.setEnabled(True)

    def set_combobox_items(self, devices: set[BLEDevice]):
        for device in devices:
            if self.comboBoxDevice.findText(device.name) == -1:
                self.comboBoxDevice.addItem(device.name, userData=device)
        if self.comboBoxDevice.count() != 0:
            self.pushButtonConnect.setEnabled(True)

    def show_message_error(self, msg: str):
        QMessageBox.critical(self,"Ошибка", msg, QMessageBox.StandardButton.Ok)

    def closeEvent(self, event):
        self.scanner.stop()
        if self.device.is_running():
            self.device.stop()

if __name__ == "__main__":
    app = QApplication([])
    loop = QtAsyncio.QAsyncioEventLoop(application=app)

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
