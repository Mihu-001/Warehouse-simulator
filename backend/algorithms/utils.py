def is_walkable(grid, cell, occupied_cells=None, goal=None):
    """
    Check if a cell (row, col) can be entered.
    Walls (8) are never walkable.
    Racks (1, 2) are only walkable if they are the goal cell.
    Occupied cells (by other robots) are not walkable.
    """
    r, c = cell
    if not (0 <= r < len(grid) and 0 <= c < len(grid[0])):
        return False
    
    cell_type = grid[r][c]
    if cell_type == 8:  # Wall
        return False
    
    # Racks are only navigable if they are the destination (picking from them)
    if cell_type in (1, 2):
        if goal is not None and (r, c) == goal:
            return True
        return False
        
    if occupied_cells and cell in occupied_cells:
        return False
        
    return True
