Design
======

Communication
-------------

Lenovo HW01 smart watch uses `Bluetooth LE <https://en.wikipedia.org/wiki/Bluetooth_Low_Energy>`_ for communication. It is done through *write*/*notification* mecanism.

  - RX
  Bluetooth characteristic `00000003-0000-1000-8000-00805f9b34fb` is used to emit command from *host* to *device*. You will use this channel to write commands.

  - TX
  Device answers to *host* requests by sending back response in form of notification on Bluetooth characteristic `00000004-0000-1000-8000-00805f9b34fb`, thus no explicit *read* is needed.
  
  Note: Notifications for its `Client Characteristic Configuration descriptor <https://www.bluetooth.com/specifications/gatt/viewer?attributeXmlFile=org.bluetooth.descriptor.gatt.client_characteristic_configuration.xml>`_ need to be enabled in order to receive responses.


Authentication
--------------

No authentication, nor authorization is requested to establish communication beetween host and device.

Binding is not permitted when device is already bond to another host.

Commands
--------

Lenovo HW01 smart watch answers to a set of commands. Each command starts with **AT+** [#AT]_ and is followed by ASCII strings representing:
  - Command name
  - Optional parameters (separated by commas)

Example:

   .. code::

    AT+command


Commands can be used to :
  - Request data.
  - Configure the device (In this case "`=`" sign is used to specifiy arguments).

Example:

   .. code::

    AT+command=param1,param2...

Refer to :doc:`API </api>` for detail.

.. [#AT] https://en.wikipedia.org/wiki/Hayes_command_set

