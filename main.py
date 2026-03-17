import asyncio
import datetime
import logging
import os
import time
from threading import Thread
from typing import Optional

import pyqtgraph as pg

import numpy as np
from PySide6 import QtAsyncio, QtCore
from PySide6.QtCore import QTimer, Signal
from PySide6.QtGui import QIcon, QFont
from PySide6.QtWidgets import QMainWindow, QApplication, QMessageBox, QComboBox, QFileDialog
from bleak import BLEDevice

from device import RatSens
from config import DATA_PATH
from constants import HZ, Pkt
from display import PlotWidgetTemperature
from record_viewer import RecordViewer
from scanner import BLEScannerWorker
from structure import EventData
from utils.check_bluetooth import check_bluetooth_status
from storage import Storage
from ui.main_window import Ui_MainWindow
from widget import WaitingDialog

logger = logging.getLogger(__name__)


RED = pg.mkPen(color=(255, 0, 0), width=1.5)


class MainWindow(QMainWindow, Ui_MainWindow):

    signal_connect = Signal()

    def __init__(self, qt_loop: QtAsyncio.QAsyncioEventLoop, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.setWindowTitle("InRat monitor")
        self.setWindowIcon(QIcon("ui/iconMCS.ico"))

        # hide
        self.pushButtonDisconnect.hide()
        self.qt_loop = qt_loop

        # build queue
        self.ecg_queue = asyncio.Queue()
        self.event_queue = asyncio.Queue()

        # data
        self.max_timebase = 60
        self.timebase = 30
        self.dt = 1 / HZ
        self.ecg_buffer = np.zeros(int(self.max_timebase * HZ))
        self.time_buffer = np.arange(0, self.max_timebase, self.dt)
        # переменные для управления отображением
        self.buffer_filled = False  # флаг заполнения буфера
        self.current_position = 0   # текущая позиция для заполнения буфера

        # main classes
        self.device: Optional[RatSens] = None
        self.storage = Storage(path_to_save=DATA_PATH, fs=HZ)
        self.scanner = BLEScannerWorker()

        # легенда
        self.legend = self.plotWidget.addLegend()
        self.legend.setLabelTextColor(0,0,0)

        # setup plot
        self.plot_ecg = self.plotWidget.plot(pen=RED)
        self.plotWidget.setDownsampling(auto=True, mode='peak', ds=50)

        self.widget_temp = PlotWidgetTemperature()
        self.plotWidget.setTitle("ECG", color="k", size="12pt")

        self.widget_temp.setFixedHeight(250)
        self.verticalLayoutDisplay.addWidget(self.widget_temp)

        # scatter plot for activity, freefall, orientation
        self.scatter_activity = pg.ScatterPlotItem(name="Activity", symbol='t', brush=pg.mkBrush(0, 255, 0, 180),  size=10,)
        self.plotWidget.addItem(self.scatter_activity)
        self.scatter_orientation = pg.ScatterPlotItem(name="Orientation", symbol="o", brush=pg.mkBrush(0, 0, 255, 180), size=10,)
        self.plotWidget.addItem(self.scatter_orientation)
        self.scatter_freefall = pg.ScatterPlotItem(name="Freefall", symbol='s', brush=pg.mkBrush(255, 0, 0, 180), size=10,)
        self.plotWidget.addItem(self.scatter_freefall)
        self.marker_temp = []

        font = QFont()
        font.setPointSize(12)

        self.plotWidget.setLabel("left", units="V", pen=pg.mkPen(color='k'), font=font)
        self.plotWidget.getAxis("left").label.setFont(font)
        self.plotWidget.getAxis("left").setPen(pg.mkPen(color='k'))
        self.plotWidget.getAxis("left").setTextPen(pg.mkPen(color='k'))
        self.plotWidget.getAxis("left").setTickFont(font)

        # "Time (sec)",
        self.plotWidget.setLabel("bottom", "Time", units="s",  pen=pg.mkPen(color='k'), font=font)
        self.plotWidget.getAxis("bottom").label.setFont(font)
        self.plotWidget.getAxis("bottom").setPen(pg.mkPen(color='k'))
        self.plotWidget.getAxis("bottom").setTextPen(pg.mkPen(color='k'))
        self.plotWidget.getAxis("bottom").setTickFont(font)

        self.plotWidget.addLegend()
        self.plotWidget.setBackground("w")

        # create scanner and run it
        self.scanner.run(self.qt_loop)
        self.scanner.signal_found.connect(self.set_combobox_items)
        self.pushButtonConnect.setEnabled(False)

        self._work: None | Thread = None
        self._running = False

        # setup combobox
        self.comboBoxDevice.setDuplicatesEnabled(False)
        self.comboBoxDevice.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)

        for v in [(1, "1 s"), (5, "5 s"), (10, "10 s"), (30, "30 s"), (60, "60 s")]:
            self.comboBoxTimebase.addItem(v[1], userData=v[0])
        self.comboBoxTimebase.setCurrentIndex(3)
        self.comboBoxTimebase.currentTextChanged.connect(self.set_timebase)

        # setup checkbox
        self.checkBoxActivated.setEnabled(False)

        # connection
        self.pushButtonConnect.clicked.connect(lambda: asyncio.ensure_future(self.connect_device()))
        self.pushButtonStart.clicked.connect(lambda: asyncio.ensure_future(self.start_device()))
        self.pushButtonStop.clicked.connect(lambda: asyncio.ensure_future(self.stop_device()))
        self.pushButtonRecording.clicked.connect(self.change_recording)
        self.pushButtonSelectDirSave.clicked.connect(self._set_storage)
        self.pushButtonDisconnect.clicked.connect(lambda: asyncio.ensure_future(self.disconnect_device()))
        # self.pushButtonShowRecords.clicked.connect(self.open_savedir)
        self.checkBoxActivated.clicked.connect(lambda: asyncio.ensure_future(self.on_activated_clicked()))
        self.pushButtonViewRecording.clicked.connect(self.on_view_recording_clicked)

        self.lineEditSave.setText(self.storage.path_to_save) # set default folder
        self.comboBoxFormat.currentTextChanged.connect(self.storage.set_format)

        # Буфер для накопления данных
        self.pending_update = False

        # таймер для обновления графика
        self.update_timer = QtCore.QTimer()
        self.update_timer.timeout.connect(self._delayed_update_plot)
        self.update_timer.start(16)  # 60 fps


    def set_timebase(self):
        self.timebase = self.comboBoxTimebase.currentData()
        if not self._running:
            self.plotWidget.setXRange(0, self.timebase)

    def _set_storage(self):
        path_to_save = QFileDialog.getExistingDirectory(
            self,
            "Select folder",
            self.storage.path_to_save,
            QFileDialog.Option.ShowDirsOnly | QFileDialog.Option.DontResolveSymlinks
        )
        self.storage.set_save_dir(path_to_save)
        self.lineEditSave.setText(path_to_save)

    def on_view_recording_clicked(self):
        """ обработка нажатия кнопки просмотра записей """
        path_to_record = QFileDialog.getExistingDirectory(
            self,
            "Select folder",
            self.storage.path_to_save,
            QFileDialog.Option.ShowDirsOnly | QFileDialog.Option.DontResolveSymlinks
        )

        if path_to_record:
            viewer = RecordViewer()
            if viewer.load_record(path_to_record):
                viewer.exec()

    def set_combobox_items(self, devices: set[BLEDevice]):
        for device in devices:
            if self.comboBoxDevice.findText(device.name) == -1:
                self.comboBoxDevice.addItem(device.name, userData=device)
        if self.comboBoxDevice.count() != 0:
            self.pushButtonConnect.setEnabled(True)

    def change_recording(self):
        """
        Change state recording.
        """
        if self.storage.is_recording:
            self.storage.is_recording = False
            self.pushButtonRecording.setText("Start Recording")

            # activate elements for setup storage when press "Stop Recording"
            self.comboBoxFormat.setEnabled(True)
            # self.pushButtonSelectDirSave.setEnabled(True)

            logger.debug("Select stop recording ECG.")

            self.labelRTvalue.setText("[00:00:00]")
            if self.device.is_running:
                self.storage.save()

                if not self.buffer_filled:
                    pos = self.time_buffer[self.current_position]
                else:
                    pos = self.time_buffer[-1]
                self.add_marker(pos=pos, text="Stop recording")

        elif self.storage.is_recording is None or not self.storage.is_recording:
            self.storage.is_recording = True
            self.pushButtonRecording.setText("Stop Recording")

            # deactivate elements when press "Start Recording"
            # self.pushButtonSelectDirSave.setEnabled(False)
            self.comboBoxFormat.setEnabled(False)

            logger.debug("Select start recording ECG.")
            if not self.buffer_filled:
                pos = self.time_buffer[self.current_position]
            else:
                pos = self.time_buffer[-1]
            self.add_marker(pos=pos, text="Start recording")

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
        # self.comboBoxDevice.clear()
        # disable combobox and button connect
        self.comboBoxDevice.setDisabled(True)
        self.pushButtonConnect.setDisabled(True)

        # reconnect with new device or old
        if self.device is not None and not self.device.is_connected:
            self.device = None
            self.reset()

        try:
            self.device = RatSens(device)

            attempt_connection = 1
            while not self.device.is_connected and attempt_connection <= 5:
                logger.debug(f"Устройство найдено! Производится попытка подключиться. Номер попытки: {attempt_connection}")
                try:
                    await self.device.connect()
                except Exception as exc:
                    ...
                attempt_connection += 1

            # add in storage device name (for write additional info in edf)
            self.storage.set_device_name(self.device.name)
            self.checkBoxActivated.setEnabled(True)

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
                self.checkBoxActivated.setEnabled(True)

                # проверка на активировано ли устройство
                _ = await self.device.get_status()
                if self.device.is_activated:
                    self.checkBoxActivated.setChecked(True)

                # enable settings for storage
                self.comboBoxFormat.setEnabled(True)
                # enable button for start device
                self.pushButtonStart.setEnabled(True)

                self.pushButtonDisconnect.show()
                self.pushButtonConnect.hide()
        finally:
            dlg.close()

    async def on_activated_clicked(self):
        if self.device.is_activated:
            res, msg = await self.device.deactivate()
            if res:
                logger.info("Устройство деактивировано")
                self.checkBoxActivated.setChecked(False)
                return
            QMessageBox.warning(
                self, "Device deactivation error!",
                f"Couldn't deactivate the device.\n{msg}",
                QMessageBox.StandardButton.Ok
            )
        else:
            res, msg = await self.device.activate()
            if res:
                logger.info("Устройство активировано")
                self.checkBoxActivated.setChecked(True)
                return
            QMessageBox.warning(
                self, "Device activation error!",
                f"Couldn't activate the device.\n{msg}",
                QMessageBox.StandardButton.Ok
            )

    async def disconnect_device(self):
        if self.device.is_connected:
            await self.device.close()
        else:
            await self.lost_connection()

        self.scanner.run(self.qt_loop)
        self.reset()

        # disable
        self.pushButtonStart.setEnabled(False)
        self.comboBoxFormat.setEnabled(False)

        # reset checkbox
        self.checkBoxActivated.setChecked(False)
        self.checkBoxActivated.setEnabled(False)

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

        self.reset() # cбросить графики

        if not self.device.is_connected:
            info = QMessageBox.information(
                self, "Lost device connection",
                f"Lost connection with device {self.device.name}",
                buttons=QMessageBox.StandardButton.Ok
            )
            # reset all
            await self.disconnect_device()
            return

        res = await self.device.start_acquisition(ecg_queue=self.ecg_queue, event_queue=self.event_queue)
        if res:

            # disable
            # self.pushButtonConnect.setEnabled(False)
            self.pushButtonDisconnect.setEnabled(False)
            self.comboBoxDevice.setEnabled(False)
            self.pushButtonStart.setEnabled(False)
            # self.pushButtonTurnOff.setEnabled(False)

            # enable
            self.pushButtonRecording.setEnabled(True)
            self.pushButtonStop.setEnabled(True)

            # when draw signal in online - disable mouse
            self.plotWidget.setMouseEnabled(x=False, y=False)

            self._running = True
            self._work = Thread(target=self._worker_thread)
            self._work.start()

        else:
            # ToDo: добавить действия на случай если не получилось запустить устройство
            ...

    def _worker_thread(self):
        """ поток обработки очередей """
        while self._running:
            # вывод сигналов
            try:
                ecg = self.ecg_queue.get_nowait()
            except asyncio.QueueEmpty:
                ecg = None
            else:
                self.set_data(ecg)
                self.ecg_queue.task_done()

            # обработка событий
            try:
                event = self.event_queue.get_nowait()
            except asyncio.QueueEmpty:
                event = None
            else:
                self.process_event(event)
                self.event_queue.task_done()

            if not self.device.is_connected:
                asyncio.run_coroutine_threadsafe(self.disconnect_device(), self.qt_loop)
            time.sleep(0.001)

    def process_event(self, event: EventData):
        """ обработка событий """
        event_type = event.type
        x = event.counter * self.dt

        if event_type == "Temp":
            try:
                self.widget_temp.set_data(time_sec=x, temperature=round(event.data / 1000, 1))
            except Exception as err:
                logger.debug(f"Ошибка установки в буфер данных: {err}")

            if self.storage.is_recording:
                self.storage.process_temperature(event)
        else:
            # определение минимального значения для вывода события
            if self.buffer_filled:
                y = min(self.ecg_buffer[-self.timebase * HZ:]) * 1.05
            else:
                idx = self.current_position - self.timebase * HZ
                if idx < 0:
                    idx = 0
                y = min(self.ecg_buffer[idx:self.current_position]) * 1.05

            if event.type == "Activity":
                if self.storage.is_recording:
                    self.storage.process_activity(event)
                try:
                    self.scatter_activity.addPoints([{'pos': (x, y)}])
                except Exception as err:
                    logger.debug(f"Возникла ошибка при добавлении события 'Activity': {err}")

            elif event.type == "Freefall":
                if self.storage.is_recording:
                    self.storage.process_activity(event)
                try:
                    self.scatter_freefall.addPoints([{'pos': (x, y)}])
                except Exception as err:
                    logger.debug(f"Возникла ошибка при добавлении события 'Freefall': {err}")

            elif event.type == "Orientation":
                if self.storage.is_recording:
                    self.storage.process_activity(event)
                try:
                    self.scatter_orientation.addPoints([{'pos': (x, y)}])
                except Exception as err:
                    logger.debug(f"Возникла ошибка при добавлении события 'Orientation': {err}")

    def set_data(self, ecg: dict):
        """ добавление данных сигнала в буфер """
        signal, counter = ecg["ecg"], ecg["counter"]
        if not self.buffer_filled:
            # вставка данных в незаполненный буфер
            if self.current_position + Pkt.SamplesCountECG < len(self.ecg_buffer):
                self.ecg_buffer[self.current_position:self.current_position+Pkt.SamplesCountECG] = signal
                self.current_position += Pkt.SamplesCountECG
            else:
                offset = len(self.ecg_buffer) - self.current_position
                self.ecg_buffer[self.current_position:] = signal[:offset]
                signal = signal[offset:]
                self.buffer_filled = True

        # вставка данных в заполненный буфер
        if self.buffer_filled:
            self.ecg_buffer = np.roll(self.ecg_buffer, -len(signal))
            self.ecg_buffer[-len(signal):] = signal
            self.time_buffer += len(signal) * self.dt

        # сохранение данных
        if self.storage.is_recording:
            self.storage(signal)
            str_time = str(datetime.datetime.now() - self.storage.start_time).split(".")[0]
            str_time = "0" + str_time if len(str_time) != 8 else str_time
            self.labelRTvalue.setText(f"[{str_time}]")

        self.pending_update = True

    def _delayed_update_plot(self):
        """Обновление графика по таймеру"""
        if not self.pending_update:
            return

        if not self.buffer_filled:
            end_idx = self.current_position
            start_idx = 0

            if end_idx > self.timebase * HZ:
                start_idx = end_idx - int(self.timebase * HZ)
        else:
            end_idx = len(self.ecg_buffer)
            start_idx = end_idx - int(self.timebase * HZ)
        visible_time = self.time_buffer[start_idx:end_idx]
        visible_ecg = self.ecg_buffer[start_idx:end_idx]

        # установка данных из буфера на дисплей
        self.plot_ecg.setData(visible_time, visible_ecg)

        # отображение по оси времени
        if not self.buffer_filled and end_idx <= self.timebase * HZ:
            self.plotWidget.setXRange(0, self.timebase, padding=0)
        else:
            current_time = visible_time[-1] if len(visible_time) > 0 else 0
            self.plotWidget.setXRange(current_time - self.timebase, current_time, padding=0)

        # отображение по оси напряжения
        if len(visible_ecg) > 0:
            data_min = visible_ecg.min()
            data_max = visible_ecg.max()
            if data_max > data_min:
                padding = (data_max - data_min) * 0.05
                self.plotWidget.setYRange(data_min - padding, data_max + padding)

        self.plotWidget.replot()
        self.pending_update = False

    async def stop_device(self):
        logger.debug("Stop device")
        # остановка потока обработки очереди
        self._running = False
        if self._work:
            self._work.join(5.0)
            self._work = None

        try:
            await self.device.stop()
        except Exception as exc:
            info = QMessageBox.information(
                self, "Stop error",
                f"An error occurred while stoping the device\n\nInfo:\n{exc}\n\nPlease, restart application!",
                QMessageBox.StandardButton.Ok
            )
        finally:

            if self.storage.is_recording:
                self.storage.save()

                if not self.buffer_filled:
                    pos = self.time_buffer[self.current_position]
                else:
                    pos = self.time_buffer[-1]
                self.add_marker(pos=pos, text="Stop recording")
                self.change_recording()

            # activate and disable btn when stop device
            self.pushButtonStop.setEnabled(False)
            self.pushButtonStart.setEnabled(True)
            # self.pushButtonTurnOff.setEnabled(True)
            self.pushButtonRecording.setEnabled(False)
            self.pushButtonDisconnect.setEnabled(True)
            # when stop device - activate mouse
            # self.plotWidget.setMouseEnabled(x=True, y=True)

    async def lost_connection(self):
        """
        Action when lost connection with device.
        :return: None
        """
        logger.info("Lost device connection.")
        self._running = False
        try:
            await self.device.stop()
        except Exception as err:
            ...

        try:
            await self.device.disconnect()
        except Exception as err:
            logger.info(f"Возникла ошибка при сбросе соединения: {err}")

        # save data in storage
        if self.storage.is_recording:
            self.storage.save()
            if not self.buffer_filled:
                pos = self.time_buffer[self.current_position]
            else:
                pos = self.time_buffer[-1]
            self.add_marker(pos=pos, text="Stop recording")
            self.change_recording()

        # disable button
        self.pushButtonStop.setEnabled(False)
        self.pushButtonStart.setEnabled(False)
        self.pushButtonRecording.setEnabled(False)
        # self.pushButtonSelectDirSave.setEnabled(False)
        self.comboBoxFormat.setEnabled(False)

        # hide disconnet and hide connect
        self.pushButtonDisconnect.hide()
        self.pushButtonConnect.show()

        # when lost connection - activate mouse
        # self.plotWidget.setMouseEnabled(x=True, y=True)

        # run scanner
        self.scanner.run(self.qt_loop)
        self.checkBoxActivated.setEnabled(True)
        # activate combobox
        self.comboBoxDevice.setEnabled(True)

        QMessageBox.information(
            self, "Connect error",
            f"An error occurred while connect to the device.\nCheck if the device has turned off.",
            QMessageBox.StandardButton.Ok
        )


    def reset(self) -> None:
        """ reset data """
        self.plotWidget.clear()
        # удаление значений температуры
        for marker in self.marker_temp:
            self.plotWidget.removeItem(marker)
        self.marker_temp = []

        self.widget_temp.reset()
        self.reset_event()
        self.reset_signal()

    def reset_signal(self):
        self.plotWidget.removeItem(self.plot_ecg)
        self.plot_ecg = self.plotWidget.plot(pen=RED)

        # data
        self.max_timebase = 60
        self.timebase = 30
        self.dt = 1 / HZ
        self.ecg_buffer = np.zeros(int(self.max_timebase * HZ))
        self.time_buffer = np.arange(0, self.max_timebase, self.dt)
        self.buffer_filled = False  # флаг заполнения буфера
        self.current_position = 0  # текущая позиция для заполнения буфера

    def reset_event(self):
        for item in [self.scatter_activity, self.scatter_orientation, self.scatter_freefall]:
            self.plotWidget.removeItem(item)

        # scatter plot for activity, freefall, orientation
        self.scatter_activity = pg.ScatterPlotItem(name="Activity", symbol='t', brush=pg.mkBrush(0, 255, 0, 180),
                                                   size=10, )
        self.plotWidget.addItem(self.scatter_activity)
        self.scatter_orientation = pg.ScatterPlotItem(name="Orientation", symbol="o", brush=pg.mkBrush(0, 0, 255, 180),
                                                      size=10, )
        self.plotWidget.addItem(self.scatter_orientation)
        self.scatter_freefall = pg.ScatterPlotItem(name="Freefall", symbol='s', brush=pg.mkBrush(255, 0, 0, 180),
                                                   size=10, )
        self.plotWidget.addItem(self.scatter_freefall)
        self.marker_temp = []

    def add_marker(self, pos, text:str="event"):
        """ Add vertical line and text on the plot."""
        line = pg.InfiniteLine(
            pos=pos,
            angle=90,
            pen=pg.mkPen('gray', width=1, style=QtCore.Qt.PenStyle.DashLine),
            movable=False,
            label=text,
            labelOpts={'color': 'k', 'position': 0.1}
        )
        self.plotWidget.addItem(line)
        self.marker_temp.append(line)

    def closeEvent(self, event):
        if self._running:
            self.pushButtonStop.click()
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