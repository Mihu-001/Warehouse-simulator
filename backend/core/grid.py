import json
import os
import networkx as nx

class WarehouseGrid:
    def __init__(self):
        layout_path = "backend/data/warehouse_layout.json"
        if not os.path.exists(layout_path):
            raise FileNotFoundError(f"Layout file not found at {layout_path}. Run generate_data.py first.")
            
        with open(layout_path, "r") as f:
            layout = json.load(f)
            
        self.rows = layout["rows"]
        self.cols = layout["cols"]
        self.matrix = layout["grid"]  # 60x40 matrix of ints
        self.tc_racks_list = layout["tc_racks"]
        self.dry_racks_list = layout["dry_racks"]
        self.docks = layout["docks"]
        
        # Build maps for rack lookup
        self.rack_positions = {}
        # Parse TC rack positions
        for rack in self.tc_racks_list:
            # Format: TC-R{row}-C{col}
            parts = rack.split("-")
            r = int(parts[1][1:])
            c = int(parts[2][1:])
            self.rack_positions[rack] = (r, c)
            
        # Parse DRY rack positions
        for rack in self.dry_racks_list:
            # Format: DRY-R{row}-C{col}
            parts = rack.split("-")
            r = int(parts[1][1:])
            c = int(parts[2][1:])
            self.rack_positions[rack] = (r, c)

    def to_matrix(self):
        return self.matrix

    def rack_position(self, rack_id):
        return self.rack_positions.get(rack_id)

    def get_rack_at(self, row, col):
        # Inverse lookup
        for rack_id, pos in self.rack_positions.items():
            if pos == (row, col):
                return rack_id
        return None

    def nearest_dock(self, rack_pos):
        """
        Determines the nearest appropriate dock depending on rack zone (TC vs DRY).
        TC items go to UNLOAD_TC, DRY items to UNLOAD_DRY (or nearest of matching category).
        """
        r, c = rack_pos
        # Determine if it's a TC or DRY rack
        is_tc = c < 28  # TC racks are in cols 2 to 25
        
        if is_tc:
            # Docks for TC: LOAD_TC (col 10), UNLOAD_TC (col 20)
            # Default delivery dock is UNLOAD_TC (col 20, row 0)
            return (self.docks["UNLOAD_TC"]["row"], self.docks["UNLOAD_TC"]["col"])
        else:
            # Docks for DRY: LOAD_DRY (col 35), UNLOAD_DRY (col 45)
            # Default delivery dock is UNLOAD_DRY (col 45, row 0)
            return (self.docks["UNLOAD_DRY"]["row"], self.docks["UNLOAD_DRY"]["col"])

    def to_networkx_graph(self):
        """
        Creates a NetworkX Graph representing the walkable grid structure.
        Walls are excluded. Racks are connected to adjacent aisles, but not to other racks.
        """
        G = nx.Graph()
        
        # Add non-wall nodes
        for r in range(self.rows):
            for c in range(self.cols):
                cell_type = self.matrix[r][c]
                if cell_type == 8:  # Skip Walls
                    continue
                
                # Determine zone (TC, DRY, COMMON)
                if c < 28:
                    zone = "TC"
                elif c > 28:
                    zone = "DRY"
                else:
                    zone = "COMMON"
                    
                node_id = f"{r},{c}"
                G.add_node(node_id, row=r, col=c, type=cell_type, zone=zone)
                
        # Add edges (4-connectivity)
        for r in range(self.rows):
            for c in range(self.cols):
                cell_type = self.matrix[r][c]
                if cell_type == 8:
                    continue
                
                node_id = f"{r},{c}"
                
                # Connect to right and down neighbors to cover all edges
                for dr, dc in [(0, 1), (1, 0)]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self.rows and 0 <= nc < self.cols:
                        n_type = self.matrix[nr][nc]
                        if n_type == 8:
                            continue
                            
                        # Robots cannot travel *through* racks. 
                        # So, an edge cannot exist between two racks!
                        if cell_type in (1, 2) and n_type in (1, 2):
                            continue
                            
                        neighbor_id = f"{nr},{nc}"
                        G.add_edge(node_id, neighbor_id, weight=1.0)
                        
        return G

    def get_subgraph_by_zone(self, zone):
        """
        Returns a subgraph for TC or DRY zone only (useful for academic report).
        """
        G = self.to_networkx_graph()
        nodes_to_keep = [n for n, attr in G.nodes(data=True) if attr["zone"] == zone]
        return G.subgraph(nodes_to_keep)
