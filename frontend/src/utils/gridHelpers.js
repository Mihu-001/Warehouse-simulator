/**
 * Helper to determine rack ID based on cell coordinates and zone type.
 */
export function getRackIdAt(row, col, cellType) {
  if (cellType === 1) {
    return `TC-R${row}-C${col}`;
  }
  if (cellType === 2) {
    return `DRY-R${row}-C${col}`;
  }
  return null;
}

/**
 * Converts grid coordinates to canvas pixels.
 */
export function gridToPx(gridVal, cellSize) {
  return gridVal * cellSize;
}

/**
 * Converts canvas pixels to grid coordinates.
 */
export function pxToGrid(pxVal, cellSize) {
  return Math.floor(pxVal / cellSize);
}
