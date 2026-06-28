import asyncio
import time
from typing import Set
import os
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
import networkx as nx

from backend.core.sim_engine import SimEngine

app = FastAPI(title="Amazon Smart Warehouse Simulator API")

# Allow all origins for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global simulation engine instance
engine = SimEngine()

@app.get("/")
def get_root():
    cdn_path = "frontend/index_cdn.html"
    if os.path.exists(cdn_path):
        return FileResponse(cdn_path)
    return {"message": "Amazon Smart Warehouse Simulator API is running. Direct HTML not found."}


# Active WebSocket connections
active_connections: Set[WebSocket] = set()

# Background simulation task
sim_task = None

async def broadcast_state():
    """
    Ticks the simulation and broadcasts the state update to all active connections.
    """
    last_tick = time.perf_counter()
    while True:
        try:
            now = time.perf_counter()
            dt = now - last_tick
            last_tick = now
            
            # Tick the engine (respects speed multiplier internally)
            engine.tick(dt)
            
            if active_connections:
                state = engine.get_state()
                # Gather tasks to send to all connections in parallel
                tasks = [connection.send_json(state) for connection in list(active_connections)]
                await asyncio.gather(*tasks, return_exceptions=True)
                
        except Exception as e:
            print(f"Error in simulation ticker loop: {e}")
            
        await asyncio.sleep(0.05)  # 20 ticks per second

@app.on_event("startup")
async def startup_event():
    global sim_task
    sim_task = asyncio.create_task(broadcast_state())
    print("Simulation background ticker started.")

@app.on_event("shutdown")
async def shutdown_event():
    if sim_task:
        sim_task.cancel()
        print("Simulation background ticker stopped.")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.add(websocket)
    print(f"WebSocket client connected. Total: {len(active_connections)}")
    
    # Send immediate initial state
    try:
        await websocket.send_json(engine.get_state())
    except Exception:
        pass
        
    try:
        while True:
            data = await websocket.receive_json()
            
            msg_type = data.get("type")
            if msg_type == "CLICK_RACK":
                engine.assign_order(data.get("rack_id"))
                
            elif msg_type == "CHANGE_ALGO":
                engine.change_algorithm(data.get("algo"))
                
            elif msg_type == "SET_SPEED":
                # Ensure speed is a positive float
                try:
                    speed = max(0.1, min(10.0, float(data.get("value", 1.0))))
                    engine.speed_multiplier = speed
                except (ValueError, TypeError):
                    pass
                    
            elif msg_type == "ADD_RANDOM_ORDER":
                engine.assign_random_order()
                
            elif msg_type == "RESET":
                engine.reset()
                
            elif msg_type == "CANCEL_ROBOT":
                engine.cancel_robot(data.get("robot_id"))
                
    except WebSocketDisconnect:
        print("WebSocket client disconnected.")
    except Exception as e:
        print(f"Error in client WebSocket handler: {e}")
    finally:
        active_connections.remove(websocket)
        print(f"WebSocket client removed. Remaining: {len(active_connections)}")

@app.get("/api/graph/export")
def export_graph(zone: str = None):
    """
    Exports the warehouse graph in NetworkX node-link JSON format.
    Allows filtering by zone: 'TC' or 'DRY'.
    """
    try:
        if zone == "TC":
            G = engine.grid.get_subgraph_by_zone("TC")
        elif zone == "DRY":
            G = engine.grid.get_subgraph_by_zone("DRY")
        else:
            G = engine.grid.to_networkx_graph()
            
        data = nx.node_link_data(G)
        
        # We can also add quick report summary metrics
        summary = {
            "total_nodes": G.number_of_nodes(),
            "total_edges": G.number_of_edges(),
            "graph_data": data
        }
        
        headers = {
            "Content-Disposition": f"attachment; filename=warehouse_graph_{zone or 'full'}.json"
        }
        return JSONResponse(content=summary, headers=headers)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
