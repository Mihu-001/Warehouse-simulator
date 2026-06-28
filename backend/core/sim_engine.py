import csv
import random
from backend.core.grid import WarehouseGrid
from backend.core.robot import Robot
from backend.core.order_queue import OrderQueue
from backend.core.dock import Dock
from backend.utils.stats import StatsTracker
from backend.algorithms.astar import astar
from backend.algorithms.dijkstra import dijkstra
from backend.algorithms.bfs import bfs

class SimEngine:
    def __init__(self):
        self.grid = WarehouseGrid()
        self.order_queue = OrderQueue()
        self.stats = StatsTracker()
        
        # 4 Robots stationed in Staging coordinates
        self.robots = [
            Robot("R1", (37, 26)),
            Robot("R2", (37, 28)),
            Robot("R3", (37, 30)),
            Robot("R4", (37, 32))
        ]
        
        # 4 Docks matching layout positions
        self.docks = {
            "LOAD_TC": Dock("LOAD_TC", 3),
            "UNLOAD_TC": Dock("UNLOAD_TC", 5),
            "LOAD_DRY": Dock("LOAD_DRY", 4),
            "UNLOAD_DRY": Dock("UNLOAD_DRY", 6)
        }
        
        self.algorithm = "astar"
        self.speed_multiplier = 1.0
        self.events = ["Simulador de Almacén Inteligente Iniciado"]
        
        # Load products catalog in-memory
        self.products = []
        self.products_by_rack = {}
        self._load_products()

    def _load_products(self):
        products_csv = "backend/data/products.csv"
        try:
            with open(products_csv, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    p = {
                        "sku": row["sku"],
                        "nombre": row["nombre"],
                        "zona": row["zona"],
                        "rack_id": row["rack_id"],
                        "cantidad": int(row["cantidad"]),
                        "peso_kg": float(row["peso_kg"]),
                        "categoria": row["categoria"]
                    }
                    self.products.append(p)
                    
                    rack_id = p["rack_id"]
                    if rack_id not in self.products_by_rack:
                        self.products_by_rack[rack_id] = []
                    self.products_by_rack[rack_id].append(p)
        except Exception as e:
            print(f"Error loading products catalog: {e}")

    def get_algo_fn(self):
        return {"astar": astar, "dijkstra": dijkstra, "bfs": bfs}[self.algorithm]

    def tick(self, dt):
        """
        Runs a simulation frame, moving robots and managing order routing.
        """
        # Dispatch waiting orders
        self._dispatch_orders()
        
        # Advance robots
        for robot in self.robots:
            # Check transitions before moving
            was_picking = robot.state == "PICKING"
            
            robot.advance(dt * self.speed_multiplier)
            
            # 1. Check if robot just started picking
            if robot.reached_rack() and not was_picking:
                self.events.append(f"{robot.id} comenzó picking de {robot.carrying} en {robot.target_rack}")
                self.stats.log_pick_time(1.0) # Picking duration
                
            # 2. Check if robot reached delivery dock
            if robot.reached_dock():
                dock_id = robot.target_dock
                sku = robot.carrying
                order_id = robot.order_id
                
                # Perform delivery at dock
                dock_event = self.docks[dock_id].deliver_product(sku)
                self.events.append(f"{robot.id} entregó {sku} en {dock_id}")
                if dock_event:
                    self.events.append(dock_event)
                
                # Register delivery in stats tracker
                # Compute path to return home
                curr_cell = (int(round(robot.position[0])), int(round(robot.position[1])))
                occupied = self._get_occupied_cells(robot)
                algo_fn = self.get_algo_fn()
                
                # Calculate return base path
                path_to_base, nodes, ms = algo_fn(self.grid.matrix, curr_cell, robot.base_position, occupied)
                
                # Retrospectively register completed order path stats (to-rack + to-dock + return)
                # First let's retrieve stats we logged during start of order or log them here
                # Let's write out to the simulation CSV
                self.stats.register_delivery(robot.id, order_id, self.algorithm, nodes, robot.original_distance, ms)
                
                # Mark order as completed in queue
                self.order_queue.mark_completed(order_id)
                
                robot.return_to_base(path_to_base)
                
        self.events = self.events[-5:]

    def _get_occupied_cells(self, current_robot):
        """
        Returns cells currently blocked by other robots.
        """
        occupied = set()
        for r in self.robots:
            if r != current_robot:
                # Get rounded cell
                occupied.add((int(round(r.position[0])), int(round(r.position[1]))))
        return occupied

    def _dispatch_orders(self):
        """
        Checks if we can match any pending orders to idle robots.
        """
        idle_robots = [r for r in self.robots if r.state == "IDLE"]
        if not idle_robots:
            return
            
        next_order = self.order_queue.pop_next()
        if not next_order:
            return
            
        rack_id = next_order["rack_id"]
        rack_pos = self.grid.rack_position(rack_id)
        if not rack_pos:
            return
            
        # Find nearest idle robot
        robot = min(
            idle_robots,
            key=lambda r: abs(r.position[0] - rack_pos[0]) + abs(r.position[1] - rack_pos[1])
        )
        
        # Calculate paths
        curr_cell = (int(round(robot.position[0])), int(round(robot.position[1])))
        dock_pos = self.grid.nearest_dock(rack_pos)
        dock_id = "UNLOAD_TC" if rack_id.startswith("TC") else "UNLOAD_DRY"
        
        occupied = self._get_occupied_cells(robot)
        algo_fn = self.get_algo_fn()
        
        # 1. Path from robot position to rack
        path_to_rack, nodes_1, ms_1 = algo_fn(self.grid.matrix, curr_cell, rack_pos, occupied)
        # 2. Path from rack to dock
        # When calculating path from rack to dock, the rack is the start, so it is walkable.
        path_to_dock, nodes_2, ms_2 = algo_fn(self.grid.matrix, rack_pos, dock_pos, occupied)
        
        total_nodes = nodes_1 + nodes_2
        total_ms = ms_1 + ms_2
        total_dist = len(path_to_rack) + len(path_to_dock)
        
        self.stats.log_path(total_nodes, total_ms, total_dist, self.algorithm)
        
        # Update order in progress
        self.order_queue.mark_in_progress(next_order["id"], robot.id)
        
        # Assign routes to robot
        robot.assign_route(path_to_rack, path_to_dock, rack_id, next_order["id"], next_order["sku"])
        robot.target_dock = dock_id
        
        self.events.append(f"Ruta asignada a {robot.id}: {total_dist} tiles ({self.algorithm.upper()})")

    def assign_order(self, rack_id):
        """
        Creates an order when user clicks a rack.
        """
        # Find a product inside this rack
        products = self.products_by_rack.get(rack_id, [])
        product = None
        for p in products:
            if p["cantidad"] > 0:
                product = p
                break
                
        if product:
            product["cantidad"] -= 1  # Pick one
            sku = product["sku"]
            zone = product["zona"]
        else:
            sku = "SKU-RESTOCK"
            zone = "TC" if "TC" in rack_id else "DRY"
            
        order_id = self.order_queue.push(rack_id, sku, zone)
        self.events.append(f"Pedido {order_id} registrado para rack {rack_id}")

    def assign_random_order(self):
        """
        Selects a random rack and assigns an order to it.
        """
        # Choose a random rack with quantity > 0
        valid_products = [p for p in self.products if p["cantidad"] > 0]
        if valid_products:
            p = random.choice(valid_products)
            self.assign_order(p["rack_id"])
        else:
            # Fallback to random rack from grid lists
            rack_id = random.choice(self.grid.tc_racks_list + self.grid.dry_racks_list)
            self.assign_order(rack_id)

    def change_algorithm(self, algo):
        """
        Swaps routing algorithm and recalculates all active paths.
        """
        if algo not in ("astar", "dijkstra", "bfs"):
            return
            
        self.algorithm = algo
        self.stats.algorithm = algo
        self.events.append(f"Cambiado algoritmo de búsqueda a {algo.upper()}")
        
        # Recalculate routes for all active robots mid-simulation
        algo_fn = self.get_algo_fn()
        
        for robot in self.robots:
            if robot.state == "IDLE":
                continue
                
            curr_cell = (int(round(robot.position[0])), int(round(robot.position[1])))
            occupied = self._get_occupied_cells(robot)
            
            if robot.state == "MOVING_TO_PRODUCT":
                # Recalculate path to rack, and path to dock
                rack_pos = self.grid.rack_position(robot.target_rack)
                dock_pos = self.grid.nearest_dock(rack_pos)
                
                path_to_rack, nodes_1, ms_1 = algo_fn(self.grid.matrix, curr_cell, rack_pos, occupied)
                path_to_dock, nodes_2, ms_2 = algo_fn(self.grid.matrix, rack_pos, dock_pos, occupied)
                
                robot.path_to_rack = path_to_rack
                robot.path_to_dock = path_to_dock
                robot.path = list(path_to_rack)
                
                self.stats.log_path(nodes_1 + nodes_2, ms_1 + ms_2, len(path_to_rack) + len(path_to_dock), algo)
                
            elif robot.state == "MOVING_TO_DOCK":
                # Recalculate path to dock
                rack_pos = self.grid.rack_position(robot.target_rack)
                dock_pos = self.grid.nearest_dock(rack_pos)
                
                path_to_dock, nodes, ms = algo_fn(self.grid.matrix, curr_cell, dock_pos, occupied)
                robot.path_to_dock = path_to_dock
                robot.path = list(path_to_dock)
                
                self.stats.log_path(nodes, ms, len(path_to_dock), algo)
                
            elif robot.state == "RETURNING":
                # Recalculate path to base
                path_to_base, nodes, ms = algo_fn(self.grid.matrix, curr_cell, robot.base_position, occupied)
                robot.path_to_base = path_to_base
                robot.path = list(path_to_base)
                
                self.stats.log_path(nodes, ms, len(path_to_base), algo)

    def cancel_robot(self, robot_id):
        """
        Cancels active order of robot and commands it to return to base.
        """
        for robot in self.robots:
            if robot.id == robot_id:
                if robot.state in ("IDLE", "RETURNING"):
                    return
                    
                # Cancel in order queue
                if robot.order_id:
                    self.order_queue.cancel_order(robot.order_id)
                    
                # Compute path to base
                curr_cell = (int(round(robot.position[0])), int(round(robot.position[1])))
                occupied = self._get_occupied_cells(robot)
                algo_fn = self.get_algo_fn()
                
                path_to_base, nodes, ms = algo_fn(self.grid.matrix, curr_cell, robot.base_position, occupied)
                self.stats.log_path(nodes, ms, len(path_to_base), self.algorithm)
                
                robot.cancel_order(path_to_base)
                self.events.append(f"Orden de {robot.id} cancelada. Retornando a base.")
                return

    def get_state(self):
        """
        Serializes current simulation state.
        """
        # Active robots count
        active_robots = sum(1 for r in self.robots if r.state != "IDLE")
        
        # Load products inventory details for tooltips: return product count per rack
        rack_inventories = {}
        # Only include racks that have inventory loaded in memory
        for rack_id, p_list in self.products_by_rack.items():
            qty = sum(p["cantidad"] for p in p_list)
            # Find the primary products
            names = [p["nombre"].split(" #")[0] for p in p_list[:2]]
            rack_inventories[rack_id] = {
                "qty": qty,
                "skus": [p["sku"] for p in p_list[:3]],
                "names": names,
                "category": p_list[0]["categoria"] if p_list else "general"
            }
            
        stats_dict = self.stats.to_dict()
        stats_dict["active_robots"] = active_robots

        return {
            "type": "STATE_UPDATE",
            "grid": self.grid.to_matrix(),
            "robots": [r.to_dict() for r in self.robots],
            "orders": self.order_queue.to_list(),
            "stats": stats_dict,
            "events": self.events,
            "docks": {k: d.get_progress() for k, d in self.docks.items()},
            "rack_inventories": rack_inventories
        }

    def reset(self):
        """
        Resets simulator to original state.
        """
        self.order_queue.clear()
        self.stats.reset()
        
        # Reset products inventory
        self.products.clear()
        self.products_by_rack.clear()
        self._load_products()
        
        # Reset robots
        for robot in self.robots:
            robot.cancel_order(None)
            
        # Reset docks
        for dock in self.docks.values():
            dock.reset()
            
        self.events = ["Simulador reiniciado correctamente"]
