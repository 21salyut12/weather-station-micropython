#from time import sleep
#import dht
#from bmp180 import BMP180
#from machine import I2C, Pin, ADC
import machine
import time

# Configure SPI communication
spi = machine.SPI(1, baudrate=10000000, polarity=0, phase=0)
nss_pin = machine.Pin(26, machine.Pin.OUT)
reset_pin = machine.Pin(33, machine.Pin.OUT)
dio0_pin = machine.Pin(25, machine.Pin.IN)

# Configure SX1278 module
nss_pin.on()
reset_pin.off()
time.sleep_ms(100)
reset_pin.on()
time.sleep_ms(100)

# Set LoRa parameters
spi.write(b'\x80')  # Write RegOpMode
spi.write(b'\x00')  # Set Sleep mode

spi.write(b'\x82')  # Write RegFrfMsb
spi.write(b'\x02')  # Set frequency to 868 MHz
spi.write(b'\x80')  # Write RegFrfMid
spi.write(b'\xD9')  # Set frequency to 868 MHz
spi.write(b'\x81')  # Write RegFrfLsb
spi.write(b'\x00')  # Set frequency to 868 MHz

spi.write(b'\x8D')  # Write RegPaConfig
spi.write(b'\x84')  # Set PA_BOOST enabled, max power

spi.write(b'\x8E')  # Write RegPaDac
spi.write(b'\x87')  # Set PA_DAC enabled

spi.write(b'\x96')  # Write RegOcp
spi.write(b'\x2B')  # Set OCP to 100 mA

spi.write(b'\x90')  # Write RegLna
spi.write(b'\x03')  # Set LNA gain to max, boost on

# Specify the maximum payload length
MAX_PAYLOAD_LENGTH = 255

# Function to handle interrupts on DIO0 pin
def handle_interrupt(pin):
    # Check if interrupt was triggered by DIO0 pin
    if pin == dio0_pin:
        # Receive data over SPI
        nss_pin.off()
        spi.write(b'\x00')  # Read RegFifo
        payload_length = bytearray(1)  # Create a buffer to hold the payload length
        spi.readinto(payload_length)  # Read payload length into the buffer
        received_data = bytearray(MAX_PAYLOAD_LENGTH)  # Create a buffer with the appropriate size
        spi.readinto(received_data)  # Read payload into the buffer
        nss_pin.on()

        # Convert received bytes to string
        received_string = str(received_data[:payload_length[0]], "utf-8")

        # Print the received string
        print("Received message: {}".format(received_string))

# Configure interrupt handler for DIO0 pin
dio0_pin.irq(trigger=machine.Pin.IRQ_RISING, handler=handle_interrupt)

# Run an infinite loop to keep the code running
while True:
    time.sleep(1)

"""
# Defining which pins to use for the BMP180
i2c = I2C(scl=Pin(5), sda=Pin(18))

# Variable for BMP180
bmp = BMP180(i2c)

# Defining which pins to use for the YL-83
rain_sensor = ADC(Pin(2), atten=ADC.ATTN_11DB)

# Defining which pins to use for the DHT11
dht_sensor = dht.DHT11(Pin(19))

# Defining which pins to use for the wind speed simulator (potentiometer)
wind_pin = ADC(Pin(35), atten=ADC.ATTN_11DB)

# Defining the range of analog values, wind speed, and rainfall intensity
analog_min = 0  # Minimum analog value
analog_max = 4095  # Maximum value (for 12-bit ADC)
wind_speed_min = 0  # Minimum wind speed (km/h)
wind_speed_max = 100  # Maximum wind speed (km/h)
rainfall_intensity_min = 0  # Minimum rainfall intensity (mm/h)
rainfall_intensity_max = 50  # Maximum rainfall intensity (mm/h)

# Calculate the analog value range per unit of wind speed
analog_range_per_wind_unit = (analog_max - analog_min) / (
    wind_speed_max - wind_speed_min
)

# Calculate the analog value range per unit of rainfall intensity
analog_range_per_rain_unit = (analog_max - analog_min) / (
    rainfall_intensity_max - rainfall_intensity_min
)


# Read the analog value and convert it to wind speed
def get_wind_speed():
    analog_value = wind_pin.read()
    wind_speed = (
        analog_value - analog_min
    ) / analog_range_per_wind_unit + wind_speed_min
    return wind_speed


# Read the analog value and convert it to rain intensity
def get_rain_intensity():
    analog_value = rain_sensor.read()
    rain_intensity = (
        analog_value - analog_min
    ) / analog_range_per_rain_unit + rainfall_intensity_min
    return rain_intensity


# Calculate the average of a list of values
def calculate_average(values):
    if len(values) > 0:
        return sum(values) / len(values)
    else:
        return 0


# Loop to get data from sensors and send data via LoRa
while True:
    try:
        # Lists to store measurements for averaging
        temperature_values = []
        pressure_values = []
        humidity_values = []
        rainfall_intensity_values = []
        wind_speed_values = []

        for _ in range(10):
            # Temperature & Pressure Readings
            temp = bmp.temperature
            pressure = bmp.pressure
            temperature_values.append(temp)
            pressure_values.append(pressure)

            # Humidity Readings
            dht_sensor.measure()
            humidity = dht_sensor.humidity()
            humidity_values.append(humidity)

            # Rain Readings
            rainfall_intensity = get_rain_intensity()
            rainfall_intensity_values.append(rainfall_intensity)

            # Wind Speed Readings
            wind_speed = get_wind_speed()
            wind_speed_values.append(wind_speed)

            # Wait 2 seconds between measurements
            sleep(2)

        # Calculate the average values
        avg_temperature = calculate_average(temperature_values)
        avg_pressure = calculate_average(pressure_values)
        avg_humidity = calculate_average(humidity_values)
        avg_rainfall_intensity = calculate_average(rainfall_intensity_values)
        avg_wind_speed = calculate_average(wind_speed_values)

        # Print the average values
        print("Average Temperature: {} °C".format(avg_temperature))
        print("Average Pressure: {} Pa".format(avg_pressure))
        print("Average Humidity: {}%".format(avg_humidity))
        print("Average Rain Intensity: {:.2f} mm/h".format(avg_rainfall_intensity))
        print("Average Wind Speed: {:.2f} km/h".format(avg_wind_speed))

        # Wait 2 minutes
        sleep(15)
    except OSError as e:
        print("Failed to read from one of the sensors.")
"""