import React from 'react';

export default function EventLog({ events }) {
  const getEventStyles = (evt) => {
    if (evt.includes("entregó") || evt.includes("despachado")) {
      return { border: "border-emerald-500/20 bg-emerald-500/5", text: "text-emerald-400", dot: "bg-emerald-500" };
    }
    if (evt.includes("comenzó") || evt.includes("recogió")) {
      return { border: "border-amber-500/20 bg-amber-500/5", text: "text-amber-400", dot: "bg-amber-500" };
    }
    if (evt.includes("Ruta asignada") || evt.includes("Cambiado")) {
      return { border: "border-blue-500/20 bg-blue-500/5", text: "text-blue-400", dot: "bg-blue-500" };
    }
    if (evt.includes("cancelada")) {
      return { border: "border-rose-500/20 bg-rose-500/5", text: "text-rose-400", dot: "bg-rose-500" };
    }
    return { border: "border-white/5 bg-white/5", text: "text-white/70", dot: "bg-white/30" };
  };

  return (
    <div className="bg-white/5 border border-white/5 rounded-2xl p-4 backdrop-blur-md flex-1 flex flex-col min-h-[160px]">
      <h2 className="text-[10px] font-bold text-white/40 uppercase tracking-widest mb-3">Historial de Eventos</h2>
      <div className="flex-1 overflow-y-auto space-y-2 max-h-[180px] pr-1">
        {events.length === 0 ? (
          <span className="text-[10px] text-white/30 italic">No hay eventos en esta sesión.</span>
        ) : (
          events.slice().reverse().map((evt, idx) => {
            const styles = getEventStyles(evt);
            return (
              <div
                key={idx}
                className={`flex items-start gap-2 p-2 border rounded-xl transition-all duration-150 ${styles.border}`}
              >
                <span className={`w-1.5 h-1.5 rounded-full mt-1.5 shrink-0 ${styles.dot}`} />
                <span className={`text-[10px] leading-relaxed font-semibold ${styles.text}`}>
                  {evt}
                </span>
              </div>
            );
          })
        )}
      </div>
    </div>
  );
}
