from typing import Dict, List, Optional
from room import Room
from devices.light import Light
from devices.motion_sensor import MotionSensor
from devices.thermostat import Thermostat



class SmartHomeController:
    _instance = None
    

    def __init__(self):
        self._rooms: Dict[str, Room] = {}
        self._is_night = False
        self._outside_temperature = 21.0
        self._log: List[str] = []
        self._current_room = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = SmartHomeController()
        return cls._instance

    @property
    def rooms(self):
        return self._rooms

    def add_room(self, room: Room):
        self._rooms[room.name.lower()] = room

    def get_room(self, name: str) -> Optional[Room]:
        return self._rooms.get(name.lower())

    def set_is_night(self, value: bool):
        self._is_night = value

    def set_outside_temperature(self, v: float):
        self._outside_temperature = v

    def log_event(self, msg: str):
        self._log.append(msg)
        print(f"[EVENT] {msg}")

    def get_log(self):
        return list(self._log)

    # ENTER ROOM

    def enter_room(self, room_name: str):
        room = self.get_room(room_name)
        if not room:
            self.log_event(f"Attempted to enter unknown room '{room_name}'")
            return

        sensors = room.get_devices_by_type(MotionSensor)
        new_sensor = sensors[0] if sensors else None

        if self._current_room == room.name:

            # bathroom special rule even if already inside
            if room.name.lower() == "bathroom":
                for light in room.get_devices_by_type(Light):
                    if not light.is_on:
                        light.turn_on()
                    self.log_event(
                        f"Light '{light.name}' turned ON (bathroom special rule: always ON when occupied)"
                    )

            if new_sensor:
                self.log_event(
                    f"MotionSensor '{new_sensor.name}' reports PRESENCE in {room.name} (already inside)"
                )
            else:
                self.log_event(
                    f"You are already in {room.name}"
                )
            return


        prev_room_name = self._current_room
        if prev_room_name is not None:
            prev_room = self.get_room(prev_room_name)

            if prev_room is not None:
                self.log_event(f"You left {prev_room.name}")

                prev_sensors = prev_room.get_devices_by_type(MotionSensor)
                prev_sensor = prev_sensors[0] if prev_sensors else None

                if prev_sensor:
                    self.log_event(
                        f"MotionSensor '{prev_sensor.name}' reports NO PRESENCE in {prev_room.name}"
                    )
                    prev_sensor.set_presence(False)


                for light in prev_room.get_devices_by_type(Light):
                    if light.is_on:
                        light.turn_off()
                        self.log_event(
                            f"Light '{light.name}' turned OFF (no presence in {prev_room.name})"
                        )
                    else:
                        self.log_event(
                            f"Light '{light.name}' stays OFF (day mode)"
                        )

        self._current_room = room.name
        self.log_event(f"You entered {room.name}")

        if new_sensor:
            self.log_event(
                f"MotionSensor '{new_sensor.name}' reports PRESENCE in {room.name}"
            )

            new_sensor.set_presence(True)

            lights = room.get_devices_by_type(Light)
            is_bathroom = (room.name.lower() == "bathroom")

            if is_bathroom:
                for light in lights:
                    if not light.is_on:
                        light.turn_on()
                    self.log_event(
                        f"Light '{light.name}' turned ON (bathroom special rule: always ON when occupied)"
                    )

            elif self._is_night:
                for light in lights:
                    if not light.is_on:
                        light.turn_on()
                    self.log_event(
                        f"Light '{light.name}' turned ON (night mode, presence detected)"
                    )

            else:
                for light in lights:
                    self.log_event(
                        f"Light '{light.name}' remains OFF (daylight)"
                    )

        else:
            self.log_event(f"No MotionSensor available in {room.name}")



    # STATUS

    def print_status(self):
        print(f"\n--- STATUS ---")
        print(f"Night: {self._is_night}")
        print(f"Temperature: {self._outside_temperature}°C")

        for room in self._rooms.values():
            print(f"\nRoom: {room.name}")
            for d in room.get_devices():
                print("  " + d.get_status())

    # LOGS
    
    def print_logs(self):
        print("\n--- EVENT LOG ---")
        if not self._log:
            print("  (no events yet)")
        else:
            for entry in self._log:
                print("  * " + entry)
        print("-----------------\n")


    # TEMPERATURE CHANGE

    def handle_outside_temperature_change(self):
        temp = self._outside_temperature

        for room in self._rooms.values():
            thermostats = room.get_devices_by_type(Thermostat)

            for t in thermostats:

                # cold
                if temp <= 5:
                    t.set_target_temperature(23)
                    t.set_heating()

                    self.log_event(
                        f"Thermostat in {room.name} detected LOW outside temperature ({temp}°C)"
                    )
                    self.log_event(
                        f"Command sent to Heater: target set to 23°C"
                    )

                # hot
                elif temp > 20:
                    t.set_target_temperature(19)
                    t.set_cooling()

                    self.log_event(
                        f"Thermostat in {room.name} detected HIGH outside temperature ({temp}°C)"
                    )
                    self.log_event(
                        f"Command sent to Cooler: target set to 19°C"
                    )

                # fine
                else:
                    t.set_target_temperature(21)
                    t.set_idle()

                    self.log_event(
                        f"Thermostat in {room.name} detected MODERATE outside temperature ({temp}°C)"
                    )
                    self.log_event(
                        f"Command sent to Thermostat: target set to 21°C (eco mode)"
                    )


    # TIME CHANGE
    
    def update_lighting_based_on_time(self, previous_state: bool):
        room = self.get_room(self._current_room) if self._current_room else None

        if previous_state == self._is_night:
            if self._is_night:
                self.log_event("It is already NIGHT – no changes made")
            else:
                self.log_event("It is already DAY – no changes made")
            return

        if room:
            lights = room.get_devices_by_type(Light)

            if self._is_night:
                self.log_event("System switched to NIGHT mode")
                for light in lights:
                    light.turn_on()
                    self.log_event(
                        f"Light '{light.name}' turned ON in {room.name} (night mode)"
                    )
            else:
                self.log_event("System switched to DAY mode")
                for light in lights:
                    light.turn_off()
                    self.log_event(
                        f"Light '{light.name}' turned OFF in {room.name} (day mode)"
                    )



