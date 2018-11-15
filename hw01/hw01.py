"""
Levono HW01 API
"""
import logging
import sys
from datetime import datetime

from bluepy.btle import Peripheral, Scanner, DefaultDelegate, ADDR_TYPE_RANDOM, BTLEException

from .constants import UUIDS


class TXDelegate(DefaultDelegate):
    """ Abstract a delegate class to handle data """
    def __init__(self, handle, log):
        DefaultDelegate.__init__(self)
        self.handle = handle
        self._log = log

        self.data = None

    def handleNotification(self, cHandle, data):
        self.data = None
        if self.handle != cHandle:
            return
        self._log.debug('Notification on 0x%x: %s' % (cHandle, data))
        self.data = data


class HW01(Peripheral):
    """ Abstract a Lenovo HW01 Bluetooth peripheral """

    # pylint: disable=too-many-instance-attributes

    def __init__(self, mac_address=None, timeout=0.5, debug=False):
        fmt = '%(asctime)-15s %(name)s (%(levelname)s) > %(message)s'
        logging.basicConfig(format=fmt)
        log_level = logging.WARNING if not debug else logging.DEBUG
        self._log = logging.getLogger(self.__class__.__name__)
        self._log.setLevel(log_level)

        self.timeout = timeout
        self.mac_address = mac_address
        self.state = None

        self.service_generic = self.service_hw01 = None
        self.device_char = None
        self.tx_char = self.rx_char = None
        self.tx_desc = None

        Peripheral.__init__(self)

    def connect(self): # pylint: disable=arguments-differ
        """Connect to HW01 peripheral"""

        if not self.mac_address:
            self._log.info('No mac address provided, start BTLE scanning for HW01...')
            scanner = Scanner()

            try:
                devices = scanner.scan(10.0)

                for device in devices:
                    for (_, desc, value) in device.getScanData():
                        print("  %s = %s" % (desc, value))
                        if desc == 'HW01':
                            self._log.info('Found HW01')
                            self.mac_address = device.addr
                            break
            except BTLEException:
                self._log.error('Fail to scan BTLE')
                sys.exit(1)

        try:
            self._log.info('Connecting to %s', self.mac_address)
            super(HW01, self).connect(self.mac_address, addrType=ADDR_TYPE_RANDOM)
            self._log.info('Connected')
            self.state = 'connected'
        except BTLEException:
            self._log.error('Failed to established connection to %s', self.mac_address)
            sys.exit(1)

        # Let HW01 to settle
        self.waitForNotifications(0.1)

    def setup_services(self):
        """Setup BLTE service for HW01."""
        self.service_generic = self.getServiceByUUID(UUIDS.SERVICE_GENERIC)
        self.device_char = self.service_generic.getCharacteristics(UUIDS.CHARACTERISTIC_DEVICE_NAME)[0] # pylint: disable=line-too-long

        self._log.info('Setup RX/TX communication')
        self.service_hw01 = self.getServiceByUUID(UUIDS.SERVICE_HW01_B)

        # Enable TX channel (device to host)
        self._log.debug('Get characteristics UUID %s', UUIDS.CHARACTERISTIC_TX)
        self.tx_char = self.service_hw01.getCharacteristics(UUIDS.CHARACTERISTIC_TX)[0]
        self._log.debug('\tHandle: 0x%04x', self.tx_char.getHandle())
        self._log.debug('Get its descriptor UUID %s', UUIDS.NOTIFICATION_DESCRIPTOR)
        self.tx_desc = self.tx_char.getDescriptors(UUIDS.NOTIFICATION_DESCRIPTOR)[0]
        self._log.debug('\tHandle: 0x%04x', self.tx_desc.handle)
        self._log.debug('Check notification status')
        self._log.debug('\t%s', ('Enabled' if self.tx_desc.read() == b'\x01\x00' else 'Disabled'))
        self._log.debug('Enable notification')
        self.tx_desc.write(b'\x01\x00')
        self._log.debug('\t%s', ('Enabled' if self.tx_desc.read() == b'\x01\x00' else 'Disabled'))

        # Enable notification handler
        self.setDelegate(TXDelegate(self.tx_char.getHandle(), self._log))

        # RX channel (host to device)
        self.rx_char = self.service_hw01.getCharacteristics(UUIDS.CHARACTERISTIC_RX)[0]

    def get_device_name(self):
        """Returns device name."""
        return self.device_char.read()

    def get_raw(self, command):
        """Send AT command request and return device response.

        Args:
            command: AT command to write on :const:`UUIDS.CHARACTERISTIC_RX`

        Returns:
            str: Raw data received on :const:`UUIDS.CHARACTERISTIC_TX`
        """
        self.rx_char.write(command)
        self.waitForNotifications(1.0)
        raw = self.delegate.data
        return raw.decode('utf-8').strip()

    def set_datetime(self, year, month, day, hour=0, minute=0, second=0): # pylint: disable=too-many-arguments
        """Set device clock date and time.

        Args:
            year: Year
            month: Month of year
            day: Day of month
            hour: Hour
            minute: Minute
            seconds: Seconds
        """

        try:
            date_time = datetime(year, month, day, hour, minute, second)
        except ValueError as ve: # pylint: disable=invalid-name
            self._log.error('Failed to set date and time: %s', ve)
            raise
        command = b'AT+DT=%s' % date_time.strftime('%Y%m%d%H%M%S').encode('utf-8')
        raw = self.get_raw(command)
        _ = raw.split(':')[1]
        self._log.info('Date and time set to %s', date_time)

    def get_battery_level(self):
        """Get battery level information.

        Returns:
            int: Battery level in percentage
        """
        command = b'AT+BATT'
        raw = self.get_raw(command)
        try:
            level = int(raw.split(':')[-1])
        except ValueError:
            self._log.error('Failed to parse battery level')
        return level

    def set_seat(self):
        """Set sedentary timeout."""
        command = b'AT+SIT=0,0900,1800,0'
        raw = self.get_raw(command)
        return raw

    def get_version(self):
        """Get Bluetooth version.

        Returns:
            str: Bluetooth version
        """
        command = b'BT+VER'
        raw = self.get_raw(command)
        try:
            blt_version = raw.split(':')[1]
            return blt_version
        except IndexError:
            self._log.error('Failed to parse Bluetooth version')

    def get_serial_number(self):
        """Get device serial number

        Returns:
            str: Device serial number
        """
        command = b'AT+SN'
        raw = self.get_raw(command)
        try:
            serial_number = raw.split(':')[1]
        except IndexError:
            self._log.error('Failed to parse serial number')
        return serial_number

    def set_distance_unit(self, unit='metric'):
        """Set displayed distance unit

        Args:
            unit: Distance unit to set: `metric` or `imperial`
        """
        units = {
            'imperial': 0,
            'metric': 1
        }

        try:
            command = b'AT+UNITS=%i' % units[unit]
            raw = self.get_raw(command)
            try:
                _ = raw.split(':')[1]
                self._log.info('Distance unit set to %s', unit)
            except IndexError:
                self._log.error('Failed to set distance unit')
        except KeyError:
            self._log.error('unit should be within: %s', ", ".join(units.keys()))
