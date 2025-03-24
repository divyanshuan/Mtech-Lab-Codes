import socket

def get_localhost_ip():
    """Returns the IP address of the localhost."""
    hostname = socket.gethostname()
    return socket.gethostbyname(hostname)

def start_server(server_ip, server_port):
    """Starts the server and handles client connections."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Set SO_REUSEADDR to reuse the port if needed
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        # Bind to the localhost IP and port
        server_socket.bind((server_ip, server_port))
        server_socket.listen(1)
        print(f"Server: Listening on {server_ip}:{server_port}\n")

        print("Server: Waiting for a client connection...\n")
        connection, client_address = server_socket.accept()
        print(f"Server: Connection established with {client_address}\n")

        while True:
            # Receiving data from the client
            data = connection.recv(1024)
            if not data:
                break
            print(f"Received from client: {data.decode()}")

            # Sending acknowledgment back to the client
            response = input("Enter message for client: ")
            connection.sendall(response.encode())

    except KeyboardInterrupt:
        print("\nServer: Closing connection.")
    except OSError as err:
        print(f"Server error: {err}")
    finally:
        if 'connection' in locals() and connection is not None:
            connection.close()
        server_socket.close()

if __name__ == "__main__":
    SERVER_IP = get_localhost_ip()
    SERVER_PORT = 3000
    start_server(SERVER_IP, SERVER_PORT)