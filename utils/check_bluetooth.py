from PySide6.QtBluetooth import QBluetoothLocalDevice
from PySide6.QtWidgets import QApplication


def check_bluetooth_status():
    local_device = QBluetoothLocalDevice()
    if local_device.isValid():
        if local_device.hostMode() == QBluetoothLocalDevice.HostMode.HostPoweredOff:
            raise ValueError("Bluetooth is turned off.")
    else:
        raise ValueError("Bluetooth not available.")


if __name__ == "__main__":
    app = QApplication
    check_bluetooth_status()
    app.exec()