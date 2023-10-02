import socket
import json
from time import sleep

# Konfiguracja klienta
host = '10.42.0.4'  # Adres urządzenia
# host = '192.168.137.3'
port = 2345  # Ten sam port co na urządzeniu

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))

while True:
    message = json.dumps((1, 2))
    client_socket.send(message.encode('utf-8'))
    sleep(2)

client_socket.close()
