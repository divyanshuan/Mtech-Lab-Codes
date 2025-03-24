import socket

def get_localhost_ip():
    """Returns the IP address of the localhost."""
    hostname = socket.gethostname()
    return socket.gethostbyname(hostname)

def connect_to_server(server_ip, server_port):
    """Connects to the server and handles sending/receiving messages."""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to the server
        client_socket.connect((server_ip, server_port))
        print(f"Client: Connected to server at {server_ip}:{server_port}")
    except socket.error as err:
        print(f"Client: Connection failed - {err}")
        return

    try:
        print("Client: Press Ctrl + C to close the connection.\n")
        
        while True:
            # Sending data to the server
            message = input("Enter message for server: ")
            client_socket.sendall(message.encode())

            # Receiving response from the server
            response = client_socket.recv(1024)
            print(f"Received from server: {response.decode()}\n")

    except KeyboardInterrupt:
        print("\nClient: Closing connection.")
    finally:
        client_socket.close()

if __name__ == "__main__":
    SERVER_IP = get_localhost_ip()
    SERVER_PORT = 3000
    connect_to_server(SERVER_IP, SERVER_PORT)