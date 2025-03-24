import socket


def start_server(host="127.0.0.1", port=65432):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen(5)
        print(f"Server listening on {host}:{port}")

        while True:
            conn, addr = server_socket.accept()
            with conn:
                print(f"Connected by {addr}")
                data = conn.recv(1024).decode()
                if not data:
                    break
                print(f"Received: {data}")
                response = f"Echo: {input('Enter reply from server: ')}"
                conn.sendall(response.encode())


if __name__ == "__main__":
    start_server()
