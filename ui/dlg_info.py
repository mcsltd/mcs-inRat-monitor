from PySide6.QtWidgets import QDialog

from device.models import DeviceProperty, DeviceUsage
from resources.dlg_info import Ui_DlgDeviceInfo


class DlgDeviceInfo(QDialog, Ui_DlgDeviceInfo):
    """ Диалоговое окно с выводом информации об устройстве """
    def __init__(
            self,
            device_property: DeviceProperty | None = None,
            working_time: DeviceUsage | None = None,
            *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.setupUi(self)

        self._property = device_property
        self._times = working_time

        self._set_device_info()
        self._set_working_times()

    def _set_device_info(self):
        """ Установка информации об устройстве """
        if self._property is not None:
            self.labelNameValue.setText(str(self._property.name))
            self.labelFirmValue.setText(str(self._property.firmware))
            self.labelHardValue.setText(str(self._property.hardware))
            self.labelModelValue.setText(str(self._property.model))
            self.labelSnValue.setText(str(self._property.serial))

    def _set_working_times(self):
        if self._times is not None:
            self.labelPowerOnCntValue.setText(f"{str(self._times.power_on_count)}")
            self.labelAdvValue.setText(f"{str(self._times.advertising_sec)} секунд")
            self.labelConnValue.setText(f"{str(self._times.connection_sec)} секунд")
            self.labelDataValue.setText(f"{str(self._times.data_sec)} секунд")
