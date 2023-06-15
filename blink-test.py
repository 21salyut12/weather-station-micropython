from machine import Pin
from time import sleep

pin = Pin(2, Pin.OUT)

while True:
    pin.value(not pin.value())
    sleep(1)