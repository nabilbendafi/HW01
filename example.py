#!/usr/bin/env python3
import sys

from hw01 import HW01

if __name__ == '__main__':
    # Rock'n'Roll
    h = HW01('XX:XX:XX:XX:XX:XX', debug=True)
    h.connect()
    h.setup_services()

    try:
        battery = h.get_battery_level()
        print(battery)
        h.set_distance_unit('metric')
        version = h.get_version()
        print('Bluetooth HW version: %s', version)
    except KeyboardInterrupt:
        pass
