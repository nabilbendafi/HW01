"""
Lenovo HW01 API constants
"""
___all__ = ['UUIDS']


class Immutable(type):
    """ Immutable clas """

    # pylint: disable=no-method-argument

    def __call__(*args):
        raise Exception("You can't create instance of immutable object")

    def __setattr__(*args):
        raise Exception("You can't modify immutable object")


class UUIDS():
    """ UUIDS """

    # pylint: disable=too-few-public-methods

    __metaclass__ = Immutable

    BASE = "0000%s-0000-1000-8000-00805f9b34fb"

    SERVICE_GENERIC = BASE % '1800'
    SERVICE_HW01_A = BASE % '190a'
    SERVICE_HW01_B = BASE % '190b'

    CHARACTERISTIC_DEVICE_NAME = BASE % '2a00'
    CHARACTERISTIC_RX = BASE % '0003'
    CHARACTERISTIC_TX = BASE % '0004'

    NOTIFICATION_DESCRIPTOR = BASE % '2902'
