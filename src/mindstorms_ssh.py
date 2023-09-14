import paramiko
import time
from simple_pid import PID


def process_run_test_print(conn):
    while True:
        xy = conn.recv()
        if xy:
            print(xy)
        else:
            print("none")


def testSSHSpeed1(ssh_client):
    start_time = time.time()

    N = 100
    for _ in range(N):
        stdin, stdout, stderr = ssh_client.exec_command('ls')

    execution_time = time.time() - start_time

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

    # Wykonanie poleceń zdalnych
    # stdin, stdout, stderr = ssh_client.exec_command('ls')
    # print(stdout.read().decode())

    # testSSHSpeed2(ssh_client)

    # Otwarcie sesji SSH
    ssh_session = ssh_client.invoke_shell()
    time.sleep(2)
    ssh_session.recv(1024).decode('utf-8')

    # Wysłanie poleceń
    commands = ['ls', 'pwd', 'echo "Hello, World!"']
    output = ''
    c = 0
    for cmd in commands:
        ssh_session.send(cmd + '\n')
        time.sleep(0.1)
        while True:
            if ssh_session.recv_ready():
                c += 1
                response = ssh_session.recv(1024).decode('utf-8')
                output += response
                if cmd in response:
                    break

    # Wyświetlenie wyników (bez znaku zachęty)
    print(output.strip(), c)

    # Zamknięcie sesji SSH
    ssh_session.close()

    # Zamknięcie połączenia SSH
    ssh_client.close()


if __name__ == "__main__":
    main()
