import socket
from time import time, sleep
# Konfiguracja klienta
host = '10.42.0.4'  # Adres urządzenia
port = 2345  # Ten sam port co na urządzeniu

# Utwórz gniazdo klienta
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))

# Wysyłaj dane do urządzenia i odbieraj odpowiedzi
i = 0
start = time()
message = "ls"
while True:
    i += 1
    client_socket.send(message.encode('utf-8'))  # Wyślij wiadomość do urządzenia
    sleep(0.05)

    if i == 100:
        end = time()
        print("msg/s: {:.1f}".format(100/(end - start)))
        start = end
        i = 0

# Zamknij połączenie
client_socket.close()
