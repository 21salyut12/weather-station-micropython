import network
from time import sleep
from machine import I2C, Pin, ADC
import dht
from bmp180 import BMP180

# Wi-Fi credentials
SSID = "DIGI-99Yw"
PASSWORD = "GRG5dpvx"

# Connect to Wi-Fi
wifi = network.WLAN(network.STA_IF)
wifi.active(True)

def connect_to_wifi():
    wifi.connect(SSID, PASSWORD)
    retries = 0
    # Retry 5 times to connect via Wi-Fi
    while not wifi.isconnected() and retries < 5:
        retries += 1
        sleep(2)
    if wifi.isconnected():
        print("Wi-Fi connected!\nIP address: {}".format(wifi.ifconfig()[0]))
    else:
        print("Failed to connect to Wi-Fi")

# Reset connection if neccesary
def reset_wifi_interface():
    wifi.disconnect()
    wifi.active(False)
    sleep(1)
    wifi.active(True)

connect_to_wifi()
reset_wifi_interface()