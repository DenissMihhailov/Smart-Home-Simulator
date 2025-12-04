from controller import SmartHomeController
from room import Room
from devices.light import Light
from devices.thermostat import Thermostat
from devices.motion_sensor import MotionSensor

import time

# python3 -m unittest discover

def print_interface():
    red = "\033[31m●\033[0m"
    yellow = "\033[33m●\033[0m"
    green = "\033[32m●\033[0m"

    print("╔══════════════════════════════════════════════════════════╗")
    print("║ " + red + " " + yellow + " " + green + " " + "               SMART HOME SIMULATOR" + "                ║")
    print("╠══════════════════════════════════════════════════════════╣")
    print("║                                                          ║")
    print("║      Commands:                                           ║")
    print("║        status            – show home status              ║")
    print("║        enter <room>      – simulate entering             ║")
    print("║        time <day/night>  – change time of day            ║")
    print("║        outside <t>       – set outside temperature       ║")
    print("║        logs              – show event log                ║")
    print("║        quit              – exit simulator                ║")
    print("║                                                          ║")
    print("║                                                          ║")
    print("║                     by Deniss Mihhailov                  ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print()





def setup_home():
    c = SmartHomeController.get_instance()

    # clear previous
    c.rooms.clear()

    # rooms
    kitchen = Room("Kitchen")
    bedroom = Room("Bedroom")
    bathroom = Room("Bathroom")

    # kitchen
    kitchen.add_device(Light("Svet na kuhne"))
    kitchen.add_device(Thermostat("Termostat na kuhne"))
    kitchen.add_device(MotionSensor("Sensor na kuhne"))


    # bedroom
    bedroom.add_device(Light("Svet v spalne"))
    bedroom.add_device(Thermostat("Termostat v spalne"))
    bedroom.add_device(MotionSensor("Sensor v spalne"))


    # bathroom
    bathroom.add_device(Light("Svet v vanne"))
    bathroom.add_device(MotionSensor("Sensor v vanne"))

    c.add_room(kitchen)
    c.add_room(bedroom)
    c.add_room(bathroom)

    return c


def main():
    controller = setup_home()

    print_interface()

    while True:
        cmd = input("> ").strip().split()

        if not cmd:
            print_interface()
            continue

        # quit
        if cmd[0] == "quit":
            print("Bye!")
            time.sleep(1)
            break

        # enter
        elif cmd[0] == "enter":
            if len(cmd) < 2:
                print("Please specify a room. Available rooms:")
                print("  - " + "\n  - ".join(controller.rooms.keys()))
                continue

            room_name = " ".join(cmd[1:])
            if room_name.lower() not in controller.rooms:
                print(f"Unknown room: '{room_name}'")
                print("Available rooms:")
                print("  - " + "\n  - ".join(controller.rooms.keys()))
                continue

            controller.enter_room(room_name)

        # logs
        elif cmd[0] == "logs":
            controller.print_logs()

        # time
        elif cmd[0] == "time":
            if len(cmd) < 2:
                print("Usage: time day / time night")
                continue

            prev = controller._is_night

            if cmd[1] == "night":
                controller.set_is_night(True)
                controller.update_lighting_based_on_time(prev)

            elif cmd[1] == "day":
                controller.set_is_night(False)
                controller.update_lighting_based_on_time(prev)


            else:
                print("Unknown time option (use: day / night)")

        # outside
        elif cmd[0] == "outside":
            if len(cmd) < 2:
                print("Usage: outside <temperature>")
                continue

            try:
                temp = float(cmd[1])

                if temp < -89 or temp > 56:
                    print(f"Temperature '{temp}°C' is unrealistic for Earth.")
                    print("Please enter a value between -89°C and 56°C.")
                    continue

                controller.log_event(f"Outside temperature updated: {temp}°C")

                controller.set_outside_temperature(temp)
                controller.handle_outside_temperature_change()

            except ValueError:
                print("Invalid temperature")


        elif cmd[0] == "status":
            controller.print_status()

        else:
            print(f"Unknown command: '{cmd[0]}'")
            time.sleep(1)
            print_interface()


if __name__ == "__main__":
    main()
