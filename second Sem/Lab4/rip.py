import socket
import threading
import time
import json

# Constants
UPDATE_INTERVAL = 10  # Time interval (seconds) between routing updates


class Router:
    def __init__(self, router_id, neighbors, interface_type="wired"):
        self.router_id = router_id
        self.neighbors = neighbors  # Dictionary {neighbor_id: cost}
        self.routing_table = {neighbor: cost for neighbor, cost in neighbors.items()}
        self.interface_type = interface_type
        self.lock = threading.Lock()

    def send_routing_update(self):
        """Periodically sends routing updates to neighbors."""
        while True:
            time.sleep(UPDATE_INTERVAL)
            update_packet = json.dumps(
                {"router_id": self.router_id, "routing_table": self.routing_table}
            )
            for neighbor in self.neighbors:
                self.send_update(neighbor, update_packet)

    def send_update(self, neighbor, update_packet):
        """Simulates sending an update to a neighboring router."""
        print(
            f"Router {self.router_id} sending update to Router {neighbor}: {update_packet}"
        )

        # Simulate wireless delay
        if self.interface_type == "wireless":
            time.sleep(1)  # Add network delay for wireless routers

    def receive_routing_update(self, update_packet):
        """Receives and processes a routing update from a neighbor."""
        with self.lock:
            update = json.loads(update_packet)
            sender_id = update["router_id"]
            received_table = update["routing_table"]
            print(
                f"Router {self.router_id} received update from Router {sender_id}: {received_table}"
            )
            self.update_routing_table(sender_id, received_table)

    def update_routing_table(self, sender_id, received_table):
        """Updates the routing table based on a received update."""
        updated = False
        for dest, cost in received_table.items():
            new_cost = self.neighbors[sender_id] + cost
            if dest not in self.routing_table or new_cost < self.routing_table[dest]:
                self.routing_table[dest] = new_cost
                updated = True

        if updated:
            print(
                f"Router {self.router_id} updated routing table: {self.routing_table}"
            )

    def print_routing_table(self):
        """Prints the current routing table for the router."""
        print(f"Router {self.router_id} ({self.interface_type}):")
        print(f"{'Destination':<15} {'Cost':<10}")
        for neighbor, cost in self.routing_table.items():
            print(f"{neighbor:<15} {cost:<10}")
        print("-" * 30)


def network_simulation():
    """Sets up the network topology and starts the simulation."""
    # Define routers with their neighbors and link costs
    router1 = Router(1, {2: 1, 3: 4}, "wired")
    router2 = Router(2, {1: 1, 3: 2}, "wireless")
    router3 = Router(3, {1: 4, 2: 2}, "wired")

    routers = [router1, router2, router3]

    # Print initial routing tables
    print("Initial Configuration:")
    print("=" * 30)
    for router in routers:
        router.print_routing_table()

    # Start routing updates in background threads
    threading.Thread(target=router1.send_routing_update, daemon=True).start()
    threading.Thread(target=router2.send_routing_update, daemon=True).start()
    threading.Thread(target=router3.send_routing_update, daemon=True).start()

    # Simulate manual routing update receptions (as if from network events)
    time.sleep(2)  # Wait for initial setup
    router2.receive_routing_update(
        json.dumps({"router_id": 1, "routing_table": {2: 1, 3: 4}})
    )
    router3.receive_routing_update(
        json.dumps({"router_id": 2, "routing_table": {1: 1, 3: 2}})
    )


if __name__ == "__main__":
    network_simulation()
