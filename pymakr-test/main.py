from time import sleep
import dht
from bmp180 import BMP180
from machine import I2C, Pin
from codes.sx127x import sx127x

# Defining what pins to use for the BMP180
i2c = I2C(scl=Pin(5), sda=Pin(18))

# Variable for BMP180
bmp = BMP180(i2c)

# Defining what pins to use for the YL-83
rain_sensor = Pin(13, Pin.IN)

# Defining what pins to use for the DHT11
dht_sensor = dht.DHT11(Pin(19))

lora = sx127x()

# Loop to get data from sensors and send data via LoRa
while True:
    try:
        # Temperature&Pressure
        temp = bmp.temperature
        pressure = bmp.pressure
        print("Temperature: {} °C".format(temp))
        print("Pressure: {} Pa".format(pressure))

        # Temperature&Humidity
        sleep(1)
        dht_sensor.measure()
        humidity = dht_sensor.humidity()
        print("Humidity: {}%".format(humidity))

        # Rain
        rain = rain_sensor.value()
        print("Is it raining? {}.".format(rain))
        # Wait 2 minutes
        sleep(60)
    except OSError as e:
        print("Failed to read from one of the sensors.")

    try:
        data = "Temperature: {}, Pressure: {} Pa, Humidity: {}, Rain: {}".format(temp, pressure, humidity, rain)
        lora.send(data)
    except OSError as e:
        print("Failed to send data.")
