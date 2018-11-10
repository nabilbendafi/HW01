#!/usr/bin/env python3
import sys

from hw01 import HW01

if __name__ == '__main__':
    # Rock'n'Roll
    h = HW01('XX:XX:XX:XX:XX:XX', debug=True)
    h.connect()
    h.setup_services()

    try:
        battery = h.get_battery_info()
        print(battery)
    except KeyboardInterrupt:
        pass
