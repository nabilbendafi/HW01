API
===

Battery level
-------------

Retrieve current device battery level

.. list-table::
   :header-rows: 1

   * - Request
     - Response
   * - AT+BATT
     - AT+BATT:`level`

.. list-table:: Field description
   :header-rows: 1

   * - Field
     - Description
   * - `level`
     - Battery level in percentage.

Example:

  .. code::

    AT+BATT:50

  is returned when device is half discharged

Serial number
-------------

Retrieve device serial number

.. list-table::
   :header-rows: 1

   * - Request
     - Response
   * - AT+SN
     - AT+SN:`serial_num`

.. list-table:: Field description
   :header-rows: 1

   * - Field
     - Description
   * - `serial_num`
     - Unique device serial number.

Example:

   .. code::

    AT+SN:HW19999999

Alarms
------
Two alarms can be set and device will vibrate when triggered

First alarm
^^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Request
     - Response
   * - AT+ALARM=\ `enable,??,activation,time`
     - AT+ALARM:\ `enable,??,activation,time`

.. list-table:: Field description
   :header-rows: 1

   * - Field
     - Description
   * - `enable`
     - **0** for *ON*, **1** for *OFF*
   * - `interval`
     - Interval in minutes.
   * - `activation`
     - Day specific activation. See below `Day activation` for details
   * - `time`
     - HHMM format


.. list-table:: Day activation
   :header-rows: 1

   * - Bit
     - Day
   * - 1000000
     - Monday
   * - 0100000
     - Tuesday
   * - 0010000
     - Wednesday
   * - 0001000
     - Thursday
   * - 0000100
     - Friday
   * - 0000010
     - Saturday
   * - 0000001
     - Sunday

Example:

  .. code::

    AT+ALARM=1,00,11111001,0800

  will setup an alarm at **08:00** every weekday (Monday to Friday)

Second alarm
^^^^^^^^^^^^
.. list-table::
   :header-rows: 1

   * - Request
     - Response
   * - AT+ALARM2=\ `A,BB,activation,time`
   * - AT+ALARM2:\ `A,BB,activation,time`

Example:

  .. code::

    AT+ALARM2=1,00,000000001,1000

  will setup an alarm at **10:00** on Saturday only


Sedentary
---------

Enable/Disable sedentary alarm to remind you to move and not to stay seated for too long period.

.. list-table::
   :header-rows: 1

   * - Request
     - Response
   * - AT+SIT=0\ `interval,start_time,end_time,enable`
     - AT+SIT:0\ `interval,start_time,end_time,enable`

.. list-table:: Field description
   :header-rows: 1

   * - Field
     - Description
   * - `interval`
     - Interval in minutes.
   * - `start_time`
     - HHMM format
   * - `end_time`
     - HHMM format
   * - `enable`
     - **0** for *ON*, **1** for *OFF*

Example:

  .. code::

    AT+SIT=030,0800,1800,1

  will enable sedentary alarm from **08:00** to **18:00** when no movement is detected within **30 minutes** intervals
