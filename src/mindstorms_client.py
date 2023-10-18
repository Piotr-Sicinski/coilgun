from typing import Tuple, Optional
from multiprocessing.connection import Connection
from simple_pid import PID
import socket
import struct
from time import sleep, time
from math import sin
import csv


def init_socket() -> socket.socket:
    host = '10.42.0.4'  # Adres urządzenia
    port = 23451

    RECONN_NO = 5
    RECONN_DELAY = 3

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    for i in range(RECONN_NO):
        try:
            client_socket.connect((host, port))
        except ConnectionRefusedError:
            print(f"Host not ready. {i+1}/{RECONN_NO}Reconnecting...")
            sleep(RECONN_DELAY)
        else:
            print(f"Connected to {host}:{port}")
            return client_socket

    raise ConnectionError("Failed to connect after multiple retries")


def sendIntTuple(soc: socket.socket, data: Tuple[int, int], cmd=0):
    message = struct.pack('!hh', *data)
    soc.send(message)


def process_run_test_print(conn: Connection):
    while True:
        xy = conn.recv()
        if xy:
            print(xy)
        else:
            print("none")


def process_run_turret(conn: Connection):
    client_socket = init_socket()

    while True:
        xy = conn.recv()  # tuple (x,y)
        if not xy:
            break
        if xy == (None, None):
            xy = 0, 0

        sendIntTuple(client_socket, xy)

    client_socket.close()


def process_run_pid(conn: Connection):
    client_socket = init_socket()

    p = -1
    i = -0.5
    d = 0
    pid = PID(p, i, d, setpoint=0)

    while True:
        xy = conn.recv()  # tuple (x,y)
        if not xy:
            break

        if xy == (None, None):
            xy = 0, 0
        else:
            control = pid(xy[1])
            xy = 0, (round(control) if control else 0)

        sendIntTuple(client_socket, xy)

    client_socket.close()


def test_slow_movement():
    client_socket = init_socket()

    x, y = 0, 0

    SLEEP_TIME = 0.5

    while True:
        try:

            user_input = input("Enter an X speed (or press 'q' to quit): ")
            if user_input.lower() == 'q':
                break  # Exit the loop if the user enters 'exit'

            x = int(user_input) if user_input else x

            user_input = input("Enter an Y speed: ")
            y = int(user_input) if user_input else y

            sendIntTuple(client_socket, (x, y))
            sleep(SLEEP_TIME)
            sendIntTuple(client_socket, (-x, -y))
            sleep(SLEEP_TIME)
            sendIntTuple(client_socket, (0, 0))

        except ValueError:
            print("Invalid input. Please enter a valid integer.")

    client_socket.close()


def process_run_degree_table(conn: Connection):

    def set_to_xy(dest_x, dest_y):
        start_time = time()
        x_deg, y_deg = None, None
        while time() - start_time < 7.5:
            xy = conn.recv()  # tuple (x,y)
            if xy == None:
                xy = DEF_DATA
            else:
                xy = xy[0] - dest_x, xy[1] - dest_y

            sendIntTuple(client_socket, xy)

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

            sendIntTuple(client_socket, xy)

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


if __name__ == "__main__":
    test_slow_movement()
