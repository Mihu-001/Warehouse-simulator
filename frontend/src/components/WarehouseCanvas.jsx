import React, { useRef, useState } from 'react';
import useCanvasRenderer from '../hooks/useCanvasRenderer';
import { CELL_COLORS, ROBOT_COLORS, PATH_COLORS } from '../utils/colors';
import { getRackIdAt, gridToPx, pxToGrid } from '../utils/gridHelpers';

export default function WarehouseCanvas({ grid, robots, stats, rackInventories, docks, onRackClick, onRobotCancel }) {
  const canvasRef = useRef(null);
  const CELL = 16; // 16px per cell * 60 = 960px width, * 40 = 640px height

  // Tooltip state
  const [tooltip, setTooltip] = useState({
    visible: false,
    x: 0,
    y: 0,
    type: null, // "RACK" | "ROBOT"
    data: null
  });

  // Canvas drawing loop
  useCanvasRenderer(canvasRef, () => {
    const canvas = canvasRef.current;
    if (!canvas || grid.length === 0) return;
    const ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // 1. Draw Grid Cells
    for (let r = 0; r < grid.length; r++) {
      for (let c = 0; c < grid[r].length; c++) {
        const cell = grid[r][c];
        ctx.fillStyle = CELL_COLORS[cell] || '#111827';
        ctx.fillRect(c * CELL, r * CELL, CELL - 0.5, CELL - 0.5);

        // Draw small grid dots for racks to simulate packages
        if (cell === 1 || cell === 2) {
          drawRackProducts(ctx, c, r, cell);
        }
      }
    }

    // 2. Draw Dotted Paths
    const activeAlgo = stats.algorithm || 'astar';
    robots.forEach(robot => {
      if (robot.path && robot.path.length > 0) {
        drawDottedPath(ctx, robot, activeAlgo);
      }
    });

    // 3. Draw Robots
    robots.forEach(robot => {
      drawRobot(ctx, robot);
    });

    // 4. Draw Trucks at Docks
    drawTrucks(ctx);

  }, [grid, robots, stats, docks]);

  // Renders small box graphics inside rack cells to show inventory fills
  const drawRackProducts = (ctx, col, row, type) => {
    const rackId = getRackIdAt(row, col, type);
    const inv = rackInventories[rackId];
    if (!inv || inv.qty <= 0) return;

    // Draw little colorful squares inside the cell representing items
    const startX = col * CELL + 2;
    const startY = row * CELL + 2;
    const innerSize = CELL - 4;

    ctx.fillStyle = type === 1 ? '#3b82f6' : '#f97316'; // blue for TC, orange for DRY
    
    if (inv.qty > 100) {
      // Draw 3 miniature squares (full rack)
      ctx.fillRect(startX, startY, innerSize / 2 - 0.5, innerSize / 2 - 0.5);
      ctx.fillRect(startX + innerSize / 2, startY, innerSize / 2 - 0.5, innerSize / 2 - 0.5);
      ctx.fillRect(startX, startY + innerSize / 2, innerSize / 2 - 0.5, innerSize / 2 - 0.5);
    } else if (inv.qty > 30) {
      // Draw 2 squares (medium fill)
      ctx.fillRect(startX, startY, innerSize / 2 - 0.5, innerSize - 1);
      ctx.fillRect(startX + innerSize / 2, startY, innerSize / 2 - 0.5, innerSize - 1);
    } else {
      // Draw 1 square (low fill)
      ctx.fillRect(startX + 2, startY + 2, innerSize - 4, innerSize - 4);
    }
  };

  const drawDottedPath = (ctx, robot, algo) => {
    ctx.beginPath();
    // Start at robot's current float position for a connected path line
    const rY = robot.row * CELL + CELL / 2;
    const rX = robot.col * CELL + CELL / 2;
    ctx.moveTo(rX, rY);

    robot.path.forEach(cell => {
      const cY = cell[0] * CELL + CELL / 2;
      const cX = cell[1] * CELL + CELL / 2;
      ctx.lineTo(cX, cY);
    });

    ctx.strokeStyle = PATH_COLORS[algo] || '#ffffff';
    ctx.lineWidth = 1.5;
    ctx.setLineDash([3, 3]);
    ctx.stroke();
    ctx.setLineDash([]); // Reset
  };

  const drawRobot = (ctx, robot) => {
    const rY = robot.row * CELL + CELL / 2;
    const rX = robot.col * CELL + CELL / 2;
    const radius = CELL * 0.45;

    // Outer glow ring
    ctx.beginPath();
    ctx.arc(rX, rY, radius + 2, 0, 2 * Math.PI);
    ctx.strokeStyle = ROBOT_COLORS[robot.state] || '#ffffff';
    ctx.lineWidth = 1;
    ctx.stroke();

    // Body
    ctx.beginPath();
    ctx.arc(rX, rY, radius, 0, 2 * Math.PI);
    ctx.fillStyle = '#090a0f';
    ctx.fill();
    ctx.strokeStyle = ROBOT_COLORS[robot.state] || '#ffffff';
    ctx.lineWidth = 2;
    ctx.stroke();

    // Inner state indicator dot
    ctx.beginPath();
    ctx.arc(rX, rY, radius * 0.4, 0, 2 * Math.PI);
    ctx.fillStyle = ROBOT_COLORS[robot.state] || '#ffffff';
    ctx.fill();

    // Draw little box inside robot if carrying product
    if (robot.carrying) {
      ctx.fillStyle = '#f59e0b';
      ctx.fillRect(rX - 3, rY - 3, 6, 6);
      ctx.strokeStyle = '#ffffff';
      ctx.lineWidth = 0.5;
      ctx.strokeRect(rX - 3, rY - 3, 6, 6);
    }

    // Robot Label (text inside)
    ctx.fillStyle = '#ffffff';
    ctx.font = 'bold 8px monospace';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    // Draw offset to make it visible
    ctx.fillText(robot.id, rX, rY - radius - 4);
  };

  const drawTrucks = (ctx) => {
    // Docks column offsets: TC Load (10), TC Unload (20), Dry Load (35), Dry Unload (45)
    const truckCols = [10, 20, 35, 45];
    
    truckCols.forEach(col => {
      // Draw a cute truck cargo block at the top
      const x = col * CELL;
      const y = 0; // Row 0
      
      // Check dock status if available
      let dockKey = "";
      if (col === 10) dockKey = "LOAD_TC";
      else if (col === 20) dockKey = "UNLOAD_TC";
      else if (col === 35) dockKey = "LOAD_DRY";
      else if (col === 45) dockKey = "UNLOAD_DRY";
      
      const progress = docks[dockKey];
      const fillPercent = progress ? (progress.loaded / progress.capacity) : 0;

      // Draw truck cab
      ctx.fillStyle = '#4b5563';
      ctx.fillRect(x + CELL * 0.1, y + 2, CELL * 0.8, 4);
      
      // Draw truck cargo body
      ctx.fillStyle = '#374151';
      ctx.fillRect(x - 2, y + 6, CELL + 4, 8);
      ctx.strokeStyle = '#9ca3af';
      ctx.strokeRect(x - 2, y + 6, CELL + 4, 8);

      // Draw loading bar inside truck body
      if (fillPercent > 0) {
        ctx.fillStyle = '#10b981'; // Green fill
        ctx.fillRect(x - 1, y + 7, (CELL + 2) * fillPercent, 6);
      }
    });
  };

  // Click & hover mouse interaction
  const handleMouseMove = (e) => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    const col = pxToGrid(x, CELL);
    const row = pxToGrid(y, CELL);

    // 1. Check if hovering a Robot (check distance < 0.7 tiles to match float movement)
    let hoveredRobot = null;
    for (const robot of robots) {
      const dist = Math.sqrt((robot.row - row) ** 2 + (robot.col - col) ** 2);
      if (dist < 0.8) {
        hoveredRobot = robot;
        break;
      }
    }

    if (hoveredRobot) {
      setTooltip({
        visible: true,
        x: e.clientX - rect.left + 15,
        y: e.clientY - rect.top + 15,
        type: 'ROBOT',
        data: hoveredRobot
      });
      return;
    }

    // 2. Check if hovering a Rack cell
    if (grid[row] && (grid[row][col] === 1 || grid[row][col] === 2)) {
      const rackId = getRackIdAt(row, col, grid[row][col]);
      const inv = rackInventories[rackId] || { qty: 0, skus: [], names: [], category: 'N/A' };
      
      setTooltip({
        visible: true,
        x: e.clientX - rect.left + 15,
        y: e.clientY - rect.top + 15,
        type: 'RACK',
        data: {
          id: rackId,
          type: grid[row][col] === 1 ? 'TC (Frío)' : 'DRY (Seco)',
          ...inv
        }
      });
      return;
    }

    // 3. Clear tooltip if hovering empty space
    setTooltip(t => ({ ...t, visible: false }));
  };

  const handleMouseLeave = () => {
    setTooltip(t => ({ ...t, visible: false }));
  };

  const handleClick = (e) => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const rect = canvas.getBoundingClientRect();
    const col = pxToGrid(e.clientX - rect.left, CELL);
    const row = pxToGrid(e.clientY - rect.top, CELL);

    if (grid[row] && (grid[row][col] === 1 || grid[row][col] === 2)) {
      const rackId = getRackIdAt(row, col, grid[row][col]);
      onRackClick(rackId);
    }
  };

  const handleContextMenu = (e) => {
    e.preventDefault();
    const canvas = canvasRef.current;
    if (!canvas) return;

    const rect = canvas.getBoundingClientRect();
    const col = pxToGrid(e.clientX - rect.left, CELL);
    const row = pxToGrid(e.clientY - rect.top, CELL);

    // Find if user right-clicked near a robot
    let clickedRobot = null;
    for (const robot of robots) {
      const dist = Math.sqrt((robot.row - row) ** 2 + (robot.col - col) ** 2);
      if (dist < 1.0) {
        clickedRobot = robot;
        break;
      }
    }

    if (clickedRobot) {
      onRobotCancel(clickedRobot.id);
    }
  };

  return (
    <div className="relative border border-white/5 bg-[#0b0c10] rounded-2xl overflow-hidden shadow-2xl shadow-black/50 select-none">
      <canvas
        ref={canvasRef}
        width={960}
        height={640}
        onMouseMove={handleMouseMove}
        onMouseLeave={handleMouseLeave}
        onClick={handleClick}
        onContextMenu={handleContextMenu}
        className="block cursor-crosshair"
      />

      {/* Tooltip Overlay */}
      {tooltip.visible && (
        <div
          className="absolute z-50 pointer-events-none rounded-xl border border-white/10 bg-[#161b26]/90 p-3 shadow-xl backdrop-blur-md transition-all duration-75 text-xs w-56 text-white"
          style={{ left: tooltip.x, top: tooltip.y }}
        >
          {tooltip.type === 'ROBOT' ? (
            <div className="space-y-1.5">
              <div className="flex justify-between items-center border-b border-white/10 pb-1 mb-1">
                <span className="font-bold text-blue-400">Robot {tooltip.data.id}</span>
                <span className="text-[10px] uppercase font-semibold px-1.5 py-0.5 rounded bg-white/10" style={{ color: ROBOT_COLORS[tooltip.data.state] }}>
                  {tooltip.data.state.replace(/_/g, ' ')}
                </span>
              </div>
              <p><span className="text-white/50">Carga:</span> {tooltip.data.carrying || 'Vacio'}</p>
              <p><span className="text-white/50">Origen:</span> {tooltip.data.target_rack || 'Ninguno'}</p>
              <p><span className="text-white/50">Destino:</span> {tooltip.data.target_dock || 'Ninguno'}</p>
              <p><span className="text-white/50 text-[10px]">Restan:</span> <span className="font-semibold text-amber-400">{tooltip.data.path?.length || 0} casillas</span></p>
            </div>
          ) : (
            <div className="space-y-1.5">
              <div className="flex justify-between items-center border-b border-white/10 pb-1 mb-1">
                <span className="font-bold text-amber-400">{tooltip.data.id}</span>
                <span className="text-[10px] uppercase font-semibold px-1.5 py-0.5 rounded bg-white/10 text-white/70">
                  {tooltip.data.type}
                </span>
              </div>
              <p><span className="text-white/50">Categoría:</span> <span className="capitalize">{tooltip.data.category}</span></p>
              <p><span className="text-white/50">Capacidad Total:</span> <span className="font-bold">{tooltip.data.qty} un</span></p>
              {tooltip.data.names.length > 0 && (
                <div className="border-t border-white/5 pt-1 mt-1">
                  <p className="text-[10px] text-white/50 mb-0.5">Productos en rack:</p>
                  <ul className="list-disc pl-3 text-[10px] text-white/80 space-y-0.5">
                    {tooltip.data.names.map((name, i) => (
                      <li key={i} className="truncate">{name}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
