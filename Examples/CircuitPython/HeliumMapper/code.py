import time
import board
import busio
import digitalio
import neopixel
import adafruit_gps
from lora_e5_atcontrol import E5_ATControl
from helium_config import helium_config


# Initialize push button.
btn = digitalio.DigitalInOut(board.GP20)
btn.direction = digitalio.Direction.INPUT


# Initialize neopixels.
num_pixels = 2
pixels = neopixel.NeoPixel(board.GP11, num_pixels)
pixels.brightness = 0.3


# Initialize UART 1 for GPS.
gps_tx = board.GP4
gps_rx = board.GP5
uart_gps = busio.UART(gps_tx, gps_rx, baudrate=9600, timeout=10, receiver_buffer_size=2048)

gps = adafruit_gps.GPS(uart_gps)


# Initialize UART 0 for E5 LoRaWAN module.
e5_tx = board.GP0
e5_rx = board.GP1
uart_e5 = busio.UART(e5_tx, e5_rx, baudrate=9600)
e5 = E5_ATControl(uart_e5)

# Set neopixel 1 to white.
pixels[1] = (255, 255, 255)

# Configure E5 LoRaWAN module.
init_successful = True
if init_successful: init_successful &= e5.send_atcommand('AT+MODE=LWOTAA\r\n', '+MODE: LWOTAA', 1)
if init_successful: init_successful &= e5.send_atcommand('AT+DR=' + helium_config['region'] + '\r\n', '+DR: ' + helium_config['region'], 1)
if init_successful: init_successful &= e5.send_atcommand('AT+REPT=1\r\n', '+REPT: 1', 1)
if init_successful: init_successful &= e5.send_atcommand('AT+ADR=OFF\r\n', '+ADR: OFF', 1)
if init_successful: init_successful &= e5.send_atcommand('AT+ID=DevEui,"' + helium_config['deveui'] + '"\r\n', '+ID: DevEui', 1)
if init_successful: init_successful &= e5.send_atcommand('AT+ID=AppEui,"' + helium_config['appeui'] + '"\r\n', '+ID: AppEui', 1)
if init_successful: init_successful &= e5.send_atcommand('AT+KEY=APPKEY,"' + helium_config['appkey'] + '"\r\n', '+KEY: APPKEY', 1)

# Fail to initialize Lora E5.
if (not init_successful):
    # Set neopixel 1 to red to indicate failed to configure E5.
    pixels[1] = (255, 0, 0)
    while True:
        pass

# Set neopixel 1 to yellow.
pixels[1] = (255, 180, 0)

# Try joining the Helium Network.
e5.send_atcommand("AT+JOIN=FORCE\r\n", "+JOIN: Done", 15)

# Turn off neopixel 1.
pixels[1] = (0, 0, 0)



timestamp = -999
while True:
    gps_data_received = gps.update()
    
    # Waiting for GPS fix.
    if not gps.has_fix:
        # Blink neopixel in red with GPS data received.
        if gps_data_received:
            pixels[0] = (255, 0, 0)
        else:
            pixels[0] = (0, 0, 0)
        continue
    
    # GPS fixed.
    # Blink neopixel in green with GPS data received.
    if gps_data_received:
        pixels[0] = (0, 255, 0)
    else:
        pixels[0] = (0, 0, 0)
        
        
    # Waiting for speed information.
    if gps.speed_knots == None:
        continue
        
        
        
    # Determine the update period base on speed.
    period = 0.0
    # 10 seconds if > 60km/h
    if gps.speed_knots * 1.852 > 60.0:
        period = 10.0
    # 20 seconds if 30km/h - 60km/h
    elif gps.speed_knots * 1.852 > 30.0:
        period = 20.0
    # 1 minute if < 30km/h
    else:
        period = 60.0
        
    
    # Send the location when timeout or button GP20 is pressed.
    if time.monotonic() - timestamp > period or btn.value == 0:
        while btn.value == 0:
            pass
        
        timestamp = time.monotonic()
        
        # Send message.
        while True:
            # Set neopixel 1 to blue.
            pixels[1] = (0, 0, 255)
            
            altitude = 0.0
            if gps.altitude_m != None:
                altitude = gps.altitude_m
                
            cmd = 'AT+MSGHEX="{:08X}{:08X}{:04X}"\r\n'.format(int(gps.latitude * 1E7), int(gps.longitude * 1E7), int(altitude * 100))
            if not e5.send_atcommand(cmd, '+MSGHEX: Done', 5):
                
                if "Please join network first" in e5.response:
                    # Set neopixel 1 to yellow.
                    pixels[1] = (255, 180, 0)
                    
                    # We need to join the network first.
                    e5.send_atcommand('AT+JOIN=FORCE\r\n', '+JOIN: Done', 15)
                    
                    # Try sending location again if network joined successfully.
                    if '+JOIN: Network joined' in e5.response:
                        continue
                    
            break
        
        # Turn off neopixel 1.
        pixels[1] = (0, 0, 0)
