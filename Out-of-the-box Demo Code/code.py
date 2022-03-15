# *************************************************
# Out-of-the-box Demo for Cytron Maker Nano RP2040
# 
# This demo code is written in CircuitPython and it serves
# as an easy quality check when you first receive the board.
#
# It plays a melody upon power up (slide power switch to ON)
# and shows running lights (blue LEDs) at the same time.
# Then the two RGB LEDs will animate the colors, while the 
# program checking push buttons' state, repeatedly.
# 
# More info: 
# 
# https://circuitpython.org/board/raspberry_pi_pico
#
# Email: support@cytron.io
# *************************************************

import board
import digitalio
import neopixel
import simpleio
import time
import pwmio
from adafruit_motor import servo, motor

# Initialize LEDs
# LEDs placement on Maker Pi RP2040
LED_PINS = [board.GP0, 
            board.GP1,
            board.GP2,
            board.GP3,
            board.GP4,
            board.GP5,
            board.GP6,
            board.GP7,
            board.GP8,
            board.GP9,
            board.GP17,
            board.GP19,
            board.GP16]

LEDS = []
for pin in LED_PINS:
    # Set pins as digital output
    digout = digitalio.DigitalInOut(pin)
    digout.direction = digitalio.Direction.OUTPUT
    LEDS.append(digout)

# Initialize Neopixel RGB LEDs
pixels = neopixel.NeoPixel(board.GP11, 2)
pixels.fill(0)

# Melody
MELODY_NOTE = [659, 659, 0, 659, 0, 523, 659, 0, 784]
MELODY_DURATION = [0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.2]

# Define pin connected to piezo buzzer
PIEZO_PIN = board.GP22

# Initialize buttons
btn1 = digitalio.DigitalInOut(board.GP20)
btn1.direction = digitalio.Direction.INPUT
btn1.pull = digitalio.Pull.UP

# -------------------------------------------------
# ON START: Show running light and play melody
# -------------------------------------------------
for i in range(len(LEDS)):
    LEDS[i].value = True
    
    if i < len(MELODY_NOTE):
        # Play melody tones
        simpleio.tone(PIEZO_PIN, MELODY_NOTE[i], duration=MELODY_DURATION[i])
    else:
        # Light up the remainding LEDs
        time.sleep(0.15)

# Turn off LEDs one-by-one very quickly
for i in range(len(LEDS)):
    LEDS[i].value = False
    time.sleep(0.02)


color = 0
state = 0

# -------------------------------------------------
# FOREVER LOOP: Check buttons & animate RGB LEDs
# -------------------------------------------------
while True:
    
    # Check button 1 (GP20)
    if not btn1.value:  # button 1 pressed
        # Light up all LEDs
        for i in range(len(LEDS)):
            LEDS[i].value = True
            
        
        # Play tones
        simpleio.tone(PIEZO_PIN, 262, duration=0.1)
        simpleio.tone(PIEZO_PIN, 659, duration=0.15)
        simpleio.tone(PIEZO_PIN, 784, duration=0.2)
        
        
    # Animate RGB LEDs
    if state == 0:
        if color < 0x101010:
            color += 0x010101   # increase rgb colors to 0x10 each
        else:
            state += 1
    elif state == 1:
        if (color & 0x00FF00) > 0:
            color -= 0x000100   # decrease green to zero
        else:
            state += 1
    elif state == 2:
        if (color & 0xFF0000) > 0:
            color -= 0x010000   # decrease red to zero
        else:
            state += 1
    elif state == 3:
        if (color & 0x00FF00) < 0x1000:
            color += 0x000100   # increase green to 0x10
        else:
            state += 1
    elif state == 4:
        if (color & 0x0000FF) > 0:
            color -= 1          # decrease blue to zero
        else:
            state += 1
    elif state == 5:
        if (color & 0xFF0000) < 0x100000:
            color += 0x010000   # increase red to 0x10
        else:
            state += 1
    elif state == 6:
        if (color & 0x00FF00) > 0:
            color -= 0x000100   # decrease green to zero
        else:
            state += 1
    elif state == 7:
        if (color & 0x00FFFF) < 0x001010:
            color += 0x000101   # increase gb to 0x10
        else:
            state = 1
    pixels.fill(color)  # fill the color on both RGB LEDs
    
    
    # Sleep to debounce buttons & change the speed of RGB color swipe
    time.sleep(0.05)
