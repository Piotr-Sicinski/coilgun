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

    def set_to_xy(dest_x, dest_y):
        start_time = time()
        x_deg, y_deg = None, None
        while time() - start_time < 7.5:
            xy = conn.recv()  # tuple (x,y)
            if xy == None:
                xy = DEF_DATA
            else:
                xy = xy[0] - dest_x, xy[1] - dest_y

            message = struct.pack('!hh', *xy)
            client_socket.send(message)

            data_bytes = client_socket.recv(1024)
            x_deg, y_deg = struct.unpack('!hh', data_bytes)

        print("Finished centering")
        return x_deg, y_deg

    print("Begin")
    client_socket = init_socket()

    CAM_WIDTH = 640
    CAM_HEIGHT = 480

    DIRECTIONS = [(1, 0), (0, 1)]
    DEF_DATA = (0, 0)
    SLOW_SPEED = 20
    PRC = 0.75

    width_tab = [None] * int(PRC * CAM_WIDTH / 2)
    height_tab = [None] * int(PRC * CAM_HEIGHT / 2)

    print("X")
    xy = True

    for x_enable, y_enable in DIRECTIONS:
        ref_x, ref_y = set_to_xy(0, 0)
        set_to_xy(len(width_tab) * x_enable, len(height_tab) * y_enable)

        while True:
            xy = conn.recv()  # tuple (x,y)
            if xy == None:
                xy = DEF_DATA
            x, y = xy

            fake_xy = SLOW_SPEED * x_enable, SLOW_SPEED * y_enable

            message = struct.pack('!hh', *fake_xy)
            client_socket.send(message)

            data_bytes = client_socket.recv(1024)
            x_deg, y_deg = struct.unpack('!hh', data_bytes)

            if x * x_enable < 0 or y * y_enable < 0:
                print(x, y)
                print("Y")
                break

            if x_enable and len(width_tab) > x:
                print(f"{x} -> {x_deg - ref_x}")
                if not width_tab[x]:
                    width_tab[x] = x_deg - ref_x

            if y_enable and len(height_tab) > y:
                print(f"{y} -> {y_deg - ref_y}")
                if not height_tab[y]:
                    height_tab[y] = y_deg - ref_y

    client_socket.close()

    print("Saving...")
    with open("degre_table.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(width_tab)
        writer.writerow(height_tab)
