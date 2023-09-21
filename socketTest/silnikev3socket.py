#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor
from pybricks.iodevices import DCMotor, UARTDevice
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
import socket
from time import sleep

ev3 = EV3Brick()
obrMotor = Motor(Port.C)
nachMotor = Motor(Port.D)
timer = StopWatch()

obrMotor.track_target(15)
sleep(1)
obrMotor.track_target(0)

host = '0.0.0.0'
port = 2345

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(1)

print("Oczekiwanie na polaczenie na {}:{}".format(host, port))

client_socket, client_address = server_socket.accept()
print("Polaczono z {}".format(client_address))

while True:
    data = client_socket.recv(1024).decode('utf-8')
    if not data:
        break

    print("Otrzymano: {}".format(data))

client_socket.close()
server_socket.close()
