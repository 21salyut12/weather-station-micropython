import ubluetooth as bluetooth

# Define the UUID and service
service_uuid = bluetooth.UUID('6E400001-B5A3-F393-E0A9-E50E24DCCA9E')
char_uuid = bluetooth.UUID('6E400003-B5A3-F393-E0A9-E50E24DCCA9E')

# Create the BLE UART service
uart_service = bluetooth.UUID('6E400001-B5A3-F393-E0A9-E50E24DCCA9E')
uart_tx = (bluetooth.UUID('6E400003-B5A3-F393-E0A9-E50E24DCCA9E'), bluetooth.FLAG_NOTIFY,)
uart_rx = (bluetooth.UUID('6E400002-B5A3-F393-E0A9-E50E24DCCA9E'), bluetooth.FLAG_WRITE,)

# Initialize Bluetooth
bluetooth.init()

# Create the BLE advertisement data
adv = bluetooth.AdvertisingData()
adv.complete_name = 'ESP32 A'
adv.uuids = [service_uuid]

# Start advertising
bluetooth.set_advertising([adv])
bluetooth.start_advertising()

# Create the BLE server and service
server = bluetooth.BLE()
service = server.service(uuid=uart_service)

# Create the characteristic for sending data
char_tx = service.characteristic(uuid=char_uuid, properties=bluetooth.FLAG_NOTIFY)

while True:
    data = input('Enter data to send: ')
    char_tx.value(data)

# Stop advertising
bluetooth.stop_advertising()