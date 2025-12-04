from .device import Device

class Light(Device):
    def __init__(self, name: str):
        super().__init__(name)
        self._is_on = False

    @property
    def is_on(self):
        return self._is_on

    def turn_on(self):
        self._is_on = True

    def turn_off(self):
        self._is_on = False

    def get_status(self) -> str:
        state = "ON" if self._is_on else "OFF"
        return f"Light '{self.name}': {state}"

