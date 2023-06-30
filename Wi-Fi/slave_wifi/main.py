import network
import socket

# Wi-Fi credentials
SSID = "DIGI-99Yw"
PASSWORD = "GRG5dpvx"

# Static IP configuration for the receiver
RECEIVER_IP = "192.168.0.100"
SUBNET_MASK = "255.255.255.0"
GATEWAY_IP = "192.168.0.1"

# Connect to Wi-Fi
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(SSID, PASSWORD)

# Wait until connected to Wi-Fi
while not wifi.isconnected():
    pass

print("Connected to Wi-Fi")

# Configure static IP address for the receiver
wifi.ifconfig((RECEIVER_IP, SUBNET_MASK, GATEWAY_IP, GATEWAY_IP))

print("Receiver IP:", RECEIVER_IP)

# Create a socket and listen for incoming connections
server_socket = socket.socket()
server_socket.bind((RECEIVER_IP, 1234))
server_socket.listen(1)

print("Waiting for connection...")

# Accept a client connection
client_socket, client_address = server_socket.accept()

print("Connected to sender:", client_address)

# Receive data from the sender
data = client_socket.recv(1024)
message = data.decode()

print("Received message:", message)

# Close the sockets
client_socket.close()
server_socket.close()
