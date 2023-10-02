import socket
import struct
from time import sleep
from math import sin


# Konfiguracja klienta
host = '10.42.0.4'  # Adres urządzenia
# host = '192.168.137.3'
port = 2345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))

STEP = 0.03
deg = 0

while True:
    deg += STEP
    data_to_send = (int(180 * sin(deg)), 0)

    message = struct.pack('!hh', *data_to_send)
    client_socket.send(message)

    sleep(STEP)

client_socket.close()
