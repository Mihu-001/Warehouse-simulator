import React from 'react';
import { CELL_COLORS, ROBOT_COLORS, PATH_COLORS } from '../utils/colors';

export default function Legend() {
  return (
    <div className="bg-white/5 border border-white/5 rounded-2xl p-4 backdrop-blur-md space-y-3.5">
      <div>
        <h2 className="text-[10px] font-bold text-white/40 uppercase tracking-widest mb-2.5">Leyenda de Almacén</h2>
        <div className="grid grid-cols-2 gap-2 text-[9px]">
          <div className="flex items-center gap-2">
            <span className="w-2.5 h-2.5 rounded shrink-0" style={{ backgroundColor: CELL_COLORS[0] }} />
            <span className="text-white/70">Pasillo Walkway</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="w-2.5 h-2.5 rounded shrink-0" style={{ backgroundColor: CELL_COLORS[8] }} />
            <span className="text-white/70">Muro Perímetro</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="w-2.5 h-2.5 rounded shrink-0" style={{ backgroundColor: CELL_COLORS[1] }} />
            <span className="text-white/70">Rack TC (Frio)</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="w-2.5 h-2.5 rounded shrink-0" style={{ backgroundColor: CELL_COLORS[2] }} />
            <span className="text-white/70">Rack DRY (Seco)</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="w-2.5 h-2.5 rounded shrink-0" style={{ backgroundColor: CELL_COLORS[3] }} />
            <span className="text-white/70">Dock TC (Ingreso)</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="w-2.5 h-2.5 rounded shrink-0" style={{ backgroundColor: CELL_COLORS[5] }} />
            <span className="text-white/70">Dock TC (Salida)</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="w-2.5 h-2.5 rounded shrink-0" style={{ backgroundColor: CELL_COLORS[4] }} />
            <span className="text-white/70">Dock DRY (Ingreso)</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="w-2.5 h-2.5 rounded shrink-0" style={{ backgroundColor: CELL_COLORS[6] }} />
            <span className="text-white/70">Dock DRY (Salida)</span>
          </div>
          <div className="flex items-center gap-2 col-span-2">
            <span className="w-2.5 h-2.5 rounded shrink-0" style={{ backgroundColor: CELL_COLORS[7] }} />
            <span className="text-white/70">Área Staging (Parqueo Robots)</span>
          </div>
        </div>
      </div>

      <div className="border-t border-white/5 pt-2.5">
        <h2 className="text-[10px] font-bold text-white/40 uppercase tracking-widest mb-2.5">Estados de Robots</h2>
        <div className="grid grid-cols-2 gap-2 text-[9px]">
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full ring-2 ring-offset-1 ring-offset-[#1a1a2e]" style={{ backgroundColor: ROBOT_COLORS.IDLE, borderColor: ROBOT_COLORS.IDLE }} />
            <span className="text-white/70">Resting (IDLE)</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full ring-2 ring-offset-1 ring-offset-[#1a1a2e]" style={{ backgroundColor: ROBOT_COLORS.MOVING_TO_PRODUCT, borderColor: ROBOT_COLORS.MOVING_TO_PRODUCT }} />
            <span className="text-white/70">Al producto</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full ring-2 ring-offset-1 ring-offset-[#1a1a2e]" style={{ backgroundColor: ROBOT_COLORS.PICKING, borderColor: ROBOT_COLORS.PICKING }} />
            <span className="text-white/70">Picking (Recojo)</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full ring-2 ring-offset-1 ring-offset-[#1a1a2e]" style={{ backgroundColor: ROBOT_COLORS.MOVING_TO_DOCK, borderColor: ROBOT_COLORS.MOVING_TO_DOCK }} />
            <span className="text-white/70">Al camión (Dock)</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full ring-2 ring-offset-1 ring-offset-[#1a1a2e]" style={{ backgroundColor: ROBOT_COLORS.RETURNING, borderColor: ROBOT_COLORS.RETURNING }} />
            <span className="text-white/70">Retornando</span>
          </div>
        </div>
      </div>

      <div className="border-t border-white/5 pt-2.5">
        <h2 className="text-[10px] font-bold text-white/40 uppercase tracking-widest mb-2">Trazado de Rutas</h2>
        <div className="flex gap-4 text-[9px]">
          <div className="flex items-center gap-1.5">
            <span className="w-4 h-0.5 border-t-2 border-dashed" style={{ borderColor: PATH_COLORS.astar }} />
            <span className="text-white/70">A*</span>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="w-4 h-0.5 border-t-2 border-dashed" style={{ borderColor: PATH_COLORS.dijkstra }} />
            <span className="text-white/70">Dijkstra</span>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="w-4 h-0.5 border-t-2 border-dashed" style={{ borderColor: PATH_COLORS.bfs }} />
            <span className="text-white/70">BFS</span>
          </div>
        </div>
      </div>
    </div>
  );
}
