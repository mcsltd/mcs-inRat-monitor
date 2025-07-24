import logging
import numpy as np
import wfdb


logger = logging.getLogger(__name__)

class Storage:
    def __init__(self):
        self.ecg = np.array([])
        self._format = "WFDB"

    def set_format(self, frmt):
        """
        Change format save file.
        :param frmt: str - name of select format
        """
        logger.debug(f"Change format: {self._format} -> {frmt}")
        self._format = frmt

    def save(self):
        """ Save in select format """
        logger.debug(f"ECG buffer size: {self.ecg.shape}")

        if self._format == "WFDB":
            self._to_wfdb()

        if self._format == "EDF":
            self._to_edf()

        self.ecg = np.array([])

    def _to_wfdb(self,):
        logger.debug("Save ecg in WFDB format.")
        ...

    def _to_edf(self,):
        logger.debug("Save ecg in EDF format.")
        ...

    def __call__(self, ecg):
        self.ecg = np.append(self.ecg, ecg)