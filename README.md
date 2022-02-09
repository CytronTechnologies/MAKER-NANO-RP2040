# MAKER-NANO-RP2040
### Simplifying Projects with Raspberry Pi RP2040

[Maker Nano RP2040](https://my.cytron.io/maker-nano-rp2040-simplifying-projects-with-raspberry-pi-rp2040) is a small but powerful MCU for your project. It has the same Arduino Nano form factor, but powered by a much more powerful [RP2040](https://www.raspberrypi.com/documentation/microcontrollers/rp2040.html) MCU from Raspberry Pi. It has 14 status indicator LEDs for GPIOs, 1 piezo buzzer with mute switch, 1 programmable push button, 2 RGB LEDs (WS2812 Neopixel), 2 Maker Ports - compatible with Qwiic, STEMMA QT, Grove (via conversion cable).

![alt text](https://github.com/CytronTechnologies/MAKER-NANO-RP2040/blob/main/MAKER-NANO-RP2040-Image.PNG)

# Getting Started & Examples

We provide some [examples](https://github.com/CytronTechnologies/MAKER-NANO-RP2040/tree/main/Examples) in CircuitPython and MicroPython for your reference. Make sure the correct firmware is loaded on your Maker Nano RP2040 before you start coding with either languages.

### CircuitPython
We've created the [CircuitPython .UF2 firmware for Maker Nano RP2040](https://circuitpython.org/board/cytron_maker_nano_rp2040/) with helps from the awesome folks at CircuitPython and Adafruit. It includes the libraries to work with Maker Nano RP2040's built-in features. [Neopixel](https://github.com/adafruit/Adafruit_CircuitPython_NeoPixel) and [simpleio](https://github.com/adafruit/Adafruit_CircuitPython_SimpleIO) libraries are embedded by default, so there's no need to add them to the _lib_ folder of the _CIRCUITPY_ drive manually.

Follow [this guide](/setup-circuitpython.md) to load the CircuitPython firmware on your Maker Nano RP2040.
If you see _CIRCUITPY_ drive appears on your computer, it means CircuitPython firmware is already loaded on board and you are good to go! 

The _code.py_ file on the _CIRCUITPY_ drive (of any new Maker Nano RP2040) is the demo program which comes with the board. You can open this file with any code editor to view or modify it. [Mu Editor](https://codewith.mu/) is highly recommended for coding the CircuitPython. Follow [Adafruit's guide](https://learn.adafruit.com/welcome-to-circuitpython/installing-mu-editor) to install the software.

Besides modifying the demo program, you can also open one of the [CircuitPython examples here](/Examples/CircuitPython). You can copy the code and paste it in the _code.py_ file on your _CIRCUITPY_ drive. Save the file after making desired changes and the code will run as soon as the file is done saving.
> Please wait until the file is successfully saved before resetting or unplugging your board!


### MicroPython

Follow [this guide](https://www.raspberrypi.com/documentation/microcontrollers/micropython.html) to load the MicroPython firmware on your Maker Nano RP2040.
