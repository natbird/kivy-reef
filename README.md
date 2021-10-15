# Kivy Reef
A touchscreen client for [reef-pi](https://github.com/reef-pi/reef-pi), written in Kivy and Python 3.

## Features
- Display sensor readings (temperature, pH, flowmeters)
- Control equipment (On/Off)
- View usage of dosers and ATOs
- Run/reverse macros
- View system information and re-load reef-pi / reboot / shutdown host

## Screenshots
Main screen:
![image](https://user-images.githubusercontent.com/1696014/137360178-8b03cb42-0d34-426a-b749-c00f841d66fe.png)

Sensor readings:
![image](https://user-images.githubusercontent.com/1696014/137360228-2af1b5e8-28cb-4ae7-b49c-709979570069.png)

Equipment control:
![image](https://user-images.githubusercontent.com/1696014/137360267-ff1197e9-23b9-43de-ab35-59fe20f99973.png)

Usage readings:
![image](https://user-images.githubusercontent.com/1696014/137360291-4e8028ab-7138-4c4b-a262-1505bfc5f546.png)

Macros:
![image](https://user-images.githubusercontent.com/1696014/137361234-5776d881-d2ee-4682-a28c-e5d57ad2c1a2.png)

System information:
![image](https://user-images.githubusercontent.com/1696014/137362172-45219591-0ade-4a0e-b829-3d612627fea0.png)

## Instructions
Kivy Reef can be run either as a desktop application on Linux / MacOS / Windows (not tested) or from the console on Linux systems, in which case it will output directly to an attached display.

### Dependencies
- Python 3.6+
- [Python Requests library](https://pypi.org/project/requests/)
- [Eclipse Paho MQTT Python client library](https://pypi.org/project/paho-mqtt/)
- [Kivy 2.0.0](https://kivy.org/doc/stable/gettingstarted/installation.html) If installing on a Raspberry Pi, you must first install the [required dependencies](https://kivy.org/doc/stable/installation/installation-rpi.html#install-source-rpi), including compiling SLD2 if you intend to run without X11/Wayland (see further below).

### Running without X11/Wayland
On Linux systems, Kivy Reef can be run from the console and output directly to an attached display via SDL2.

If you are running Raspbian, you will need to compile SDL2 from source to enable support for the kmsdrm backend before install Kivy – see the instructions here: https://kivy.org/doc/stable/installation/installation-rpi.html#raspberry-pi-4-headless-installation-on-raspbian-buster

Note that kivy-reef will need to be started from a local console (not via ssh) or a systemd service.

### Config
On first run, Kivy Reef will create a config file containing default options in .ini format. Edit this file to suit and re-start Kivy Reef.

### Running Kivy Reef
From the location where you have cloned extracted Kivy Reef:
```
python3 main.py
```

## Acknowledgments
Thank you to Ranjib and the rest of the [reef-pi team](https://github.com/reef-pi/reef-pi#maintainers) for making reef-pi awesome.

The [Orbitron font](https://fonts.google.com/specimen/Orbitron) is part of the Google Fonts library and is licenced under the Open Font Licence.
All icons are from the [Google Material Design Icons](https://fonts.google.com/icons) and are licenced under the Apache License, Version 2.0.
