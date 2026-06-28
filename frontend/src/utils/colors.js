export const CELL_COLORS = {
  0: "#1e2130",       // EMPTY — walkway
  1: "#1a4a7a",       // RACK_TC — cold zone rack (dark blue)
  2: "#7a4a1a",       // RACK_DRY — dry zone rack (dark orange)
  3: "#0f4a3a",       // DOCK_LOAD_TC (loading cold)
  4: "#4a3a0f",       // DOCK_LOAD_DRY (loading dry)
  5: "#1a3a5a",       // DOCK_UNLOAD_TC (unloading cold)
  6: "#5a3a1a",       // DOCK_UNLOAD_DRY (unloading dry)
  7: "#2a2a3a",       // STAGING (robot base staging)
  8: "#0a0a0f",       // WALL (dark gray border)
}

export const ROBOT_COLORS = {
  IDLE:               "#4ade80",   // Green
  MOVING_TO_PRODUCT:  "#facc15",   // Yellow
  PICKING:            "#fb923c",   // Orange
  MOVING_TO_DOCK:     "#f87171",   // Red
  RETURNING:          "#94a3b8",   // Light gray
}

export const PATH_COLORS = {
  astar:    "#3b82f6",   // Vibrant blue
  dijkstra: "#8b5cf6",   // Vibrant purple
  bfs:      "#10b981",   // Vibrant green
}
