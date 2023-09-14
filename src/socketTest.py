import socket

# Konfiguracja klienta
host = '169.254.233.12'  # Adres urządzenia
port = 2345  # Ten sam port co na urządzeniu

# Utwórz gniazdo klienta
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))

# Wysyłaj dane do urządzenia i odbieraj odpowiedzi
while True:
    message = input("Wiadomość: ")  # Pobierz wiadomość od użytkownika
    client_socket.send(message.encode('utf-8'))  # Wyślij wiadomość do urządzenia

    response = client_socket.recv(1024).decode('utf-8')
    print(f"Odpowiedź z urządzenia: {response}")

# Zamknij połączenie
client_socket.close()

# import socket


# host = '0.0.0.0'
# port = 2345


# server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server_socket.bind((host, port))
# server_socket.listen(1)

# print(f"Oczekiwanie na polaczenie na {host}:{port}")


# client_socket, client_address = server_socket.accept()
# print(f"Polaczono z {client_address}")


# while True:
#     data = client_socket.recv(1024).decode('utf-8')
#     if not data:
#         break

#     print(f"Otrzymano: {data}")

#     response = input("Odpowiedz: ")
#     client_socket.send(response.encode('utf-8'))


# client_socket.close()
# server_socket.close()
