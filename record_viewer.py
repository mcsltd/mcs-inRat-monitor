import csv
import logging
import os.path

import numpy as np
import pyedflib
import wfdb
from PySide6.QtGui import QIcon

from PySide6.QtWidgets import QDialog, QMessageBox

from display import PlotWidgetEcg, PlotWidgetTemperature
from ui.dlg_record_viewer import Ui_DlgRecordViewer


logger = logging.getLogger(__name__)

class RecordViewer(QDialog, Ui_DlgRecordViewer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.setWindowIcon(QIcon("ui/iconMCS.ico"))
        self.setWindowTitle("Record Viewer")

        self.widget_ecg = PlotWidgetEcg()
        self.widget_temperature = PlotWidgetTemperature()

        self.verticalLayoutDisplay.addWidget(self.widget_ecg)
        # self.verticalLayoutDisplay.addWidget(self.widget_temperature)


    def load_record(self, path_to_record):
        logger.debug(f"загрузка записи из {path_to_record}")

        if not os.path.exists(path_to_record):
            return

        temp_csv = None
        activity_csv = None
        ecg_edf = None
        ecg_wfdb = None

        for file in os.listdir(path_to_record):
            if "activity" in file and file.endswith(".csv"):
                activity_csv = f"{path_to_record}\\{file}"
                logger.info(f"найден файл с записями активности: {activity_csv=}")
            if "temperature" in file and file.endswith(".csv"):
                temp_csv = f"{path_to_record}\\{file}"
                logger.info(f"найден файл с записями температуры: {temp_csv=}")
            if file.endswith(".dat") or file.endswith(".hea"):
                ecg_wfdb = f"{path_to_record}\\{file}"
                logger.info(f"найден файл с записями сигналов в формате wfdb: {ecg_wfdb=}")
            if file.endswith(".edf"):
                ecg_edf = f"{path_to_record}\\{file}"
                logger.info(f"найден файл с записями сигналов в формате wfdb: {ecg_edf=}")

        if ecg_edf and not ecg_wfdb:
            try:
                self.load_edf(ecg_edf)
            except Exception as err:
                logger.error(f"возникла ошибка чтения edf файла: {err=}")

        if ecg_wfdb and not ecg_edf:
            try:
                self.load_wfdb(ecg_wfdb)
            except Exception as err:
                logger.error(f"возникла ошибка чтения wfdb файла: {err=}")

        if temp_csv:
            try:
                self.load_temperature(temp_csv)
            except Exception as err:
                logger.error(f"возникла ошибка чтения csv файла: {err=}")

        if activity_csv:
            try:
                self.load_activity(activity_csv)
            except Exception as err:
                logger.error(f"возникла ошибка чтения csv файла: {err=}")

        if not activity_csv and not temp_csv and not ecg_wfdb and not ecg_edf:
            QMessageBox.warning(
                self,
                "Warning! Don't find recording",
                "Сouldn't find records. Please check recordings in the selected folder.",
                buttons=QMessageBox.StandardButton.Ok
            )
            return False
        return True

    def load_temperature(self, file_csv: str):
        t, temp = [], []
        with open(file_csv, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file, fieldnames=["time_sec", "temp_celsius"])
            next(reader)
            for row in reader:
                t.append(float(row["time_sec"]))
                temp.append(float(row["temp_celsius"]))
        self.widget_temperature.load_data(t, temp)

    def load_activity(self, file_csv):
        ev_activity = []
        with open(file_csv, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file, fieldnames=["time_sec", "description"])
            next(reader)
            for row in reader:
                ev_activity.append({"time": float(row["time_sec"]), "event": row["description"]})
        self.widget_ecg.load_event(ev_activity)

    def load_edf(self, file_edf):
        """Чтение данных из EDF файла"""
        with pyedflib.EdfReader(file_edf) as file:
            duration = file.getFileDuration()
            sample_rate = int(file.getSampleFrequency(0))
            signal = file.readSignal(0)
            self.widget_ecg.load_ecg(ecg=signal, sec_duration=duration, sample_rate=sample_rate)

    def load_wfdb(self, file_wfdb):
        """ чтение данных из WFDB файла """
        base_path = file_wfdb
        if file_wfdb.endswith('.dat') or file_wfdb.endswith('.hea'):
            base_path = file_wfdb[:-4]
        record = wfdb.rdrecord(base_path)

        sample_rate = record.fs
        duration = record.sig_len / record.fs
        signal = record.p_signal.T if record.p_signal is not None else record.d_signal.T
        ecg = np.squeeze(signal)

        self.widget_ecg.load_ecg(ecg=ecg, sec_duration=duration, sample_rate=sample_rate)