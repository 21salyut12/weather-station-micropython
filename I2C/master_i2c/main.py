from time import sleep
import dht, ujson
from bmp180 import BMP180
from machine import I2C, Pin, ADC

# Configuring I2C communication between the ESP32 boards
i2c_communication = I2C(scl=Pin(19), sda=Pin(21), freq=100000)
slave_address = 0x12

# Defining which pins to use for the BMP180
bmp_i2c = I2C(scl=Pin(5), sda=Pin(18))

# Variable for BMP180
bmp = BMP180(bmp_i2c)

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
analog_range_per_wind_unit = (analog_max - analog_min) / (wind_speed_max - wind_speed_min)

# Calculate the analog value range per unit of rainfall intensity
analog_range_per_rain_unit = (analog_max - analog_min) / (rainfall_intensity_max - rainfall_intensity_min)


# Read the analog value and convert it to wind speed
def get_wind_speed():
    analog_value = wind_pin.read()
    wind_speed = (analog_value - analog_min) / analog_range_per_wind_unit + wind_speed_min
    return wind_speed


# Read the analog value and convert it to rain intensity
def get_rain_intensity():
    analog_value = rain_sensor.read()
    rain_intensity = (analog_value - analog_min) / analog_range_per_rain_unit + rainfall_intensity_min
    return rain_intensity


# Calculate the average of a list of values
def calculate_average(values):
    if len(values) > 0:
        return sum(values) / len(values)
    else:
        return 0


# Send data to the slave
def send_data(data):
    i2c_communication.writeto(slave_address, data)



# Main loop
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
        
        # Read sensor data and package it
        # Package the sensor data as a JSON object
        data = {
            "temperature": avg_temperature,
            "pressure": avg_pressure,
            "humidity": avg_humidity,
            "rainfall_intensity": avg_rainfall_intensity,
            "wind_speed": avg_wind_speed,
        }

        ujson.dumps(data)
        # Wait 2 minutes before beginning the measurements again
        sleep(120)
    except OSError as e:
        print("Failed to read from one of the sensors.")