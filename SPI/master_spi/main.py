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

MAX_PAYLOAD_LENGTH = 255

delay_before_send = 10
time.sleep(delay_before_send)

# Send continuous stream of numbers
count = 0
while True:
    # Define the number to send
    message = str(count)

    # Send data over SPI
    nss_pin.off()
    spi.write(b'\x80')  # Write RegOpMode
    spi.write(b'\x01')  # Set LoRa mode, Standby mode

    spi.write(b'\x80')  # Write RegOpMode
    spi.write(b'\x80')  # Set LoRa mode, Tx mode

    spi.write(b'\x80')  # Write RegOpMode
    spi.write(b'\x83')  # Set LoRa mode, Tx mode, StartTx

    spi.write(b'\x00')  # Write RegFifo
    spi.write(bytes([len(message)]))  # Set payload length
    spi.write(bytes(message, "utf-8"))  # Set payload data
    nss_pin.on()

    print("Message sent: {}".format(message))
    count += 1
    time.sleep(1)