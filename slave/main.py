from time import sleep
import dht
from bmp180 import BMP180
from machine import I2C, Pin, ADC
from codes.sx127x import sx127x

# Defining which pins to use for the BMP180
i2c = I2C(scl=Pin(5), sda=Pin(18))

# Variable for BMP180
bmp = BMP180(i2c)

# Defining which pins to use for the YL-83
rain_sensor = Pin(13, Pin.IN)

# Defining which pins to use for the DHT11
dht_sensor = dht.DHT11(Pin(19))

# Defining which pins to use for the wind speed simulator (potentiometer)
wind_pin = ADC(35)

# Defining which pins to use to connect the esp32 to the lora module
lora = sx127x(
    spi_id=1,
    sck=Pin(27, Pin.OUT),
    mosi=Pin(14, Pin.OUT),
    miso=Pin(12, Pin.IN),
    cs=Pin(26, Pin.OUT),
    reset=Pin(33, Pin.OUT),
    dio0=Pin(25, Pin.IN),
)

# Set LoRa parameters
lora.set_frequency(868E6)  # Set the frequency (868MHz for Europe)
lora.set_spreading_factor(7)  # Set the spreading factor (SF7)
lora.set_tx_power(14)  # Set the transmit power (14 dBm)

# Loop to get data from sensors and send data via LoRa
while True:
    try:
        # Temperature & Pressure Readings
        temp = bmp.temperature
        pressure = bmp.pressure
        print("Temperature: {} °C".format(temp))
        print("Pressure: {} Pa".format(pressure))

        # Humidity Readings
        sleep(1)
        dht_sensor.measure()
        humidity = dht_sensor.humidity()
        print("Humidity: {}%".format(humidity))

        # Rain Readings
        # Reading the sensor's analog value
        rain = rain_sensor.read()
        # Convert the sensor value to rain intensity
        rain_intensity = (rain / 1023) * 100  # assume rain intensity ranges 0-100
        print("Rain Intensity: {}mm/h".format(rain_intensity))

        # Wind Speed Readings
        # Reading the potentiometer value
        wind_value = wind_pin.read()
        # Convert the potentiometer value to wind speed
        wind_speed = (wind_value / 1023) * 100  # Assume wind speed ranges 0-100
        print("Wind Speed: {}m/s".format(wind_speed))

        # Wait 2 minutes
        sleep(120)
    except OSError as e:
        print("Failed to read from one of the sensors.")

    try:
        data = "Temperature: {}, Pressure: {} Pa, Humidity: {}, Rain Intensity: {}, Wind Speed: {}".format(
            temp, pressure, humidity, rain_intensity, wind_speed
        )
        lora.send(data)
        print("Data sent over LoRa.")
    except OSError as e:
        print("Failed to send data.")
