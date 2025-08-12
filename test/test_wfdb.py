import pyedflib
import wfdb
from wfdb.io.convert.edf import read_edf, rdedfann
import numpy as np


def read_and_plot_wfdb(record_name):
    record = wfdb.rdrecord(record_name)

    wfdb.plot_items(
        signal=record.p_signal,
        fs=record.fs, sig_units=record.units,
        time_units='seconds',
        figsize=(10,4), ecg_grids='all'
    )


def covert_edf_to_wfdb(record_name):
    record = read_edf(record_name=record_name)
    _ = 1

def read_file_edf(record_name="file.edf"):
    f = pyedflib.EdfReader(record_name)
    n = f.signals_in_file
    signal_labels = f.getSignalLabels()
    sigbufs = np.zeros((n, f.getNSamples()[0]))
    for i in np.arange(n):
        sigbufs[i, :] = f.readSignal(i)
    _ = 1


if __name__ == "__main__":
    # read_file_edf(record_name="file.edf")
    read_and_plot_wfdb(record_name="2025-08-12_11h53m08s_dur_11_sec")