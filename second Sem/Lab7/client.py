import socket


def send_message(message, host="127.0.0.1", port=65432):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        client_socket.sendall(message.encode())
        response = client_socket.recv(1024).decode()
        print(f"Server Response: {response}")


if __name__ == "__main__":
    print("Client Machine started. Press Ctrl+C to exit")
    while True:
        try:
            message = input("Enter message: ")
            send_message(message)
        except KeyboardInterrupt:
            print("\nClient exited.")
            break
