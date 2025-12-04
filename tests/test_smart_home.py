import unittest
from controller import SmartHomeController
from room import Room
from devices.light import Light
from devices.motion_sensor import MotionSensor
from devices.thermostat import Thermostat


class TestSmartHome(unittest.TestCase):

    def setUp(self):
        SmartHomeController._instance = None
        self.controller = SmartHomeController.get_instance()

        self.kitchen = Room("Kitchen")
        self.bathroom = Room("Bathroom")
        self.bedroom = Room("Bedroom")

        # Kitchen devices
        self.kitchen_light = Light("Kitchen Light")
        self.kitchen_sensor = MotionSensor("Kitchen Sensor")
        self.kitchen_thermo = Thermostat("Kitchen Thermostat")
        self.kitchen.add_device(self.kitchen_light)
        self.kitchen.add_device(self.kitchen_thermo)
        self.kitchen.add_device(self.kitchen_sensor)

        # Bathroom devices
        self.bathroom_light = Light("Bathroom Light")
        self.bathroom_sensor = MotionSensor("Bathroom Sensor")
        self.bathroom.add_device(self.bathroom_light)
        self.bathroom.add_device(self.bathroom_sensor)

        # Bedroom devices
        self.bedroom_light = Light("Bedroom Light")
        self.bedroom_sensor = MotionSensor("Bedroom Sensor")
        self.bedroom.add_device(self.bedroom_light)
        self.bedroom.add_device(self.bedroom_sensor)

        # Register rooms
        self.controller.add_room(self.kitchen)
        self.controller.add_room(self.bathroom)
        self.controller.add_room(self.bedroom)

    def test_daytime_enter_room(self):
        """Entering a room during daytime does not turn the light on."""

        self.controller.set_is_night(False)
        self.controller.enter_room("Kitchen")

        self.assertFalse(self.kitchen_light.is_on)
        self.assertTrue(self.kitchen_sensor.presence)

    def test_night_enter_room_turns_light_on(self):
        """Entering a room at night turns the light on."""

        self.controller.set_is_night(True)
        self.controller.enter_room("Bedroom")

        self.assertTrue(self.bedroom_light.is_on)
        self.assertTrue(self.bedroom_sensor.presence)

    def test_bathroom_always_turns_light_on(self):
        """Bathroom always turns its light on regardless of time of day."""

        self.controller.set_is_night(False)
        self.controller.enter_room("Bathroom")
        self.assertTrue(self.bathroom_light.is_on)

        self.bathroom_light.turn_off()
        self.controller.set_is_night(True)
        self.controller.enter_room("Bathroom")
        self.assertTrue(self.bathroom_light.is_on)


if __name__ == "__main__":
    unittest.main()
