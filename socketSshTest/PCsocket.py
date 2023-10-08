import socket

# Konfiguracja klienta
host = '10.42.0.4'  # Adres urządzenia
# host = '192.168.137.3'
port = 2345  # Ten sam port co na urządzeniu

# Utwórz gniazdo klienta
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))

# Wysyłaj dane do urządzenia i odbieraj odpowiedzi
while True:
    message = input("Wiadomość: ")  # Pobierz wiadomość od użytkownika
    # Wyślij wiadomość do urządzenia
    client_socket.send(message.encode('utf-8'))

    # response = client_socket.recv(1024).decode('utf-8')
    # print(f"Odpowiedź z urządzenia: {response}")

# Zamknij połączenie
client_socket.close()
