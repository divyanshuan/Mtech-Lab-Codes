class LogicalClock:
    def __init__(self, process_id):
        self.process_id = process_id
        self.time = 0

    def tick(self):
        """Increment the logical clock."""
        self.time += 1

    def send_event(self):
        """Simulate sending an event from this process."""
        self.tick()
        print(f"Process {self.process_id} sends an event at time {self.time}")
        return self.time

    def receive_event(self, received_time):
        """Simulate receiving an event at this process."""
        self.tick()
        self.time = max(self.time, received_time) + 1
        print(f"Process {self.process_id} receives an event at time {self.time}")
        return self.time


def is_consistent_cut(events, cut):
    """
    Check if a given cut is consistent.

    A cut is consistent if for every received event included in the cut,
    its corresponding send event is also included in the cut.

    Args:
    - events: List of tuples (send_time, receive_time, receiving_process)
    - cut: List of logical timestamps for the cut

    Returns:
    - True if the cut is consistent, False otherwise.
    """
    for send_time, recv_time, _ in events:
        # If the receive event is in the cut, check if its corresponding send event is also in the cut
        if recv_time in cut and send_time not in cut:
            return False
    return True


def simulate_events():
    """Simulate the processes and the events between them."""
    p1 = LogicalClock(1)
    p2 = LogicalClock(2)

    events = []  # Store events as (send_time, receive_time, receiving_process)

    # Simulate some events
    p1.tick()
    p2.tick()
    sent_time = p1.send_event()
    received_time = p2.receive_event(sent_time)
    events.append((sent_time, received_time, 2))

    p1.tick()
    p2.tick()
    sent_time = p2.send_event()
    received_time = p1.receive_event(sent_time)
    events.append((sent_time, received_time, 1))

    return events


def main():
    events = simulate_events()

    # Display all events
    print("\nEvent log (send_time, receive_time, receiving_process):")
    for event in events:
        print(event)

    # Get a cut from the user
    cut = list(
        map(
            int,
            input("\nEnter the cut as space-separated logical timestamps: ").split(),
        )
    )

    # Check if the cut is consistent
    is_consistent = is_consistent_cut(events, cut)
    print(f"\nIs the cut consistent? {'Yes' if is_consistent else 'No'}")


if __name__ == "__main__":
    main()
