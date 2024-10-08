import socket


def send_file(server_ip, port, filename):
    # Try to resolve both IPv4 and IPv6 addresses
    addr_info = socket.getaddrinfo(
        server_ip, port, socket.AF_UNSPEC, socket.SOCK_STREAM
    )

    # Select the first valid address (IPv4 or IPv6)
    for res in addr_info:
        af, socktype, proto, canonname, sa = res
        try:
            client_socket = socket.socket(af, socktype, proto)
            client_socket.connect(sa)
            break
        except socket.error:
            client_socket = None
            continue

    if client_socket is None:
        print("Failed to connect to the server.")
        return

    # Open the file to read
    with open(filename, "rb") as f:
        while True:
            # Read file data in chunks
            data = f.read(1024)
            if not data:
                break
            # Send the data
            client_socket.sendall(data)
            print("Sending...")

    print(f"File '{filename}' sent successfully.")

    # Close the socket
    client_socket.close()


# Example usage
server_ip = (
    "127.0.0.1"  # Can be an IPv4 (e.g., '127.0.0.1') or IPv6 address (e.g., '::1')
)
port = 12345
filename = "test.txt"
send_file(server_ip, port, filename)
