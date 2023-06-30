from machine import I2C, Pin
import ujson

# Configuring I2C communication between the ESP32 boards
i2c_communication = I2C(scl=Pin(26), sda=Pin(25), freq=100000)

i2c_address = 0x12  # Set the I2C address of the slave device

# Function to receive data from the master
def receive_data():
    data = i2c_communication.read()
    return data

# Function to process received data
def process_data(data):
    # Assuming the master sends JSON-encoded data
    data = ujson.loads(data)

    # Perform actions or computations with the received data
    # ...

    # Print the received data
    print("Received Data:")
    print("Temperature: {} °C".format(data["temperature"]))
    print("Pressure: {} Pa".format(data["pressure"]))
    print("Humidity: {}%".format(data["humidity"]))
    print("Rainfall Intensity: {:.2f} mm/h".format(data["rainfall_intensity"]))
    print("Wind Speed: {:.2f} km/h".format(data["wind_speed"]))
    print()

# Main loop
while True:
    # Check if data is available from the master
    if i2c_communication.any():
        # Receive data from the master
        received_data = receive_data()

        # Process the received data
        process_data(received_data)