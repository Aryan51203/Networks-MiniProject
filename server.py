import socket


def receive_file(port, filename):
    # Create a dual-stack socket (AF_INET6) for both IPv6 and IPv4
    server_socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)

    # Allow both IPv4 and IPv6 connections
    server_socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)

    # Bind to the IPv6 wildcard address (which also handles IPv4)
    server_socket.bind(("::", port))

    # Start listening for incoming connections
    server_socket.listen(1)
    print(f"Server listening on port {port} (IPv4 and IPv6)")

    # Accept incoming client connections
    client_socket, addr = server_socket.accept()
    print(f"Connected to {addr}")

    # Open a file to write the received data
    with open(filename, "wb") as f:
        while True:
            # Receive data in chunks
            data = client_socket.recv(1024)
            if not data:
                break
            f.write(data)
            print("Receiving...")

    print(f"File '{filename}' received successfully.")

    # Close connections
    client_socket.close()
    server_socket.close()


# Example usage
port = 12345
filename = "received_file.txt"
receive_file(port, filename)
