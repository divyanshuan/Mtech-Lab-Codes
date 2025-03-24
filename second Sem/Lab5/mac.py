import random
import time


class Network:
    def __init__(self, num_nodes, protocol):
        self.num_nodes = num_nodes
        self.medium_busy = False
        self.protocol = protocol

    def transmit(self, node_id):
        print(f"Node {node_id} is attempting to transmit.")
        if self.medium_busy:
            if self.protocol == "CSMA/CD":
                self.handle_collision(node_id)
            else:  # CSMA/CA
                print(f"Medium busy! Node {node_id} is waiting.")
                time.sleep(random.randint(1, 3))
                self.transmit(node_id)  # Retry
        else:
            self.medium_busy = True
            if self.protocol == "CSMA/CD":
                self.csma_cd_transmit(node_id)
            else:  # CSMA/CA
                self.csma_ca_transmit(node_id)

    def handle_collision(self, node_id):
        print(f"Collision detected! Node {node_id} is backing off.")
        backoff_time = random.randint(1, 5)
        time.sleep(backoff_time)
        print(f"Node {node_id} retrying after {backoff_time} seconds.")
        self.transmit(node_id)  # Retry after backoff

    def csma_cd_transmit(self, node_id):
        print(f"Node {node_id} is transmitting (CSMA/CD)...")
        time.sleep(2)
        print(f"Node {node_id} completed transmission.")
        self.medium_busy = False

    def csma_ca_transmit(self, node_id):
        print(f"Node {node_id} is waiting for ACK (CSMA/CA)...")
        time.sleep(2)
        print(f"Node {node_id} completed transmission with ACK.")
        self.medium_busy = False


# Simulate the MAC protocols
wired_network = Network(num_nodes=5, protocol="CSMA/CD")
wireless_network = Network(num_nodes=5, protocol="CSMA/CA")

print("Simulation in Wired Network (CSMA/CD)")
for _ in range(3):
    node_id = random.randint(1, 5)
    wired_network.transmit(node_id)
    time.sleep(1)

print("\nSimulation in Wireless Network (CSMA/CA)")
for _ in range(3):
    node_id = random.randint(1, 5)
    wireless_network.transmit(node_id)
    time.sleep(1)
