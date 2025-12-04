from .device import Device

class MotionSensor(Device):
    def __init__(self, name: str):
        super().__init__(name)
        self._presence = False

    @property
    def presence(self):
        return self._presence

    def set_presence(self, value: bool):
        self._presence = value

    def get_status(self):
        state = "PRESENCE" if self._presence else "NO PRESENCE"
        return f"MotionSensor '{self.name}': {state}"

