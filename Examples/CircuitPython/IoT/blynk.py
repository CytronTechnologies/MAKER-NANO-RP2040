################################################################################
# Example for Blynk.
# Showing the status of virtual pin V0 on LED GP0.
# Send the status of push button GP20 to virtual pin V1.
#
# Hardware:
# - Maker Pi Pico / Maker Pi RP2040 / Maker Nano RP2040
# - ESP8266 WiFi module with Espressif AT Firmware v2.2.0 and above.
#
# Dependencies:
# - adafruit_requests
# - adafruit_espatcontrol
#
# Instructions:
# - Copy the lib folder to the CIRCUITPY device.
# - Modify the keys in secrets.py and copy to the CIRCUITPY device.
# - Make sure the UART pins are defined correctly according to your hardware.
#
#
# Author: Cytron Technologies
# Website: www.cytron.io
# Email: support@cytron.io
################################################################################

import time
import board
import digitalio
import busio
import adafruit_requests as requests
import adafruit_espatcontrol.adafruit_espatcontrol_socket as socket
from adafruit_espatcontrol import adafruit_espatcontrol


# Get wifi details and more from a secrets.py file
try:
    from secrets import secrets
except ImportError:
    print("All secret keys are kept in secrets.py, please add them there!")
    raise

# Initialize LED and button.
led = digitalio.DigitalInOut(board.GP18)
led.direction = digitalio.Direction.OUTPUT

button = digitalio.DigitalInOut(board.GP20)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

# Initialize UART connection to the ESP8266 WiFi Module.
RX = board.GP1
TX = board.GP0
uart = busio.UART(TX, RX, receiver_buffer_size=2048)  # Use large buffer as we're not using hardware flow control.

esp = adafruit_espatcontrol.ESP_ATcontrol(uart, 115200, debug=False)
requests.set_socket(socket, esp)

print("Resetting ESP module")
esp.soft_reset()

while True:
    try:
        # Make sure WiFi is connected.
        while not esp.is_connected:
            print("Connecting...")
            esp.connect(secrets)

        # Reading Blynk virtual pin V0.
        # Turn on/off on board LED depending on the value of virtual pin V0
        r = requests.get("https://blynk.cloud/external/api/get?token=" + secrets["blynk_auth_token"] + "&v0")
        led.value = int(r.text)

        # Writting Blynk virtual pin V1.
        # Sending value 255 if button is pressed, 0 otherwise.
        # Can use LED widget on Blynk App to show the value.
        if not button.value:
            # Button pressed.
            value = 255
        else:
            value = 0
        requests.get("https://blynk.cloud/external/api/update?token=" + secrets["blynk_auth_token"] + "&v1=" + str(value))

    except (ValueError, RuntimeError, adafruit_espatcontrol.OKError) as e:
        print("Failed, retrying\n", e)
