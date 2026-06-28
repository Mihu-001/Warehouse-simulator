import { useMemo } from 'react';

export default function useSimulation(wsState) {
  return useMemo(() => {
    // Safe defaults when connection is pending or lost
    if (!wsState) {
      return {
        grid: [],
        robots: [],
        stats: {
          orders_completed: 0,
          total_distance: 0,
          nodes_explored: 0,
          avg_pick_time: 0.0,
          active_robots: 0,
          algorithm: "astar",
          comparison: {
            astar: { avg_nodes: 0, avg_time_ms: 0.0, runs: 0 },
            dijkstra: { avg_nodes: 0, avg_time_ms: 0.0, runs: 0 },
            bfs: { avg_nodes: 0, avg_time_ms: 0.0, runs: 0 }
          }
        },
        events: ["Conectando al servidor backend..."],
        docks: {
          LOAD_TC: { id: "LOAD_TC", loaded: 0, capacity: 5 },
          UNLOAD_TC: { id: "UNLOAD_TC", loaded: 0, capacity: 5 },
          LOAD_DRY: { id: "LOAD_DRY", loaded: 0, capacity: 5 },
          UNLOAD_DRY: { id: "UNLOAD_DRY", loaded: 0, capacity: 5 }
        },
        rackInventories: {}
      };
    }

    return {
      grid: wsState.grid || [],
      robots: wsState.robots || [],
      stats: wsState.stats || {
        orders_completed: 0,
        total_distance: 0,
        nodes_explored: 0,
        avg_pick_time: 0.0,
        active_robots: 0,
        algorithm: "astar",
        comparison: {
          astar: { avg_nodes: 0, avg_time_ms: 0.0, runs: 0 },
          dijkstra: { avg_nodes: 0, avg_time_ms: 0.0, runs: 0 },
          bfs: { avg_nodes: 0, avg_time_ms: 0.0, runs: 0 }
        }
      },
      events: wsState.events || [],
      docks: wsState.docks || {},
      rackInventories: wsState.rack_inventories || {}
    };
  }, [wsState]);
}
