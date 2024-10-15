import socket
import threading

def handle_client(client_socket):
    with open("received_file.txt", 'wb') as file:
        while True:
            data = client_socket.recv(4096)
            if not data:
                break
            file.write(data)
    client_socket.close()

def start_server(ip_version, address, port):
    family = socket.AF_INET if ip_version == 'IPv4' else socket.AF_INET6
    server_socket = socket.socket(family, socket.SOCK_STREAM)
    server_socket.bind((address, port))
    server_socket.listen(5)
    print(f"Server listening on {address}:{port} ({ip_version})")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Accepted connection from {addr}")
        threading.Thread(target=handle_client, args=(client_socket,)).start()

# Start the server for both IPv4 and IPv6 using localhost
threading.Thread(target=start_server, args=('IPv4', '127.0.0.1', 12345)).start()
threading.Thread(target=start_server, args=('IPv6', '::1', 12345)).start()
