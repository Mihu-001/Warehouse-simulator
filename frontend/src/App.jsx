import React from 'react';
import useWebSocket from './hooks/useWebSocket';
import useSimulation from './hooks/useSimulation';
import WarehouseCanvas from './components/WarehouseCanvas';
import AlgoSelector from './components/AlgoSelector';
import StatsPanel from './components/StatsPanel';
import SpeedSlider from './components/SpeedSlider';
import EventLog from './components/EventLog';
import Legend from './components/Legend';

export default function App() {
  const { state, status, sendMessage } = useWebSocket();
  const { grid, robots, stats, events, docks, rackInventories } = useSimulation(state);

  const getStatusBadge = () => {
    if (status === "CONNECTED") {
      return (
        <span className="flex items-center gap-1.5 px-2 py-1 rounded-full text-[9px] font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
          <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
          Conectado
        </span>
      );
    }
    if (status === "CONNECTING") {
      return (
        <span className="flex items-center gap-1.5 px-2 py-1 rounded-full text-[9px] font-bold bg-amber-500/10 text-amber-400 border border-amber-500/20">
          <span className="w-1.5 h-1.5 rounded-full bg-amber-400 animate-bounce" />
          Conectando
        </span>
      );
    }
    return (
      <span className="flex items-center gap-1.5 px-2 py-1 rounded-full text-[9px] font-bold bg-rose-500/10 text-rose-400 border border-rose-500/20">
        <span className="w-1.5 h-1.5 rounded-full bg-rose-400" />
        Desconectado
      </span>
    );
  };

  const handleDownloadGraph = (zone) => {
    const url = `http://localhost:8000/api/graph/export${zone ? `?zone=${zone}` : ""}`;
    // Simple download trigger
    const link = document.createElement("a");
    link.href = url;
    link.download = `warehouse_graph_${zone || "full"}.json`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="flex h-screen w-screen bg-[#090b0f] text-white font-sans overflow-hidden">
      
      {/* Main View Area */}
      <div className="flex-1 flex flex-col p-6 overflow-hidden items-center justify-between">
        
        {/* Header bar */}
        <header className="w-full max-w-[960px] flex justify-between items-center bg-[#131722]/50 border border-white/5 px-5 py-3 rounded-2xl backdrop-blur-md">
          <div className="flex items-center gap-3">
            <img src="https://img.icons8.com/color/48/amazon.png" alt="Amazon Logo" className="w-7 h-7" />
            <div>
              <h1 className="text-sm font-bold tracking-wide">Amazon Smart Warehouse</h1>
              <p className="text-[10px] text-white/40 font-semibold tracking-wider uppercase">Complejidad Algorítmica · 1ACC0184</p>
            </div>
          </div>
          {getStatusBadge()}
        </header>

        {/* Canvas Frame */}
        <main className="my-auto flex flex-col items-center justify-center">
          <WarehouseCanvas
            grid={grid}
            robots={robots}
            stats={stats}
            docks={docks}
            rackInventories={rackInventories}
            onRackClick={(rackId) => sendMessage({ type: 'CLICK_RACK', rack_id: rackId })}
            onRobotCancel={(robotId) => sendMessage({ type: 'CANCEL_ROBOT', robot_id: robotId })}
          />
          <div className="flex justify-between w-[960px] text-[10px] text-white/30 font-medium px-4 mt-2">
            <span>💡 Click Izquierdo en Rack: Asignar Pedido</span>
            <span>💡 Hover: Tooltip Detalles</span>
            <span>💡 Click Derecho en Robot: Cancelar Orden</span>
          </div>
        </main>

        {/* Bottom Banner */}
        <footer className="w-full max-w-[960px] flex justify-between items-center text-[10px] text-white/40 bg-white/5 border border-white/5 px-4 py-2 rounded-xl">
          <span>Integrantes Grupo: TB1 Informe</span>
          <span>FastAPI Backend + React Canvas Simulation</span>
        </footer>
      </div>

      {/* Control & Statistics Panel (Right Sidebar) */}
      <aside className="w-[360px] h-screen bg-[#11131a] border-l border-white/5 flex flex-col p-5 gap-4 overflow-y-auto select-none">
        
        {/* Algorithm Selector */}
        <AlgoSelector
          current={stats.algorithm}
          onChange={(algo) => sendMessage({ type: 'CHANGE_ALGO', algo })}
        />

        {/* Real-time KPI Stats */}
        <StatsPanel stats={stats} />

        {/* Simulation speed */}
        <SpeedSlider
          onChange={(val) => sendMessage({ type: 'SET_SPEED', value: val })}
        />

        {/* Action Panel */}
        <div className="bg-white/5 border border-white/5 rounded-2xl p-4 space-y-3">
          <h2 className="text-[10px] font-bold text-white/40 uppercase tracking-widest">Acciones de Almacén</h2>
          
          <div className="flex gap-2">
            <button
              onClick={() => sendMessage({ type: 'ADD_RANDOM_ORDER' })}
              className="flex-1 bg-amber-600 hover:bg-amber-500 text-white font-semibold rounded-xl text-xs py-2.5 transition-all active:scale-[0.98]"
            >
              + Pedido Aleatorio
            </button>
            
            <button
              onClick={() => sendMessage({ type: 'RESET' })}
              className="flex-1 bg-white/10 hover:bg-white/20 text-white font-semibold rounded-xl text-xs py-2.5 transition-all active:scale-[0.98]"
            >
              ↺ Reiniciar
            </button>
          </div>

          <div className="border-t border-white/5 pt-3 space-y-2">
            <span className="text-[10px] font-bold text-white/40 uppercase tracking-widest block">Exportar Grafo (NetworkX)</span>
            <div className="grid grid-cols-3 gap-1">
              <button
                onClick={() => handleDownloadGraph()}
                className="bg-blue-600/10 hover:bg-blue-600/25 border border-blue-500/20 text-blue-400 font-semibold rounded-lg text-[9px] py-1.5 transition-all"
              >
                Completo
              </button>
              <button
                onClick={() => handleDownloadGraph("TC")}
                className="bg-purple-600/10 hover:bg-purple-600/25 border border-purple-500/20 text-purple-400 font-semibold rounded-lg text-[9px] py-1.5 transition-all"
              >
                TC (Frío)
              </button>
              <button
                onClick={() => handleDownloadGraph("DRY")}
                className="bg-amber-600/10 hover:bg-amber-600/25 border border-amber-500/20 text-amber-400 font-semibold rounded-lg text-[9px] py-1.5 transition-all"
              >
                DRY (Seco)
              </button>
            </div>
          </div>
        </div>

        {/* Real-time simulation events */}
        <EventLog events={events} />

        {/* Code colors and states */}
        <Legend />
      </aside>
    </div>
  );
}
