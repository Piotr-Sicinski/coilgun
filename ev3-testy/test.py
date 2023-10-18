#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor
from pybricks.iodevices import DCMotor, UARTDevice
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog

from time import sleep
import socket
import struct

obrMotor1 = Motor(Port.A)
obrMotor2 = Motor(Port.D)
nachMotor = Motor(Port.B)

# print(nachMotor.settings())
print(nachMotor.control)
