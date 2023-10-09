#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor
from pybricks.iodevices import DCMotor, UARTDevice
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog

from time import sleep
from math import sin

ev3 = EV3Brick()
obrMotor = Motor(Port.D)

STEP = 0.05
deg = 0

while True:
    deg += STEP
    obrMotor.track_target(180 * sin(deg))
    # obrMotor.run_target(1000, 60 * sin(deg), wait=False)
    sleep(STEP)

sleep(1)
obrMotor.track_target(0)
