# Controlling Nanoleaf Shapes using a Raspberry PI
Nanoleaf shapes are light panels that connects with your local network. This is a project I did during my free time in February. These lights are controlled using their app, however for this project I used the Nanoleaf API to make it work together with my Raspberry Pi.

## Hardware requirements
* Nanoleafs shapes
* Raspbery Pi
* 3 Push buttons
* 1 Potentiometers 
* 3 1K Ohm resistor
* 1 MCP3008
* Jumper cables
* Breadboard

## Software requirements
* Python 3.7
* Python 3 Development toolkit (install python3-dev python3-setuptools)
* RPi.GPIO (install python3-rpi.gpio)
* Enable spi in /boot/config.txt (https://www.raspberrypi.org/documentation/hardware/raspberrypi/spi/README.md)

## Nanoleaf Open API
The link the Nanoleaf API is: https://forum.nanoleaf.me/docs#_y93gn2m7n534

The API is a REST API which means the protocol HTTP is used.

## Setup 
This is how the setup looks like:
<br>

I will discuss each piece of the important hardware seperatly to make it more clear.

### Push buttons
The push buttons will be used for the following:
* Turning the lights on and off
* Go to the next color
* GO back to the previous color

Resistors are needed here because otherwise the Raspberry Pi will short circuit.

### Potentiometer + MCP3008
With an MCP3008 it is possible to convert a DC voltage (between 0 and -3.3V) to a digital reading (between 0 and 1023).
A potentiometer is a resistor that acts as an adjustable voltage divider. Because the voltage will be adjustable, we can easily use it as a brightness changer. If the voltage gets higher, the light gets brighter.

## Result

Here you can find the video of the result:

## Code
The code that is used can be found in this repository.


