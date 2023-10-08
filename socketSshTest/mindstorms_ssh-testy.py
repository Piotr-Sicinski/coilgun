import paramiko
from time import sleep, time


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
