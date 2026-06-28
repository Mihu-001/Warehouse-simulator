import heapq
import time
from backend.algorithms.utils import is_walkable

def astar(grid, start, goal, occupied_cells=None):
    """
    A* pathfinding with Manhattan distance heuristic.
    
    Args:
        grid:           list of lists (matrix) with cell types
        start:          tuple (row, col)
        goal:           tuple (row, col)
        occupied_cells: set of tuples representing cells occupied by other robots
        
    Returns:
        path:           list of tuples [(row, col), ...] representing the path (including start and goal)
        nodes_explored: int number of evaluated nodes
        time_ms:        float computation time in milliseconds
    """
    start_time = time.perf_counter()
    if occupied_cells is None:
        occupied_cells = set()
    start = tuple(start)
    goal = tuple(goal)
    
    if start == goal:
        elapsed = (time.perf_counter() - start_time) * 1000
        return [start], 0, elapsed

    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])  # Manhattan distance

    open_set = []
    # Items: (f_score, insertion_index, current_node) to avoid comparison errors
    heapq.heappush(open_set, (heuristic(start, goal), 0, start))
    came_from = {}
    g_score = {start: 0}
    nodes_explored = 0
    counter = 1

    while open_set:
        _, _, current = heapq.heappop(open_set)
        nodes_explored += 1

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            elapsed = (time.perf_counter() - start_time) * 1000
            return path, nodes_explored, elapsed

        # 4-connectivity: up, down, left, right
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (current[0] + dr, current[1] + dc)
            
            if not is_walkable(grid, neighbor, occupied_cells, goal):
                continue
                
            tentative_g = g_score[current] + 1
            if tentative_g < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score = tentative_g + heuristic(neighbor, goal)
                counter += 1
                heapq.heappush(open_set, (f_score, counter, neighbor))

    # If no path found (e.g. because of occupied cells blocking), retry without occupied cells as fallback
    if occupied_cells:
        elapsed_so_far = (time.perf_counter() - start_time) * 1000
        # Call astar recursively with empty occupied cells
        fallback_path, fallback_nodes, fallback_time = astar(grid, start, goal, set())
        return fallback_path, nodes_explored + fallback_nodes, elapsed_so_far + fallback_time

    elapsed = (time.perf_counter() - start_time) * 1000
    return [], nodes_explored, elapsed
