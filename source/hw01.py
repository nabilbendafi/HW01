import binascii
import logging
import struct
import sys
import time

from datetime import datetime
from uuid import UUID

from bluepy.btle import Peripheral, Characteristic, Scanner, DefaultDelegate, ADDR_TYPE_RANDOM, BTLEException

from .constants import UUIDS


class TXDelegate(DefaultDelegate):
    def __init__(self, handle, log):
        DefaultDelegate.__init__(self)
        self.handle = handle
        self._log = log

        self.data = None

    def handleNotification(self, handle, data):
        if self.handle != handle:
            pass
        self.data = data


class HW01(Peripheral):

    def __init__(self, mac_address=None, timeout=0.5, debug=False):
        fmt = '%(asctime)-15s %(name)s (%(levelname)s) > %(message)s'
        logging.basicConfig(format=fmt)
        log_level = logging.WARNING if not debug else logging.DEBUG
        self._log = logging.getLogger(self.__class__.__name__)
        self._log.setLevel(log_level)

        self.timeout = timeout
        self.mac_address = mac_address
        self.state = None

        if not mac_address:
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

        self._log.info('Connecting to ' + mac_address)
        try:
            Peripheral.__init__(self, mac_address, addrType=ADDR_TYPE_RANDOM)
            self._log.info('Connected')
            self.state = 'connected'
        except:
            self._log.error('Failed to established connection to ' + mac_address)
            sys.exit(1)

        # Let HW01 to settle
        self.waitForNotifications(0.1)

    def setup_services(self):
        """Setup BLTE service for HW01."""
        self.service_generic = self.getServiceByUUID(UUIDS.SERVICE_GENERIC)
        self.device_char = self.service_generic.getCharacteristics(UUIDS.CHARACTERISTIC_DEVICE_NAME)[0]

        self._log.info('Setup RX/TX communication')
        self.service_hw01 = self.getServiceByUUID(UUIDS.SERVICE_HW01_B)

        # Enable TX channel (device to host)
        self._log.debug('Get characteristics UUID %s' % UUIDS.CHARACTERISTIC_TX)
        self.tx_char = self.service_hw01.getCharacteristics(UUIDS.CHARACTERISTIC_TX)[0]
        self._log.debug('\tHandle: 0x%04x' % self.tx_char.getHandle())
        self._log.debug('Get its descriptor UUID %s' % UUIDS.NOTIFICATION_DESCRIPTOR)
        self.tx_desc = self.tx_char.getDescriptors(UUIDS.NOTIFICATION_DESCRIPTOR)[0]
        self._log.debug('\tHandle: 0x%04x' % self.tx_desc.handle)
        self._log.debug('Check notification status')
        self._log.debug('\t%s' % ('Enabled' if self.tx_desc.read() == b'\x01\x00' else 'Disabled'))
        self._log.debug('Enable notification')
        self.tx_desc.write(b'\x01\x00')
        self._log.debug('\t%s' % ('Enabled' if self.tx_desc.read() == b'\x01\x00' else 'Disabled'))

        # Enable notification handler
        self.setDelegate(TXDelegate(self.tx_char, self._log))

        # RX channel (host to device)
        self.rx_char = self.service_hw01.getCharacteristics(UUIDS.CHARACTERISTIC_RX)[0]

    def get_device_name(self):
        """Returns device name."""
        return self.device_char.read()

    def get_battery_info(self):
        """Returns battery level information."""
        command = b'AT+BATT'
        self.rx_char.write(command)
        self.waitForNotifications(1.0)
        return self.delegate.data

    def set_seat(self):
        """Returns battery level information."""
        command = b'AT+SIT=0,0900,1800,0'
        self.rx_char.write(command)
        self.waitForNotifications(1.0)
        return self.delegate.data

    def get_serial_number(self):
        """Returns battery level information."""
        command = b'AT+SN'
        self.rx_char.write(command)
        self.waitForNotifications(1.0)
        return self.delegate.data
