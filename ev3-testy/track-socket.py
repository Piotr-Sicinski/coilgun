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

host = '0.0.0.0'
port = 23451

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(1)
print("Oczekiwanie na polaczenie na {}:{}".format(host, port))

client_socket, client_address = server_socket.accept()
print("Polaczono z {}".format(client_address))

while True:
    data_bytes = client_socket.recv(1024)
    if not data_bytes:
        break

    x, y = struct.unpack('!hh', data_bytes)

    # obrMotor1.track_target(x)
    # obrMotor2.track_target(x)
    # nachMotor.track_target(x)
    # obrMotor1.run_angle(500, x, wait=False)
    # obrMotor2.run_angle(500, x, wait=False)
    # nachMotor.run_angle(500, -y, wait=False)

    # obrMotor1.run(1.5*x)
    # obrMotor2.run(1.5*x)
    # nachMotor.run(-1.5*y)

    obrMotor1.run(x)
    obrMotor2.run(x)
    nachMotor.run(-y)

    # print(nachMotor.angle())

obrMotor1.stop()
obrMotor2.stop()
nachMotor.stop()

client_socket.close()
server_socket.close()
