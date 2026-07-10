from pyedflib.edfreader import EdfReader

data_1068 = [
    ("inRat-1-1068_ecg_500hz_acc_1min", "./data/inRat-1-1068_exg_acc/ecg_500hz_acc_1_min/acc.edf", "./data/inRat-1-1068_exg_acc/ecg_500hz_acc_1_min/ecg.edf"),
    ("inRat-1-1068_1000hz_acc_1min", "./data/inRat-1-1068_exg_acc/ecg_1000hz_acc_1_min/acc.edf", "./data/inRat-1-1068_exg_acc/ecg_1000hz_acc_1_min/ecg.edf"),
    ("inRat-1-1068_ecg_2000hz_1min", "./data/inRat-1-1068_exg_acc/ecg_2000hz_acc_1_min/acc.edf", "./data/inRat-1-1068_exg_acc/ecg_2000hz_acc_1_min/ecg.edf"),
    ("inRat-1-1068_eeg_500hz_acc_1min", "./data/inRat-1-1068_exg_acc/eeg_500hz_acc_1_min/acc.edf", "./data/inRat-1-1068_exg_acc/eeg_500hz_acc_1_min/eeg.edf"),
]

data_1069 = [
    ("inRat-1-1069_ecg_500hz_acc_1min", "./data/inRat-1-1069_exg_acc/ecg_500hz_acc_1_min/acc.edf", "./data/inRat-1-1069_exg_acc/ecg_500hz_acc_1_min/ecg.edf"),
    ("inRat-1-1069_1000hz_acc_1min", "./data/inRat-1-1069_exg_acc/ecg_1000hz_acc_1_min/acc.edf", "./data/inRat-1-1069_exg_acc/ecg_1000hz_acc_1_min/ecg.edf"),
    ("inRat-1-1069_ecg_2000hz_1min", "./data/inRat-1-1069_exg_acc/ecg_2000hz_acc_1_min/acc.edf", "./data/inRat-1-1069_exg_acc/ecg_2000hz_acc_1_min/ecg.edf"),
    ("inRat-1-1069_eeg_500hz_acc_1min", "./data/inRat-1-1069_exg_acc/eeg_500hz_acc_1_min/acc.edf", "./data/inRat-1-1069_exg_acc/eeg_500hz_acc_1_min/eeg.edf"),
]

data_1070 = [
    ("inRat-1-1070_ecg_500hz_acc_1min", "./data/inRat-1-1070_exg_acc/ecg_500hz_acc_1_min/acc.edf", "./data/inRat-1-1070_exg_acc/ecg_500hz_acc_1_min/ecg.edf"),
    ("inRat-1-1070_1000hz_acc_1min", "./data/inRat-1-1070_exg_acc/ecg_1000hz_acc_1_min/acc.edf", "./data/inRat-1-1070_exg_acc/ecg_1000hz_acc_1_min/ecg.edf"),
    ("inRat-1-1070_ecg_2000hz_1min", "./data/inRat-1-1070_exg_acc/ecg_2000hz_acc_1_min/acc.edf", "./data/inRat-1-1070_exg_acc/ecg_2000hz_acc_1_min/ecg.edf"),
    ("inRat-1-1070_eeg_500hz_acc_1min", "./data/inRat-1-1070_exg_acc/eeg_500hz_acc_1_min/acc.edf", "./data/inRat-1-1070_exg_acc/eeg_500hz_acc_1_min/eeg.edf"),
]

data_1071 = [
    ("inRat-1-1071_ecg_500hz_acc_1min", "./data/inRat-1-1071_exg_acc/ecg_500hz_acc_1_min/acc.edf", "./data/inRat-1-1071_exg_acc/ecg_500hz_acc_1_min/ecg.edf"),
    ("inRat-1-1071_1000hz_acc_1min", "./data/inRat-1-1071_exg_acc/ecg_1000hz_acc_1_min/acc.edf", "./data/inRat-1-1071_exg_acc/ecg_1000hz_acc_1_min/ecg.edf"),
    ("inRat-1-1071_ecg_2000hz_1min", "./data/inRat-1-1071_exg_acc/ecg_2000hz_acc_1_min/acc.edf", "./data/inRat-1-1071_exg_acc/ecg_2000hz_acc_1_min/ecg.edf"),
    ("inRat-1-1071_eeg_500hz_acc_1min", "./data/inRat-1-1071_exg_acc/eeg_500hz_acc_1_min/acc.edf", "./data/inRat-1-1071_exg_acc/eeg_500hz_acc_1_min/eeg.edf"),
]


def get_true_sample_rate_acc(name: str, file_acc: str, file_exg: str):
    acc = EdfReader(file_acc)
    counters_acc = len(acc.readSignal(0))

    exg = EdfReader(file_exg)
    sec_duration = exg.getFileDuration()

    sample_rate = counters_acc / sec_duration
    print(f"{name}; sample rate: {sample_rate}")


if __name__ == "__main__":
    for name, acc, exg in data_1068:
        get_true_sample_rate_acc(name=name, file_acc=acc, file_exg=exg)
    print()

    for name, acc, exg in data_1069:
        get_true_sample_rate_acc(name=name, file_acc=acc, file_exg=exg)
    print()

    for name, acc, exg in data_1070:
        get_true_sample_rate_acc(name=name, file_acc=acc, file_exg=exg)
    print()

    for name, acc, exg in data_1071:
        get_true_sample_rate_acc(name=name, file_acc=acc, file_exg=exg)
    print()