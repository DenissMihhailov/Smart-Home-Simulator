from devices.device import Device

class Thermostat(Device):
    def __init__(self, name: str):
        super().__init__(name)
        self._target_temperature = 21
        self._mode = "IDLE"

    @property
    def target_temperature(self):
        return self._target_temperature

    @property
    def mode(self):
        return self._mode  

    def set_target_temperature(self, temp: int):
        self._target_temperature = temp

    def set_heating(self):
        self._mode = "HEATING"

    def set_cooling(self):
        self._mode = "COOLING"

    def set_idle(self):
        self._mode = "IDLE"

    def get_status(self):
        return f"Thermostat '{self.name}': mode= {self._mode}, target={ self._target_temperature}°C"
