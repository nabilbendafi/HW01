Lenovo HW01
===========

Library to work with Lenovo HW01. To be used in place of Android [Lenovo Healthy](https://play.google.com/store/apps/details?id=com.lenovohw.base.framework) app.

Dependencies
------------
 - [bluepy](https://github.com/IanHarvey/bluepy)


Traffic analysis
----------------
In order to analyse communication between official Android app [Lenovo Healthy](https://play.google.com/store/apps/details?id=com.lenovohw.base.framework&hl=en_US) and Lenovo HW01 device, additional app [NordicSemiconductor/Android-nRF-Connect](https://github.com/NordicSemiconductor/Android-nRF-Connect) is used to perform traffic logging.

It allows us to write an API library to interact with the watch without using the official Android app.

Debugging
---------
```bash
$> sudo hcitool lescan
LE Scan ...
XX:XX:XX:XX:XX:XX HW01
```

```bash
sudo gatttool --device=XX:XX:XX:XX:XX:XX -I -t random
[XX:XX:XX:XX:XX:XX][LE]> connect
Attempting to connect to XX:XX:XX:XX:XX:XX
Connection successful

[XX:XX:XX:XX:XX:XX][LE]> primary
attr handle: 0x0001, end grp handle: 0x0007 uuid: 00001800-0000-1000-8000-00805f9b34fb
attr handle: 0x0008, end grp handle: 0x0008 uuid: 00001801-0000-1000-8000-00805f9b34fb
attr handle: 0x0009, end grp handle: 0x000e uuid: 0000190a-0000-1000-8000-00805f9b34fb
attr handle: 0x000f, end grp handle: 0x0014 uuid: 0000190b-0000-1000-8000-00805f9b34fb
attr handle: 0x0015, end grp handle: 0xffff uuid: 0000fee7-0000-1000-8000-00805f9b34fb
```

References
----------
 - [creotiv/MiBand2](https://github.com/creotiv/MiBand2)
 - [My journey towards Reverse Engineering a Smart Band — Bluetooth-LE RE](https://medium.com/@arunmag/my-journey-towards-reverse-engineering-a-smart-band-bluetooth-le-re-d1dea00e4de2)
 - [Xiaomi Mi Band BLE Protocol reverse-engineering and API](http://androiders-newbie.blogspot.com/2014/12/xiaomi-mi-band-ble-protocol-reverse.html)
 - [How I hacked my Xiaomi MiBand 2 fitness tracker — a step-by-step Linux guide](https://medium.com/machine-learning-world/how-i-hacked-xiaomi-miband-2-to-control-it-from-linux-a5bd2f36d3ad)
 - [Get Started with Bluetooth Low Energy on Linux](https://www.jaredwolff.com/blog/get-started-with-bluetooth-low-energy/)
 - [NordicSemiconductor/Android-nRF-Connect](https://github.com/NordicSemiconductor/Android-nRF-Connect)
