from simple_pid import PID
import socket
import struct
from time import sleep, time
from math import sin
import csv


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

    def recenter():
        loop_duration = 7.5  # 10 seconds
        start_time = time()
        x_deg, y_deg = None, None
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

        print("Finished centering")
        return x_deg, y_deg

    print("Begin")
    client_socket = init_socket()

    def_data = (0, 0)

    cam_width = 640
    cam_height = 480

    slow_speed = 20
    prc = 0.75

    width_tab = [None] * int(prc * cam_width / 2)
    height_tab = [None] * int(prc * cam_height / 2)

    dirs = [(1, 0), (0, 1)]

    print("X")

    xy = True

    for x_mov, y_mov in dirs:
        ref_x, ref_y = recenter()

        while True:
            xy = conn.recv()  # tuple (x,y)
            if xy == None:
                xy = def_data
            x, y = xy

            fake_xy = slow_speed * x_mov, -slow_speed * y_mov

            message = struct.pack('!hh', *fake_xy)
            client_socket.send(message)

            data_bytes = client_socket.recv(1024)
            if not data_bytes:
                break

            x_deg, y_deg = struct.unpack('!hh', data_bytes)

            if x >= prc * cam_width / 2 or y >= prc * cam_height / 2:
                print("Y")
                break

            if x_mov:
                width_tab[x] = x_deg - ref_x

            if y_mov:
                height_tab[y] = y_deg - ref_y

    client_socket.close()

    print("Saving...")
    with open("degre_table.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(width_tab)
        writer.writerow(height_tab)
