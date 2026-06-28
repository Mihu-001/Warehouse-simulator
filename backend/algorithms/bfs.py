import time
from collections import deque
from backend.algorithms.utils import is_walkable

def bfs(grid, start, goal, occupied_cells=None):
    """
    Breadth-First Search pathfinding.
    
    Args:
        grid:           list of lists (matrix) with cell types
        start:          tuple (row, col)
        goal:           tuple (row, col)
        occupied_cells: set of tuples representing cells occupied by other robots
        
    Returns:
        path:           list of tuples [(row, col), ...] representing the path
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

    queue = deque([start])
    came_from = {}
    visited = {start}
    nodes_explored = 0

    while queue:
        current = queue.popleft()
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

        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (current[0] + dr, current[1] + dc)
            
            if neighbor in visited:
                continue
                
            if not is_walkable(grid, neighbor, occupied_cells, goal):
                continue
                
            visited.add(neighbor)
            came_from[neighbor] = current
            queue.append(neighbor)

    # Retry without occupied cells if blocked
    if occupied_cells:
        elapsed_so_far = (time.perf_counter() - start_time) * 1000
        fallback_path, fallback_nodes, fallback_time = bfs(grid, start, goal, set())
        return fallback_path, nodes_explored + fallback_nodes, elapsed_so_far + fallback_time

    elapsed = (time.perf_counter() - start_time) * 1000
    return [], nodes_explored, elapsed
