from PySide6.QtBluetooth import QBluetoothLocalDevice
from PySide6.QtWidgets import QApplication


def get_bluetooth_error() -> str | None:
    """ текст ошибки Bluetooth или None, если Bluetooth доступен и включён """
    local_device = QBluetoothLocalDevice()
    if not local_device.isValid():
        return "Bluetooth-адаптер не найден."
    if local_device.hostMode() == QBluetoothLocalDevice.HostMode.HostPoweredOff:
        return "Bluetooth выключен."
    return None


def check_bluetooth_status():
    error = get_bluetooth_error()
    if error is not None:
        raise ValueError(error)


if __name__ == "__main__":
    app = QApplication
    check_bluetooth_status()
    app.exec()