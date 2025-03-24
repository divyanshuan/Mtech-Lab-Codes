import heapq
class Network:
    def __init__(self, is_wireless=False):
        self.nodes = {}
        self.is_wireless = is_wireless

    def add_link(self, node1, node2, cost):
        """Add a bidirectional link between two nodes with the given cost."""
        if node1 not in self.nodes:
            self.nodes[node1] = {}
        if node2 not in self.nodes:
            self.nodes[node2] = {}
        self.nodes[node1][node2] = cost
        self.nodes[node2][node1] = cost  # Assuming bidirectional link

    def dijkstra(self, start, end):
        heap = [(0, start)]
        distances = {node: float("inf") for node in self.nodes}
        distances[start] = 0
        previous_nodes = {node: None for node in self.nodes}

        while heap:
            current_distance, current_node = heapq.heappop(heap)
            if current_node == end:
                break

            for neighbor, weight in self.nodes[current_node].items():
                distance = current_distance + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous_nodes[neighbor] = current_node
                    heapq.heappush(heap, (distance, neighbor))

        path, current = [], end
        while previous_nodes[current] is not None:
            path.insert(0, current)
            current = previous_nodes[current]
        if path:
            path.insert(0, start)
        return path, distances[end]

    def print_network(self):
        """Print the network topology showing all links and costs."""
        print(f"{'Wireless' if self.is_wireless else 'Wired'} Network Topology:")
        for node, links in self.nodes.items():
            for neighbor, cost in links.items():
                print(f"{node} --({cost})--> {neighbor}")
        print()

    def simulate(self, start, end):
        """Simulate routing from start to end in the network."""
        self.print_network()
        path, cost = self.dijkstra(start, end)
        print(
            f"Routing {'wireless' if self.is_wireless else 'wired'} network from {start} to {end}"
        )
        print(f"Path: {' -> '.join(path) if path else 'No path found'}")
        print(f"Total cost: {cost}")


# Example Simulation for Wired and Wireless Networks

# Wired Network Simulation
wired_network = Network(is_wireless=False)
wired_network.add_link("A", "B", 1)
wired_network.add_link("B", "C", 2)
wired_network.add_link("A", "D", 4)
wired_network.add_link("D", "C", 1)
wired_network.simulate("A", "C")

# Wireless Network Simulation
wireless_network = Network(is_wireless=True)
wireless_network.add_link("X", "Y", 3)
wireless_network.add_link("Y", "Z", 1)
wireless_network.add_link("X", "Z", 5)
wireless_network.simulate("X", "Z")
