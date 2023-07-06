# Weather Station Project With Micropython

## Description

This project is one of two main components for my bachelor project. This being the first big component and the second one being the [Front-end React App](https://github.com/21salyut12/weather-react-app).
Main objective is to send to the realtime database measurements regarding temperature, atmospheric pressure, humidity, rainfall intensity and wind speed, as well as a timestamp for these measurements and their respective weather station' location.
Initially this project was supposed to contain a slave and a master that communicate through IoT technologies or protocols but along the way the master had burned out so I had to combine it's functionality with the slave and thus the final version of this project is just the [master folder](https://github.com/21salyut12/weather-station-micropython/tree/main/master)

## Libraries I've used to make my work a lot easier:

- [Micropython-Firebase-Realtime-Database](https://github.com/ckoever/micropython-firebase-realtime-database);
- [Micropython-BMP180](https://github.com/micropython-IMU/micropython-bmp180);
- And rest of the libraries that have been used are all built into micropython.

## ESP32

I used the ESP32-Devkit-V1 development board and in order to connect to it and program it using micropython I had to install the following:
- [CP210X Driver](https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers) to make my PC communicate with the board
- [Micropython Firmware](https://micropython.org/download/esp32/) (here you'll also find how to flash the firmware onto the ESP32)
- Also because of the fact that i used Visual Studio as my IDE I had to install the PyMakr extension (here's a quick tutorial on how you can [blink the onboard led of the ESP32](https://www.youtube.com/watch?v=YOeV14SESls&t=270s))

## Sensors used
- BMP180 for temperature and pressure readings
- DHT11 for humidity readings
- YL-83 - rain intensity
- A potentiometer to simulate the functionality of a wind sensor (anemometer)
