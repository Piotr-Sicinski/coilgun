from simple_pid import PID
import socket
import struct
from time import sleep, time
from math import sin


def init_socket() -> socket.socket:
    # Konfiguracja klienta
    host = '10.42.0.4'  # Adres urządzenia
    # host = '192.168.137.3'
    port = 2345

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    return client_socket


def process_run_test_print(conn):
    while True:
        xy = conn.recv()
        if xy:
            print(xy)
        else:
            print("none")


def process_run_turret(conn):
    client_socket = init_socket()

    def_data = (0, 0)

    while True:
        xy = conn.recv()  # tuple (x,y)
        if xy == None:
            xy = def_data

        message = struct.pack('!hh', *xy)
        client_socket.send(message)

    client_socket.close()


def process_run_degree_table(conn):
    client_socket = init_socket()
    def_data = (0, 0)

    loop_duration = 7.5  # 10 seconds
    start_time = time()

    while time() - start_time < loop_duration:
        xy = conn.recv()  # tuple (x,y)
        if xy == None:
            xy = def_data

        message = struct.pack('!hh', *xy)
        client_socket.send(message)

        data_bytes = client_socket.recv(1024)
        if not data_bytes:
            break

        x_deg, y_deg = struct.unpack('!hh', data_bytes)

    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    client_socket.close()
