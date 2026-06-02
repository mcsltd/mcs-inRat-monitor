import asyncio
import datetime
import logging
import time
from threading import Thread
from typing import Optional

import pyqtgraph as pg


from PySide6 import QtAsyncio
from PySide6.QtCore import Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QMainWindow, QApplication, QMessageBox, QComboBox, QFileDialog
from bleak import BLEDevice

from device.constants import Pkt
from device.inrat import InRat
from config import DATA_PATH
from device.ui.config_dialog import DlgConfigDevice
from device.ui.control_pane import FrmControlPane
from stream_displays import StreamAccelerationViewer, StreamSignalViewer
from scanner import BLEScannerWorker
from utils.check_bluetooth import check_bluetooth_status
from storage import DataStorage
from resources.main_window import Ui_MainWindow
from widget import WaitingDialog

logger = logging.getLogger(__name__)

HZ = 500
RED = pg.mkPen(color=(255, 0, 0), width=1.5)


class MainWindow(QMainWindow, Ui_MainWindow):

    signal_connect = Signal()

    def __init__(self, qt_loop: QtAsyncio.QAsyncioEventLoop, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        # self.setWindowTitle("InRat monitor")
        # self.setWindowIcon(QIcon("ui/iconMCS.ico"))

        # hide
        self.pushButtonDisconnect.hide()
        self.qt_loop = qt_loop

        # build queue
        self.ecg_queue = asyncio.Queue()
        self.event_queue = asyncio.Queue()
        self.acceleration_queue = asyncio.Queue()

        # main classes
        self.device: Optional[InRat] = None
        # self.storage = Storage(path_to_save=DATA_PATH, fs=HZ)
        self.scanner = BLEScannerWorker()

        # графики отображения сигналов
        self.plot_signal = StreamSignalViewer()
        self.verticalLayoutDisplay.insertWidget(0, self.plot_signal)
        self.plot_acceleration = StreamAccelerationViewer()
        self.verticalLayoutDisplay.insertWidget(1, self.plot_acceleration)

        # класс для сохранения данных с устройства
        self.data_storage = DataStorage()
        self.verticalLayout.insertWidget(6, self.data_storage.control_pane)

        # create scanner and run it
        self.scanner.run(self.qt_loop)
        self.scanner.signal_found.connect(self.set_combobox_items)
        self.pushButtonConnect.setEnabled(False)

        self._work: None | Thread = None
        self._running = False

        # setup combobox
        self.comboBoxDevice.setDuplicatesEnabled(False)
        self.comboBoxDevice.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)

        self.device_control_pane = FrmControlPane()
        self.verticalLayout.insertWidget(5, self.device_control_pane)
        self.device_control_pane.pushButtonStart.clicked.connect(lambda: asyncio.ensure_future(self.start_device()))
        self.device_control_pane.pushButtonStop.clicked.connect(lambda: asyncio.ensure_future(self.stop_device()))
        self.device_control_pane.pushButtonConfig.clicked.connect(self.on_config_clicked)

        # connection
        self.pushButtonConnect.clicked.connect(lambda: asyncio.ensure_future(self.connect_device()))
        self.pushButtonDisconnect.clicked.connect(lambda: asyncio.ensure_future(self.disconnect_device()))

    def set_combobox_items(self, devices: set[BLEDevice]):
        for device in devices:
            if self.comboBoxDevice.findText(device.name) == -1:
                self.comboBoxDevice.addItem(device.name, userData=device)
        if self.comboBoxDevice.count() != 0:
            self.pushButtonConnect.setEnabled(True)

    def on_config_clicked(self):
        dlg = DlgConfigDevice(self.device)
        dlg.exec()

    async def connect_device(self):
        # raise waiting dialog
        dlg = WaitingDialog(parent=self)
        dlg.show()

        # get device name for connection
        device = self.comboBoxDevice.currentData()
        idx_device = self.comboBoxDevice.currentIndex()
        logger.debug(f"Select device with name: {device.name}.")

        # stop scanner
        self.scanner.stop()
        # remove all device in combobox
        # disable combobox and button connect
        self.comboBoxDevice.setDisabled(True)
        self.pushButtonConnect.setDisabled(True)

        # reconnect with new device or old
        if self.device is not None and not self.device.is_connected:
            self.device = None
        try:
            self.device = InRat(ble_device=device)

            attempt_connection = 1
            while not self.device.is_connected and attempt_connection <= 5:
                logger.debug(f"Устройство найдено! Производится попытка подключиться. Номер попытки: {attempt_connection}")
                try:
                    await self.device.connect()
                except Exception as exc:
                    ...
                attempt_connection += 1

            # # add in storage device name (for write additional info in edf)
            # self.storage.set_device_name(self.device.name)
            self.device_control_pane.state_connection()

        except Exception as exc:
            self.device = None
            info = QMessageBox.information(
                self, "Connect error",
                f"An error occurred while connect to the device.\nCheck if the device has turned off.",
                QMessageBox.StandardButton.Ok
            )
            # remove device in combobox if not connected
            self.comboBoxDevice.removeItem(idx_device)
            self.comboBoxDevice.setEnabled(True)
            # run the scanner if can't connect
            self.scanner.run(self.qt_loop)
        else:
            # disable and activate btn state when connect to device
            if self.device.is_connected:
                self.device_control_pane.setEnabled(True)

                # проверка на активировано ли устройство
                if self.device.is_activated:
                    self.device_control_pane.checkBoxActivated.setChecked(True)

                self.device_control_pane.state_connection()

                self.pushButtonDisconnect.show()
                self.pushButtonConnect.hide()

        finally:
            dlg.close()

    async def disconnect_device(self):
        if self.device.is_connected:
            await self.device.disconnect()
        else:
            await self.lost_connection()

        self.scanner.run(self.qt_loop)

        # reset checkbox
        self.device_control_pane.checkBoxActivated.setChecked(False)
        self.device_control_pane.checkBoxActivated.setEnabled(False)
        self.device_control_pane.state_disconnect()

        # activate
        self.comboBoxDevice.clear()
        self.comboBoxDevice.setEnabled(True)

        self.pushButtonConnect.show()
        self.pushButtonDisconnect.hide()

    async def start_device(self):
        logger.debug("Start device")
        # очищение очередей перед стартом
        while not self.event_queue.empty():
            self.event_queue.get_nowait()
        while not self.ecg_queue.empty():
            self.ecg_queue.get_nowait()

        if not self.device.is_connected:
            info = QMessageBox.information(
                self, "Lost device connection",
                f"Lost connection with device {self.device.name}",
                buttons=QMessageBox.StandardButton.Ok
            )
            # reset all
            await self.disconnect_device()
            return

        await self.device.start_acquisition(signal_queue=self.ecg_queue,event_queue=self.event_queue, acceleration_queue=self.acceleration_queue)

        # настройка параметров записи
        self.data_storage.set_recording_params(
            sample_rate=self.device.sample_rate,
            samples_count=Pkt.SamplesCountEcg,
            frmt="EDF",
            device_name=self.device.name
        )
        self.data_storage.start()

        # disable
        self.pushButtonDisconnect.setEnabled(False)
        self.comboBoxDevice.setEnabled(False)
        self.device_control_pane.state_acquisition()

        self._running = True
        self._work = Thread(target=self._worker_thread)
        self._work.start()

    def _worker_thread(self):
        """ поток обработки очередей """
        while self._running:
            # вывод сигналов
            try:
                ecg = self.ecg_queue.get_nowait()

            except asyncio.QueueEmpty:
                ecg = None
            else:
                self.plot_signal.set_data(ecg)
                self.data_storage._input_queue.put(ecg)
                self.ecg_queue.task_done()

            # # обработка событий
            # try:
            #     event = self.event_queue.get_nowait()
            # except asyncio.QueueEmpty:
            #     event = None
            # else:
            #     self.process_event(event)
            #     self.event_queue.task_done()

            # обработка очереди с ускорениями
            try:
                data = self.acceleration_queue.get_nowait()
            except asyncio.QueueEmpty:
                data = None
            else:
                self.plot_acceleration.set_data(data)
                self.acceleration_queue.task_done()

            if not self.device.is_connected:
                asyncio.run_coroutine_threadsafe(self.disconnect_device(), self.qt_loop)

            time.sleep(0.001)


    async def stop_device(self):
        logger.debug("Stop device")
        # остановка потока обработки очереди
        self._running = False
        if self._work:
            self._work.join(5.0)
            self._work = None

        self.data_storage.stop()
        try:
            await self.device.stop_acquisition()
        except Exception as exc:
            info = QMessageBox.information(
                self, "Stop error",
                f"An error occurred while stoping the device\n\nInfo:\n{exc}\n\nPlease, restart application!",
                QMessageBox.StandardButton.Ok
            )
        finally:

            # activate and disable btn when stop device
            self.device_control_pane.state_connection()
            # self.pushButtonTurnOff.setEnabled(True)
            self.pushButtonDisconnect.setEnabled(True)


    async def lost_connection(self):
        """
        Action when lost connection with device.
        :return: None
        """
        logger.info("Lost device connection.")
        self._running = False
        try:
            await self.device.stop_acquisition()
        except Exception as err:
            ...

        try:
            await self.device.disconnect()
        except Exception as err:
            logger.info(f"Возникла ошибка при сбросе соединения: {err}")


        # disable button
        self.device_control_pane.state_disconnect()

        # hide disconnect and hide connect
        self.pushButtonDisconnect.hide()
        self.pushButtonConnect.show()

        # run scanner
        self.scanner.run(self.qt_loop)
        self.device_control_pane.checkBoxActivated.setEnabled(True)
        # activate combobox
        self.comboBoxDevice.setEnabled(True)

        QMessageBox.information(
            self, "Connect error",
            f"An error occurred while connect to the device.\nCheck if the device has turned off.",
            QMessageBox.StandardButton.Ok
        )


    def closeEvent(self, event):
        if self._running:
            self.device_control_pane.pushButtonStop.click()
        # stop scanner
        self.scanner.stop()

if __name__ == "__main__":
    # logging.basicConfig(
    #     level=logging.DEBUG,
    #     format="%(asctime)-15s %(name)-8s %(levelname)s: %(message)s",
    # )

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
        # window.show()
        window.showMaximized()
        loop.run_forever()

    # QtAsyncio.run(handle_sigint=True, debug=True)