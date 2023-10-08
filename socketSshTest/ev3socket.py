import socket

host = '0.0.0.0'
port = 2345

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(1)

print("Oczekiwanie na polaczenie na {}:{}".format(host, port))

client_socket, client_address = server_socket.accept()
print("Polaczono z {}".format(client_address))

while True:
    data = client_socket.recv(1024).decode('utf-8')
    if not data:
        break

    print("Otrzymano: {}".format(data))

    response = input("Odpowiedz: ")
    client_socket.send(response.encode('utf-8'))

client_socket.close()
server_socket.close()
