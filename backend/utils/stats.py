import os
import csv
import json

class StatsTracker:
    def __init__(self):
        self.orders_completed = 0
        self.total_distance = 0
        self.nodes_explored = 0
        
        # Picking times tracking
        self.total_pick_time = 0.0
        self.pick_times_list = []
        
        self.algorithm = "astar"
        
        # Historical metrics for algorithm comparison
        self.algo_metrics = {
            "astar": {"nodes": 0, "time_ms": 0.0, "count": 0},
            "dijkstra": {"nodes": 0, "time_ms": 0.0, "count": 0},
            "bfs": {"nodes": 0, "time_ms": 0.0, "count": 0}
        }
        
        # CSV Path
        self.csv_path = "backend/data/simulation_session.csv"
        self._init_csv()

    def _init_csv(self):
        # Create CSV header if file doesn't exist
        os.makedirs("backend/data", exist_ok=True)
        if not os.path.exists(self.csv_path):
            with open(self.csv_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["pedido", "robot", "algoritmo", "nodos_explorados", "distancia_tiles", "tiempo_computo_ms"])

    def log_path(self, nodes, ms, distance, algorithm=None):
        """
        Record path calculation metrics.
        """
        algo = algorithm or self.algorithm
        self.nodes_explored += nodes
        self.total_distance += distance
        
        # Track by algorithm
        if algo in self.algo_metrics:
            self.algo_metrics[algo]["nodes"] += nodes
            self.algo_metrics[algo]["time_ms"] += ms
            self.algo_metrics[algo]["count"] += 1

    def register_delivery(self, robot_id, order_id, algo, nodes, distance, comp_ms):
        """
        Logs a completed pickup order to the tracker and writes a row in the session CSV.
        """
        self.orders_completed += 1
        
        # Add to CSV log
        try:
            with open(self.csv_path, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([order_id, robot_id, algo, nodes, distance, round(comp_ms, 3)])
        except Exception as e:
            print(f"Error logging delivery to CSV: {e}")

    def log_pick_time(self, pick_duration):
        self.pick_times_list.append(pick_duration)
        self.total_pick_time = sum(self.pick_times_list)

    def get_avg_pick_time(self):
        if not self.pick_times_list:
            return 0.0
        return self.total_pick_time / len(self.pick_times_list)

    def to_dict(self):
        # Build comparison statistics
        comparison = {}
        for algo, data in self.algo_metrics.items():
            count = data["count"]
            comparison[algo] = {
                "avg_nodes": round(data["nodes"] / count, 1) if count > 0 else 0,
                "avg_time_ms": round(data["time_ms"] / count, 3) if count > 0 else 0.0,
                "runs": count
            }
            
        return {
            "orders_completed": self.orders_completed,
            "total_distance": self.total_distance,
            "nodes_explored": self.nodes_explored,
            "avg_pick_time": round(self.get_avg_pick_time(), 2),
            "algorithm": self.algorithm,
            "comparison": comparison
        }

    def reset(self):
        self.orders_completed = 0
        self.total_distance = 0
        self.nodes_explored = 0
        self.total_pick_time = 0.0
        self.pick_times_list.clear()
        
        # Keep historical algo comparison, but clear run counts if desired or reset completely
        # Let's reset completely on reset to allow clean comparisons per run
        self.algo_metrics = {
            "astar": {"nodes": 0, "time_ms": 0.0, "count": 0},
            "dijkstra": {"nodes": 0, "time_ms": 0.0, "count": 0},
            "bfs": {"nodes": 0, "time_ms": 0.0, "count": 0}
        }
        # Re-initialize CSV (new session starts)
        if os.path.exists(self.csv_path):
            try:
                os.remove(self.csv_path)
            except Exception:
                pass
        self._init_csv()
