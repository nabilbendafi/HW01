import unittest

from unittest import mock

from bluepy.btle import Service, Characteristic, Descriptor
from hw01 import HW01


class HW01TestSuite(unittest.TestCase):
    """HW01 test cases."""

    def test_connect_with_bad_address(self):
        """Test connection to device with bad mac address"""
        mac_address = 'XX:XX:XX:XX:XX:XX'
        self.h = HW01(mac_address)

        self.assertEqual(self.h.mac_address, mac_address)

        with self.assertRaises(SystemExit) as _:
            with self.assertLogs('HW01') as log:
                self.h.connect()

        self.assertEqual(log.output, ['INFO:HW01:Connecting to %s' % mac_address,
                                      'ERROR:HW01:Failed to established connection to %s' % mac_address])

    def test_connect_without_address(self):
        """Test connection to device without providing mac address"""
        self.h = HW01()

        self.assertEqual(self.h.mac_address, None)

        with self.assertRaises(SystemExit) as _:
            with self.assertLogs('HW01') as log:
                self.h.connect()

        self.assertEqual(log.output, ['INFO:HW01:No mac address provided, start BTLE scanning for HW01...',
                                      'ERROR:HW01:Fail to scan BTLE'])

    @mock.patch('bluepy.btle.Characteristic.getDescriptors')
    @mock.patch('bluepy.btle.Service.getCharacteristics')
    @mock.patch('bluepy.btle.Peripheral.getServiceByUUID')
    def test_service_setup(self, mock_getsrv, mock_getchar, mock_getdesc):
        """Test service setup"""
        self.h = HW01('XX:XX:XX:XX:XX:XX')

        services = []
        for service in ['1800', '190b']:
            services.append(Service(self.h, '0000%s-0000-1000-8000-00805f9b34fb' % service, 0x0, 0xffff))
        mock_getsrv.side_effect = services

        characteristics = []
        for char in ['2a00', '0003', '0004']:
            characteristics.append([Characteristic(self.h, '0000%s-0000-1000-8000-00805f9b34fb' % char,
                                                   0x47, [0b00000010, 0b00001000], 0x47)])
        mock_getchar.side_effect = characteristics

        mock_desc = [Descriptor(self.h, '00002902-0000-1000-8000-00805f9b34fb', 0x12)]
        mock_getdesc.return_value = mock_desc

        with mock.patch('bluepy.btle.Descriptor.read', return_value=(b'\x01\x00')):
            with mock.patch('bluepy.btle.Descriptor.write'):
                with self.assertLogs('HW01') as log:
                    self.h.setup_services()

        self.assertEqual(log.output, ['INFO:HW01:Setup RX/TX communication'])

    @mock.patch('bluepy.btle.Characteristic.read', return_value='HW01')
    def test_device_name(self, mock_device_name):
        """Test device name"""
        self.h = HW01('XX:XX:XX:XX:XX:XX')

        mock_device_char = Characteristic(self.h, '00000000-0000-1000-8000-00805f9b34fb',
                                          0xff, [0b00000010, 0b00001000], 0xff)
        self.h.device_char = mock_device_char

        self.assertEqual(self.h.get_device_name(), 'HW01')

    @mock.patch('hw01.HW01.get_raw', return_value='AT+BATT:80')
    def test_battery_info(self, mock_battery_info):
        """Test battery level"""
        self.h = HW01('XX:XX:XX:XX:XX:XX')

        self.assertEqual(self.h.get_battery_info(), 80)

    @mock.patch('hw01.HW01.get_raw', return_value='AT+SN:HW19999999')
    def test_serial_number(self, mock_battery_info):
        """Test device serial number"""
        self.h = HW01('XX:XX:XX:XX:XX:XX')

        self.assertEqual(self.h.get_serial_number(), 'HW19999999')

if __name__ == '__main__':
    unittest.main()
