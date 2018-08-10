import unittest


class HW01TestSuite(unittest.TestCase):
    """HW01 test cases."""

    def test_device_name(self):
        self.assertEqual('HW01', 'HW01')


if __name__ == '__main__':
    unittest.main()
