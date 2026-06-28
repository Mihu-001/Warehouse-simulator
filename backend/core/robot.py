class Robot:
    def __init__(self, robot_id, base_position):
        self.id = robot_id
        self.base_position = base_position  # (row, col)
        
        # Position is float for smooth canvas interpolation
        self.position = (float(base_position[0]), float(base_position[1]))
        
        self.state = "IDLE"  # IDLE, MOVING_TO_PRODUCT, PICKING, MOVING_TO_DOCK, RETURNING
        self.path = []       # Active list of (row, col)
        self.path_to_rack = []
        self.path_to_dock = []
        self.path_to_base = []
        
        self.carrying = None
        self.target_rack = None
        self.target_dock = None
        self.order_id = None
        self.original_distance = 0  # Stored for CSV metrics
        
        self.speed = 4.0      # tiles per second
        self.pick_timer = 0.0 # Time remaining to pick product (seconds)

    def assign_route(self, path_to_rack, path_to_dock, rack_id, order_id, sku):
        """
        Assigns routes to navigate to rack and then to dock.
        """
        self.path_to_rack = path_to_rack
        self.path_to_dock = path_to_dock
        self.original_distance = len(path_to_rack) + len(path_to_dock)
        self.target_rack = rack_id
        self.order_id = order_id
        self.carrying = sku
        
        if path_to_rack:
            self.path = list(path_to_rack)
            self.state = "MOVING_TO_PRODUCT"
        else:
            # If already at rack
            self.path = []
            self.state = "PICKING"
            self.pick_timer = 1.0

    def cancel_order(self, path_to_base):
        """
        Cancels current order and assigns path back to staging base.
        """
        self.order_id = None
        self.carrying = None
        self.target_rack = None
        self.target_dock = None
        self.path_to_rack = []
        self.path_to_dock = []
        
        if path_to_base:
            self.path = list(path_to_base)
            self.state = "RETURNING"
        else:
            self.position = (float(self.base_position[0]), float(self.base_position[1]))
            self.path = []
            self.state = "IDLE"

    def advance(self, dt):
        """
        Updates robot position based on speed and time delta.
        """
        if self.state == "IDLE":
            return
            
        if self.state == "PICKING":
            self.pick_timer -= dt
            if self.pick_timer <= 0:
                self.state = "MOVING_TO_DOCK"
                self.path = list(self.path_to_dock)
            return

        if not self.path:
            # Reached a destination node but no more steps left in current path segment
            if self.state == "MOVING_TO_PRODUCT":
                self.state = "PICKING"
                self.pick_timer = 1.0  # 1 second pick time
            elif self.state == "MOVING_TO_DOCK":
                # Wait for SimEngine to process delivery and set to RETURNING
                pass
            elif self.state == "RETURNING":
                self.state = "IDLE"
                self.reset_order()
            return

        # Move towards the next waypoint in path
        target = self.path[0]
        curr_r, curr_c = self.position
        tgt_r, tgt_c = target
        
        dr = tgt_r - curr_r
        dc = tgt_c - curr_c
        dist = (dr**2 + dc**2)**0.5
        
        if dist < 0.01:
            self.position = (float(tgt_r), float(tgt_c))
            self.path.pop(0)
            return
            
        step = self.speed * dt
        if step >= dist:
            self.position = (float(tgt_r), float(tgt_c))
            self.path.pop(0)
        else:
            self.position = (curr_r + dr * step / dist, curr_c + dc * step / dist)

    def reset_order(self):
        self.order_id = None
        self.carrying = None
        self.target_rack = None
        self.target_dock = None
        self.original_distance = 0
        self.path_to_rack = []
        self.path_to_dock = []
        self.path = []

    def return_to_base(self, path_to_base):
        self.path_to_base = path_to_base
        self.path = list(path_to_base)
        self.state = "RETURNING"
        self.carrying = None
        self.target_rack = None
        self.target_dock = None

    def reached_rack(self):
        return self.state == "PICKING" and self.pick_timer == 1.0

    def reached_dock(self):
        return self.state == "MOVING_TO_DOCK" and not self.path

    def to_dict(self):
        return {
            "id": self.id,
            "row": round(self.position[0], 3),
            "col": round(self.position[1], 3),
            "state": self.state,
            "path": self.path,
            "carrying": self.carrying,
            "target_rack": self.target_rack,
            "target_dock": self.target_dock
        }
