class Dock:
    def __init__(self, dock_id, dock_type, capacity=5):
        self.id = dock_id
        self.type = dock_type  # 3: LOAD_TC, 4: LOAD_DRY, 5: UNLOAD_TC, 6: UNLOAD_DRY
        self.capacity = capacity
        self.loaded_count = 0
        self.total_shipments = 0

    def deliver_product(self, sku):
        """
        Deliver a product to this dock.
        Returns a log string if a truck departs, otherwise None.
        """
        self.loaded_count += 1
        self.total_shipments += 1
        
        if self.loaded_count >= self.capacity:
            self.loaded_count = 0
            return f"Camión en {self.id} completado con éxito y despachado. Nuevo camión posicionado."
        return None

    def get_progress(self):
        return {
            "id": self.id,
            "loaded": self.loaded_count,
            "capacity": self.capacity
        }

    def reset(self):
        self.loaded_count = 0
        self.total_shipments = 0
