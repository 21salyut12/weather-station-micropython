import ubluetooth as bluetooth

# Define the UUID and service
service_uuid = bluetooth.UUID('6E400001-B5A3-F393-E0A9-E50E24DCCA9E')
char_uuid = bluetooth.UUID('6E400003-B5A3-F393-E0A9-E50E24DCCA9E')

# Initialize Bluetooth
bluetooth.init()

# Create the BLE advertisement data
adv = bluetooth.AdvertisingData()
adv.complete_name = 'ESP32 B'
adv.uuids = [service_uuid]

# Start advertising
bluetooth.set_advertising([adv])
bluetooth.start_advertising()

# Create the BLE client and connect to the server
client = bluetooth.BLE()
conn = client.connect(service_uuid)

# Find the characteristic for receiving data
char_rx = conn.characteristic(char_uuid)

# Callback function for handling received data
def handle_rx(data):
    print('Received:', data)

char_rx.callback(handle_rx)

# Keep the program running to receive data
while True:
    pass

# Stop advertising
bluetooth.stop_advertising()