import datetime
import logging
import os.path
from typing import Optional

import numpy as np
import wfdb
from pyedflib import EdfWriter


logger = logging.getLogger(__name__)

class Storage:
    def __init__(self, path_to_save: str, fs: int):
        self.ecg = np.array([])

        self.is_recording = None

        self.path_to_save = os.path.abspath(path_to_save)
        self.fs = fs

        self._format = "WFDB" # default format
        self.start_time: Optional[datetime.datetime] = None


    def set_format(self, frmt):
        """
        Change format save file.
        :param frmt: str - name of select format
        """
        logger.debug(f"Change format: {self._format} -> {frmt}")
        self._format = frmt

    def set_save_dir(self, path: str):
        """ Save record in save dir. Raise error if dir is not exists. """
        if os.path.isdir(path):
            self.path_to_save = path
        else:
            raise ValueError("Dir is not exists!")

    def get_file_name(self):
        str_st = str(self.start_time.replace(microsecond=0)).replace(":", "-")
        dur = int(self.ecg.shape[0] / 500)
        filename = f"{str_st}_dur_{dur}_sec"
        return filename

    def save(
        self,
    ):
        """ Save in select format """
        logger.debug(f"ECG buffer size: {self.ecg.shape}")

        if self.ecg.shape[0] == 0:
            return

        filename = self.get_file_name()
        write_dir = f"{self.path_to_save}\\{self._format.lower()}_{filename}"

        # create dir for saving files with selected format
        os.mkdir(path=write_dir)

        if self._format == "WFDB":
            self._to_wfdb(record_name=filename, write_dir=write_dir)

        # filename = f"{write_dir}\\{filename}.edf"
        filename = f"{write_dir}\\file.edf"
        if self._format == "EDF":
            self._to_edf(filename)

        self.ecg = np.array([])
        self.start_time = None

    def _to_wfdb(
            self,
            record_name: str, write_dir: str,

            sig_name:list[str]=["ECG"], units: list[str] = ["uV"], fs: int = 500 # default
    ):
        logger.debug("Save ecg in WFDB format.")
        wfdb.io.wrsamp(
            record_name="file",
            fs=self.fs, units=units, p_signal=self.ecg[np.newaxis].T,
            sig_name=sig_name, write_dir=write_dir, base_datetime=self.start_time
        )

    def _to_edf(
        self,
        filename:str, units: str = "uV", fs: int = 500, sig_name:str="ECG",
    ):
        logger.debug("Save ecg in EDF format.")
        writer = EdfWriter(
            n_channels=1,
            file_name=filename,
        )
        self.ecg = np.round(self.ecg, decimals=3)

        margin = 0.15
        signal_max = np.max(self.ecg)
        signal_min = np.min(self.ecg)
        physical_max = np.round(signal_max * (1 + margin) if signal_max > 0 else signal_max * (1 - margin), decimals=3)
        physical_min = np.round(signal_min * (1 - margin) if signal_min > 0 else signal_min * (1 + margin), decimals=3)

        channel_info = {
            'label': sig_name,
            'dimension': units,
            'sample_frequency': fs,
            'physical_max': physical_max,
            'physical_min': physical_min,
            'digital_max': 32767,
            'digital_min': -32768,
        }
        writer.setSignalHeader(0, channel_info)
        writer.setEquipment("inRat")
        writer.writeSamples(self.ecg[np.newaxis])
        writer.close()

    def __call__(self, ecg):
        if self.ecg.shape[0] == 0:
            self.start_time = datetime.datetime.now()
        self.ecg = np.append(self.ecg, ecg)