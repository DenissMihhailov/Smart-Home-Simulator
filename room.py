from typing import List, Optional, Type
from devices.device import Device
from devices.motion_sensor import MotionSensor



class Room:
    def __init__(self, name: str):
        self._name = name
        self._devices: List[Device] = []

    @property
    def name(self):
        return self._name

    def add_device(self, device: Device):
        self._devices.append(device)

    def get_devices(self):
        return list(self._devices)

    def get_devices_by_type(self, t: Type[Device]):
        return [d for d in self._devices if isinstance(d, t)]
