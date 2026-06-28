import React from 'react';

export default function AlgoSelector({ current, onChange }) {
  const algos = ["astar", "dijkstra", "bfs"];
  
  const getAlgoLabel = (algo) => {
    if (algo === "astar") return "A* Manhattan";
    return algo.toUpperCase();
  };

  const getActiveStyles = (algo) => {
    if (current !== algo) return "bg-white/5 text-white/50 hover:bg-white/10 hover:text-white";
    
    if (algo === "astar") return "bg-blue-600/25 text-blue-400 border border-blue-500/50 shadow-lg shadow-blue-500/10";
    if (algo === "dijkstra") return "bg-purple-600/25 text-purple-400 border border-purple-500/50 shadow-lg shadow-purple-500/10";
    return "bg-emerald-600/25 text-emerald-400 border border-emerald-500/50 shadow-lg shadow-emerald-500/10";
  };

  return (
    <div className="bg-white/5 border border-white/5 rounded-2xl p-4 backdrop-blur-md">
      <h2 className="text-[10px] font-bold text-white/40 uppercase tracking-widest mb-3">Algoritmo de Búsqueda</h2>
      <div className="flex gap-2">
        {algos.map(algo => (
          <button
            key={algo}
            onClick={() => onChange(algo)}
            className={`flex-1 rounded-xl py-2 text-xs font-semibold transition-all duration-200 capitalize ${getActiveStyles(algo)}`}
          >
            {getAlgoLabel(algo)}
          </button>
        ))}
      </div>
    </div>
  );
}
