import paramiko
from simple_pid import PID
import socket
import struct
from time import sleep
from math import sin


def process_run_test_print(conn):
    while True:
        xy = conn.recv()
        if xy:
            print(xy)
        else:
            print("none")


def mindstorms_ssh_process_run_turret(conn):
    # Konfiguracja klienta
    host = '10.42.0.4'  # Adres urządzenia
    # host = '192.168.137.3'
    port = 2345

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    def_data = (0, 0)

    while True:
        xy = conn.recv()  # tuple (x,y)
        if xy == None:
            xy = def_data

        message = struct.pack('!hh', *xy)
        client_socket.send(message)

        # sleep(STEP)

    client_socket.close()


def testSSHSpeed1(ssh_client):
    start_time = time()

    N = 100
    for _ in range(N):
        stdin, stdout, stderr = ssh_client.exec_command('ls')

    execution_time = time() - start_time

    print(f"Czas wykonywania: {execution_time/N} sekundy")


def testSSHSpeed2(ssh_client):
    # Otwarcie sesji SSH
    ssh_session = ssh_client.invoke_shell()

    # Wysłanie poleceń
    commands = ['ls', 'pwd', 'echo "Hello, World!"']
    for cmd in commands:
        ssh_session.send(cmd + '\n')

    # Odczytanie wyników
    output = ''
    while True:
        if ssh_session.recv_ready():
            output += ssh_session.recv(1024).decode('utf-8')
        else:
            break

    # Wyświetlenie wyników
    print(output)

    # Zamknięcie sesji SSH
    ssh_session.close()


def main():
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect('ev3dev', port=22, username='robot', password='maker')
    # ssh_client.connect('10.42.0.4', port=22, username='robot', password='maker')

    # Wykonanie poleceń zdalnych
    stdin, stdout, stderr = ssh_client.exec_command('ls')
    print(stdout.read().decode())

    # Zamknięcie połączenia SSH
    ssh_client.close()


if __name__ == "__main__":
    main()
