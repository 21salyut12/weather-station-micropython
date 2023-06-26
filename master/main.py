from machine import Pin, SPI
from codes.sx127x import sx127x
import mysql.connector

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
lora.set_frequency(868E6)   # Set the frequency (868MHz for Europe)
lora.set_spreading_factor(7)    # Set the spreding factor (SF7)
lora.set_tx_power(14)   # Set the transmit power (14dBm)

# MySQL database connection configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'weather_informations'
}

# Connect to the MySQL database
db_connection = mysql.connector.connect(**db_config)
db_cursor = db_connection.cursor()

# Function to process received LoRa packets
def process_packet(packet):
    # Decode the received packet
    data = packet.decode('utf-8')

    # Split the data into individual values
    values = data.split(',')

    # Extract the weather information
    temperature = float(values[0])
    pressure = float(values[1])
    humidity = float(values[2])
    rain_intensity = float(values[3])
    wind_speed = float(values[4])

    # Insert the weather information into the database
    query = "INSERT INTO weather_data (temperature, pressure, humidity, rain_intensity, wind_speed) VALUES (%s, %s, %s, %s, %s)"
    values = (temperature, pressure, humidity, rain_intensity, wind_speed)
    db_cursor.execute(query, values)
    db_connection.commit()

# Main loop to receive data from the slave
while True:
    packet = lora.receive()
    if packet is not None:
        process_packet(packet)
