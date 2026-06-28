import React from 'react';

export default function StatsPanel({ stats }) {
  const getAlgoColor = (algo) => {
    if (algo === 'astar') return 'text-blue-400';
    if (algo === 'dijkstra') return 'text-purple-400';
    return 'text-emerald-400';
  };

  return (
    <div className="bg-white/5 border border-white/5 rounded-2xl p-4 backdrop-blur-md space-y-4">
      <div className="flex justify-between items-center border-b border-white/5 pb-2">
        <h2 className="text-[10px] font-bold text-white/40 uppercase tracking-widest">Estadísticas de Sesión</h2>
        <span className="text-[10px] px-2 py-0.5 rounded bg-white/5 font-semibold text-white/70">
          Activo: <span className={`font-bold capitalize ${getAlgoColor(stats.algorithm)}`}>{stats.algorithm === 'astar' ? 'A*' : stats.algorithm}</span>
        </span>
      </div>

      <div className="grid grid-cols-2 gap-3">
        <div className="bg-white/5 rounded-xl p-2.5 border border-white/5">
          <span className="text-[10px] text-white/40 block">Entregas</span>
          <span className="text-xl font-bold text-emerald-400">{stats.orders_completed}</span>
        </div>
        <div className="bg-white/5 rounded-xl p-2.5 border border-white/5">
          <span className="text-[10px] text-white/40 block">Distancia Total</span>
          <span className="text-lg font-bold text-white/90">{stats.total_distance} <span className="text-xs font-normal text-white/40">tiles</span></span>
        </div>
        <div className="bg-white/5 rounded-xl p-2.5 border border-white/5">
          <span className="text-[10px] text-white/40 block">Nodos Evaluados</span>
          <span className="text-lg font-bold text-amber-400">{stats.nodes_explored}</span>
        </div>
        <div className="bg-white/5 rounded-xl p-2.5 border border-white/5">
          <span className="text-[10px] text-white/40 block">Pick Promedio</span>
          <span className="text-lg font-bold text-blue-400">{stats.avg_pick_time ? stats.avg_pick_time.toFixed(1) : '0.0'}<span className="text-xs font-normal text-white/40">s</span></span>
        </div>
      </div>

      {/* Algorithm Comparison Matrix */}
      <div className="pt-2 border-t border-white/5">
        <h3 className="text-[10px] font-bold text-white/40 uppercase tracking-widest mb-2">Comparativa Algorítmica</h3>
        <div className="overflow-hidden rounded-lg border border-white/5">
          <table className="w-full text-[10px] text-left text-white/60">
            <thead className="bg-white/5 text-[9px] uppercase tracking-wider text-white/40">
              <tr>
                <th className="p-2">Algoritmo</th>
                <th className="p-2 text-right">Nodos (Prom)</th>
                <th className="p-2 text-right">Tiempo (Prom)</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-white/5 font-mono">
              <tr className={stats.algorithm === 'astar' ? 'bg-blue-500/5' : ''}>
                <td className="p-2 font-bold text-blue-400">A* Manhattan</td>
                <td className="p-2 text-right">{stats.comparison?.astar?.avg_nodes || 0}</td>
                <td className="p-2 text-right text-blue-300">{(stats.comparison?.astar?.avg_time_ms || 0).toFixed(2)} ms</td>
              </tr>
              <tr className={stats.algorithm === 'dijkstra' ? 'bg-purple-500/5' : ''}>
                <td className="p-2 font-bold text-purple-400">Dijkstra</td>
                <td className="p-2 text-right">{stats.comparison?.dijkstra?.avg_nodes || 0}</td>
                <td className="p-2 text-right text-purple-300">{(stats.comparison?.dijkstra?.avg_time_ms || 0).toFixed(2)} ms</td>
              </tr>
              <tr className={stats.algorithm === 'bfs' ? 'bg-emerald-500/5' : ''}>
                <td className="p-2 font-bold text-emerald-400">BFS</td>
                <td className="p-2 text-right">{stats.comparison?.bfs?.avg_nodes || 0}</td>
                <td className="p-2 text-right text-emerald-300">{(stats.comparison?.bfs?.avg_time_ms || 0).toFixed(2)} ms</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
