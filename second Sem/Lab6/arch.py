import socket
import threading


# Tier-I (Client) - Sends requests to the application server
def client_request(request):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect(("localhost", 5002))
        client.send(request.encode())
        response = client.recv(1024).decode()
        print(f"Client received: {response}")


# Tier-II (Application Server) - Acts as an intermediary between
#  the client and the database server
def tier2_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind(("localhost", 5002))
        server.listen(5)
        print("Tier-II (Application Server) is running...")

        while True:
            conn, _ = server.accept()
            with conn:
                data = conn.recv(1024).decode()
                print(f"Tier-II received: {data}")

                # Forward request to Tier-III (Database Server)
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tier3:
                    tier3.connect(("localhost", 5003))
                    tier3.send(data.encode())
                    response = tier3.recv(1024).decode()

                # Send back the response to the client
                conn.send(response.encode())


# Tier-III (Database Server) - Responsible for handling database requests
def tier3_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind(("localhost", 5003))
        server.listen(5)
        print("Tier-III (Database Server) is running...")

        while True:
            conn, _ = server.accept()
            with conn:
                data = conn.recv(1024).decode()
                print(f"Tier-III received: {data}")
                response = f"Data processed for {data}"
                # Simulate database processing
                conn.send(response.encode())


# Start Tier-II and Tier-III servers in separate threads
threading.Thread(target=tier3_server, daemon=True).start()
threading.Thread(target=tier2_server, daemon=True).start()

# Simulate a client request
print("Client made a request - Fetch Order #123")
threading.Thread(target=client_request, args=("Fetch Order #123",)).start()
