from time import sleep
from bmp180 import BMP180
from machine import I2C, Pin

# Defining which pins to use for the BMP180
i2c = I2C(scl=Pin(26), sda=Pin(25))

# Variable for BMP180
bmp = BMP180(i2c)

while True:
    temp = bmp.temperature
    press = bmp.pressure
    print(temp)
    print(press)
    sleep(5)