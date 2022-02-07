# Plays a melody on start, then plays a tone whenever the programmable button (GP20) is pressed.
# Copy this file to Maker Nano RP2040 CIRCUITPY drive as code.py to run it on power up.

# This example code uses: Maker Nano RP2040

import board
import digitalio
import simpleio
import time

# Melody
POWERUP_NOTE = [659, 659, 0, 659, 0, 523, 659, 0, 784]
POWERUP_DURATION = [0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.2]

# Define pin connected to piezo buzzer
PIEZO_PIN = board.GP22

# Initialize button
btn = digitalio.DigitalInOut(board.GP20)
btn.direction = digitalio.Direction.INPUT
btn.pull = digitalio.Pull.UP

# Play melody upon start up
print("Playing audio...")
for i in range(len(POWERUP_NOTE)):
    simpleio.tone(PIEZO_PIN, POWERUP_NOTE[i], duration=POWERUP_DURATION[i])
print("Stopped")

while True:
    # Check button 1 (GP20)
    if not btn.value:
        print("Button 1 pressed")
        simpleio.tone(PIEZO_PIN, 262, duration=0.1)
        simpleio.tone(PIEZO_PIN, 659, duration=0.15)
        simpleio.tone(PIEZO_PIN, 784, duration=0.2)

    time.sleep(0.1) # sleep for debounce
