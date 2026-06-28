# 🏭 Warehouse Simulator

Simulador de almacén inteligente con robots autónomos que usan algoritmos de búsqueda de caminos (A*, Dijkstra, BFS) para recoger y entregar productos.

**Curso**: Complejidad Algorítmica · 1ACC0184

---

## 📋 Requisitos

- **Python 3.10+** → [Descargar Python](https://www.python.org/downloads/)

> No necesitas Node.js. El frontend se sirve directamente desde el backend.

---

## 🚀 Cómo ejecutar

### 1. Instalar dependencias

```bash
pip install fastapi uvicorn websockets networkx
```

### 2. Generar datos (solo la primera vez o si quieres regenerar)

```bash
python -m backend.generate_data
```

### 3. Iniciar el servidor

```bash
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

### 4. Abrir en el navegador

```
http://localhost:8000
```

---

## 🎮 Controles

| Acción | Cómo |
|--------|------|
| Asignar pedido | Click izquierdo en un rack |
| Pedido aleatorio | Botón "+ Pedido Aleatorio" |
| Cancelar orden | Click derecho en un robot |
| Cambiar algoritmo | Botones A* / Dijkstra / BFS |
| Velocidad | Slider de velocidad |
| Reiniciar | Botón "↺ Reiniciar" |
| Exportar grafo | Botones "Completo / TC / DRY" |

---

## 📁 Estructura del Proyecto

```
Warehouse simulator/
├── backend/
│   ├── main.py              # Servidor FastAPI + WebSocket
│   ├── generate_data.py     # Generador de layout y productos
│   ├── requirements.txt
│   ├── algorithms/
│   │   ├── astar.py         # A* con heurística Manhattan
│   │   ├── dijkstra.py      # Dijkstra (A* sin heurística)
│   │   ├── bfs.py           # Búsqueda en anchura
│   │   └── utils.py         # Validación de celdas transitables
│   ├── core/
│   │   ├── sim_engine.py    # Motor de simulación principal
│   │   ├── grid.py          # Grilla del almacén + grafo NetworkX
│   │   ├── robot.py         # Lógica de robots
│   │   ├── order_queue.py   # Cola de prioridad de pedidos
│   │   └── dock.py          # Muelles de carga/descarga
│   ├── utils/
│   │   └── stats.py         # Métricas y exportación CSV
│   └── data/
│       ├── warehouse_layout.json
│       ├── products.csv
│       └── simulation_session.csv
└── frontend/
    ├── index_cdn.html        # Frontend standalone (se sirve desde el backend)
    └── src/                  # Código fuente React (requiere Node.js)
```

---

## 🧠 Algoritmos Implementados

| Algoritmo | Complejidad Temporal | Heurística | Óptimo |
|-----------|---------------------|------------|--------|
| **A\***   | O(E log V)          | Manhattan  | ✅ Sí  |
| **Dijkstra** | O(E log V)       | Ninguna    | ✅ Sí  |
| **BFS**   | O(V + E)            | Ninguna    | ✅ Sí (peso uniforme) |
