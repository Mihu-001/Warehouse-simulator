import React, { useState } from 'react';

export default function SpeedSlider({ onChange }) {
  const [val, setVal] = useState(1.0);

  const handleChange = (e) => {
    const v = parseFloat(e.target.value);
    setVal(v);
    onChange(v);
  };

  return (
    <div className="bg-white/5 border border-white/5 rounded-2xl p-4 backdrop-blur-md">
      <div className="flex justify-between items-center mb-2">
        <span className="text-[10px] font-bold text-white/40 uppercase tracking-widest">Velocidad Simulación</span>
        <span className="text-xs font-mono font-bold text-amber-400">{val.toFixed(1)}x</span>
      </div>
      <input
        type="range"
        min="0.2"
        max="5.0"
        step="0.1"
        value={val}
        onChange={handleChange}
        className="w-full h-1.5 bg-white/10 rounded-lg appearance-none cursor-pointer accent-amber-500"
      />
      <div className="flex justify-between text-[8px] text-white/30 font-mono mt-1">
        <span>Lento (0.2x)</span>
        <span>Normal (1.0x)</span>
        <span>Rápido (5.0x)</span>
      </div>
    </div>
  );
}
