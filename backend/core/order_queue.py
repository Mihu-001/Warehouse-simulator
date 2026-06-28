import heapq

class OrderQueue:
    def __init__(self):
        # Items in queue are tuples: (priority, counter, order_id)
        # priority: 1 for TC (High), 2 for DRY (Normal)
        self.pending_queue = []
        self.order_counter = 0
        self.orders = {}  # order_id -> dict

    def push(self, rack_id, sku, zone):
        """
        Pushes a new order onto the queue.
        TC zone is prioritized (priority 1) over DRY zone (priority 2).
        """
        self.order_counter += 1
        order_id = f"ORD-{self.order_counter:04d}"
        priority = 1 if zone == "TC" else 2
        
        order = {
            "id": order_id,
            "rack_id": rack_id,
            "sku": sku,
            "zone": zone,
            "status": "PENDING",
            "robot": None,
            "priority_label": "HIGH (TC)" if priority == 1 else "NORMAL (DRY)"
        }
        
        self.orders[order_id] = order
        heapq.heappush(self.pending_queue, (priority, self.order_counter, order_id))
        return order_id

    def pop_next(self):
        """
        Pops the next highest priority order from the queue.
        """
        while self.pending_queue:
            priority, counter, order_id = heapq.heappop(self.pending_queue)
            # Ensure it hasn't been cancelled or modified in the meantime
            if order_id in self.orders and self.orders[order_id]["status"] == "PENDING":
                return self.orders[order_id]
        return None

    def mark_in_progress(self, order_id, robot_id):
        if order_id in self.orders:
            self.orders[order_id]["status"] = "IN_PROGRESS"
            self.orders[order_id]["robot"] = robot_id

    def mark_completed(self, order_id):
        if order_id in self.orders:
            self.orders[order_id]["status"] = "COMPLETED"

    def cancel_order(self, order_id):
        if order_id in self.orders:
            order = self.orders[order_id]
            if order["status"] == "PENDING":
                # Mark as cancelled so pop_next ignores it
                order["status"] = "CANCELLED"
            elif order["status"] == "IN_PROGRESS":
                order["status"] = "CANCELLED"
            return order
        return None

    def to_list(self):
        """
        Returns a list of all active orders (PENDING or IN_PROGRESS) for UI.
        """
        return [order for order in self.orders.values() if order["status"] in ("PENDING", "IN_PROGRESS")]

    def clear(self):
        self.pending_queue.clear()
        self.orders.clear()
        self.order_counter = 0
