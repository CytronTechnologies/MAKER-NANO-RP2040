# This example code uses: Maker Nano RP2040

import board
import time
from pwmio import PWMOut
from pitches import tones
import digitalio

time.sleep(1)

# Pixel colours
pixel_off = bytearray([0, 0, 0])
pixel_red = bytearray([0, 10, 0])
pixel_green = bytearray([10, 0, 0])
pixel_blue = bytearray([0, 0, 10])

# Configure pin
pin = digitalio.DigitalInOut(board.GP28)
pin.direction = digitalio.Direction.OUTPUT

time.sleep(1)

tempo = 0.65

melody = (
    'a2','','a2','','a2','b2','','cs3',
    'a3','','d4','d4','','fs4','b4','','fs4','a4','',
    'a4','','b4','a4','','fs4','g4','','fs4','e4','',
    'b3','','e4','e4','','g4','cs5','','cs5','b4','',
    'a4','g4','','g4','','fs4','b3','','cs4','','d4','e4','',

    'a2','','a2','','a2','b2','','cs3',
    'a3','','d4','d4','','fs4','b4','','fs4','a4','',
    'a4','','b4','a4','','fs4','g4','','fs4','e4','',
    'b3','','e4','e4','','g4','cs5','','b4','','a4',
    'g4','','g4','fs4','','e4','cs4','','e4','','d4','',

    'd3','','e3','','fs3','',
    'b4','','b4','','a4','g4','a4','b4','a4','',
    'e4','','fs4','gs4','','e4','a4','',
    'b4','','a4','','e4','','fs4','gs4','','e4','a4','',

    'a2','','a3','','a2','',
    'b4','','a4','','g4','',
    'e4','','cs5','','b4','a4','','b4','a4','','g4','',
    'a4','','b4','fs4','','','e4','d4','',

    'd3','','e3','','fs3','',
    'b4','','a4','','g4','',
    'e4','','cs5','','b4','a4','','b4','a4','','g4','',
    'a4','','b4','fs4','','','e4','d4','',
)
rhythm = [
    4,2,4,4,4,4,4,4,
    4,4,4,4,4,4,4,4,4,4,2,
    4,4,4,4,4,4,4,4,4,4,2,
    4,4,4,4,4,4,4,4,4,4,4,
    4,4,2,4,4,4,4,4,4,2,4,2,4,

    4,2,4,4,4,4,4,4,
    4,4,4,4,4,4,4,4,4,4,2,
    4,4,4,4,4,4,4,4,4,4,2,
    4,4,4,4,4,4,4,2,4,4,4,
    4,4,4,4,4,4,4,2,4,2,2,4,

    4,2,4,2,4,2,
    4,2,4,4,4,4,4,4,4,2,
    4,4,4,4,4,4,2,1,
    4,2,4,2,4,4,4,4,4,4,2,4,

    4,2,4,2,4,2,
    4,2,4,2,2,1,
    4,2,4,4,4,4,4,4,4,4,2,2,
    4,4,4,2,2,4,4,2,4,

    4,2,4,2,4,2,
    4,2,4,2,2,1,
    4,2,4,4,4,4,4,4,4,4,2,2,
    4,4,4,2,2,4,4,2,4,
]

for tone, length in zip(melody, rhythm):
    beeper = PWMOut(board.GP22, variable_frequency=True)
    if tones[tone] != 0:
        beeper.duty_cycle = 2 ** 15
        beeper.frequency = tones[tone]
    time.sleep(tempo/length)
    beeper.deinit()

time.sleep(1)
