import dht
from bmp180 import BMP180
from machine import I2C, Pin
from time import sleep

# Temperature&Pressure variables
i2c = I2C(scl=Pin(18), sda=Pin(5))

bmp = BMP180(i2c)

rain_sensor = Pin(13, Pin.IN)

dht_pin = dht.DHT11(Pin(19))



# Loop to get data from sensors
while True:
    # Temperature&Pressure
    temp = bmp.temperature
    pressure = bmp.pressure
    print("Temperature: {} °C".format(temp))
    print("Pressure: {} Pa".format(pressure))

    # Rain
    rain = rain_sensor.value()
    print("Is it raining? {}.".format(rain))

    sleep(30)