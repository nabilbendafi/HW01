import unittest

from unittest import mock

from bluepy.btle import Service, Characteristic, Descriptor
from hw01 import HW01, UUIDS, TXDelegate


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
        for uuid in [UUIDS.SERVICE_GENERIC, UUIDS.SERVICE_HW01_B]:
            services.append(Service(self.h, uuid, 0x0, 0xffff))
        mock_getsrv.side_effect = services

        characteristics = []
        for uuid in [UUIDS.CHARACTERISTIC_DEVICE_NAME, UUIDS.CHARACTERISTIC_TX, UUIDS.CHARACTERISTIC_RX]:
            characteristics.append([Characteristic(self.h, uuid,
                                                   0x47, [0b00000010, 0b00001000], 0x47)])
        mock_getchar.side_effect = characteristics

        mock_desc = [Descriptor(self.h, UUIDS.NOTIFICATION_DESCRIPTOR, 0x12)]
        mock_getdesc.return_value = mock_desc

        with mock.patch('bluepy.btle.Descriptor.read', return_value=(b'\x01\x00')):
            with mock.patch('bluepy.btle.Descriptor.write'):
                with self.assertLogs('HW01') as log:
                    self.h.setup_services()

        self.assertEqual(log.output, ['INFO:HW01:Setup RX/TX communication'])

    def test_notification_for_expected_handle(self):
        """Test Bluetooth notification for TX channel"""
        self.h = HW01('XX:XX:XX:XX:XX:XX')
        mock_char = Characteristic(self.h, UUIDS.CHARACTERISTIC_TX,
                                   0x14, [0b00010000], 0x14)

        tx_delegate = TXDelegate(mock_char.getHandle(), self.h._log)
        self.h.setDelegate(tx_delegate)

        self.assertEqual(tx_delegate.data, None)

        # Trigger notification with expected handle
        self.h.delegate.handleNotification(0x14, 'AT+??')
        self.assertEqual(tx_delegate.data, 'AT+??')

    def test_notification_for_unexpected_handle(self):
        """Test Bluetooth notification for unexpected handle"""
        self.h = HW01('XX:XX:XX:XX:XX:XX')
        mock_char = Characteristic(self.h, UUIDS.CHARACTERISTIC_TX,
                                   0x14, [0b00010000], 0x14)

        tx_delegate = TXDelegate(mock_char.getHandle(), self.h._log)
        self.h.setDelegate(tx_delegate)

        self.assertEqual(tx_delegate.data, None)

        # Trigger notification with expected handle
        self.h.delegate.handleNotification(0xff, 'AT+??')
        self.assertEqual(tx_delegate.data, None)


    @mock.patch('bluepy.btle.Characteristic.read', return_value='HW01')
    def test_device_name(self, mock_device_name):
        """Test device name"""
        self.h = HW01('XX:XX:XX:XX:XX:XX')

        mock_device_char = Characteristic(self.h, '00000000-0000-1000-8000-00805f9b34fb',
                                          0xff, [0b00000010, 0b00001000], 0xff)
        self.h.device_char = mock_device_char

        self.assertEqual(self.h.get_device_name(), 'HW01')

    @mock.patch('hw01.HW01.get_raw', return_value='AT+BATT:80')
    def test_battery_level(self, _):
        """Test battery level"""
        self.h = HW01('XX:XX:XX:XX:XX:XX')

        self.assertEqual(self.h.get_battery_level(), 80)

    @mock.patch('hw01.HW01.get_raw', return_value='AT+SN:HW19999999')
    def test_serial_number(self, _):
        """Test device serial number"""
        self.h = HW01('XX:XX:XX:XX:XX:XX')

        self.assertEqual(self.h.get_serial_number(), 'HW19999999')

if __name__ == '__main__':
    unittest.main()
