import csv
import json
import os
import random

def generate_layout_and_products():
    # Grid Dimensions
    rows = 40
    cols = 60

    # Ensure directories exist
    os.makedirs("backend/data", exist_ok=True)

    # 1. Generate grid representation
    # 0: EMPTY (Walkway)
    # 1: RACK_TC (Cold Zone Rack)
    # 2: RACK_DRY (Dry Zone Rack)
    # 3: DOCK_LOAD_TC
    # 4: DOCK_LOAD_DRY
    # 5: DOCK_UNLOAD_TC
    # 6: DOCK_UNLOAD_DRY
    # 7: STAGING
    # 8: WALL

    grid = [[0 for _ in range(cols)] for _ in range(rows)]

    # Draw border walls (Row 0, Row 39, Col 0, Col 59)
    for r in range(rows):
        grid[r][0] = 8
        grid[r][cols - 1] = 8
    for c in range(cols):
        grid[0][c] = 8
        grid[rows - 1][c] = 8

    # Place Docks on Row 0 (overwriting wall cells)
    # We will make them walkable in/out
    dock_load_tc_col = 10
    dock_unload_tc_col = 20
    dock_load_dry_col = 35
    dock_unload_dry_col = 45

    grid[0][dock_load_tc_col] = 3
    grid[0][dock_unload_tc_col] = 5
    grid[0][dock_load_dry_col] = 4
    grid[0][dock_unload_dry_col] = 6

    # Staging area for robots at the bottom (Row 37 and 38, near center)
    for c in range(25, 35):
        grid[rows - 2][c] = 7
        grid[rows - 3][c] = 7

    # Lay out Racks
    # Cold Zone (TC): Cols 2 to 25
    # Dry Zone (DRY): Cols 30 to 57
    # Vertical rack double columns, with walkway between them
    tc_rack_cols = [2, 3, 5, 6, 8, 9, 11, 12, 14, 15, 17, 18, 20, 21, 23, 24]
    dry_rack_cols = [30, 31, 33, 34, 36, 37, 39, 40, 42, 43, 45, 46, 48, 49, 51, 52, 54, 55, 57, 58]

    # Row intervals for racks to allow horizontal walkways
    rack_row_ranges = [
        range(4, 12),   # Segment 1 (rows 4 to 11)
        range(13, 24),  # Segment 2 (rows 13 to 23)
        range(25, 35)   # Segment 3 (rows 25 to 34)
    ]

    tc_racks = []
    dry_racks = []

    for c in tc_rack_cols:
        for r_range in rack_row_ranges:
            for r in r_range:
                grid[r][c] = 1
                tc_racks.append(f"TC-R{r}-C{c}")

    for c in dry_rack_cols:
        for r_range in rack_row_ranges:
            for r in r_range:
                grid[r][c] = 2
                dry_racks.append(f"DRY-R{r}-C{c}")

    # Write Layout JSON
    layout_data = {
        "rows": rows,
        "cols": cols,
        "grid": grid,
        "tc_racks": tc_racks,
        "dry_racks": dry_racks,
        "docks": {
            "LOAD_TC": {"row": 0, "col": dock_load_tc_col, "type": 3},
            "UNLOAD_TC": {"row": 0, "col": dock_unload_tc_col, "type": 5},
            "LOAD_DRY": {"row": 0, "col": dock_load_dry_col, "type": 4},
            "UNLOAD_DRY": {"row": 0, "col": dock_unload_dry_col, "type": 6}
        },
        "staging": [{"row": r, "col": c} for r in range(rows - 3, rows - 1) for c in range(25, 35)]
    }

    with open("backend/data/warehouse_layout.json", "w") as f:
        json.dump(layout_data, f, indent=2)

    # 2. Generate products CSV
    random.seed(42)

    categories_tc = ["lacteos", "carnes", "congelados", "farmacia", "bebidas_frias"]
    categories_dry = ["limpieza", "abarrotes", "snacks", "electro", "hogar", "juguetes", "libros"]

    product_names_tc = [
        "Leche UHT 1L", "Jugo Naranja 2L", "Yogurt Natural 1kg", "Queso Edam 500g",
        "Mantequilla con sal 200g", "Salchicha Viena x10", "Pechuga de Pollo 1kg",
        "Lomo de Cerdo 1kg", "Helado de Vainilla 1L", "Papas Fritas Congeladas 1kg",
        "Vacuna Gripe A", "Insulina Rápida", "Suero Fisiológico", "Bebida Energética 500ml",
        "Cerveza Premium 6pack", "Agua Mineral Fria 1.5L"
    ]
    product_names_dry = [
        "Papel Toalla x6", "Detergente Líquico 3L", "Jabón Lavavajillas 500ml", "Arroz Extra 5kg",
        "Azúcar Rubia 1kg", "Fideos Tallarín 500g", "Aceite Vegetal 1L", "Atún en Conserva 170g",
        "Galletas de Soda x12", "Papas Pringles Original", "Ch chocolates Milk 100g", "Café Instantáneo 200g",
        "Té Filtrante 100un", "Audífonos Bluetooth", "Cargador Carga Rápida", "Sartén Antiadherente 24cm",
        "Toalla de Baño", "Set de Cubiertos x24", "Muñeca de Moda", "Bloques de Construcción",
        "Libro Novela Ficción", "Cuaderno Espiral A4"
    ]

    total_products = 1500
    products = []

    for i in range(1, total_products + 1):
        sku = f"SKU-{i:04d}"
        
        # Decide zone based on a simple split or random choice
        # Let's say ~40% TC, ~60% DRY to match rack capacities roughly
        is_tc = random.random() < 0.4
        
        if is_tc:
            zona = "TC"
            categoria = random.choice(categories_tc)
            nombre = f"{random.choice(product_names_tc)} #{random.randint(10, 99)}"
            rack_id = random.choice(tc_racks)
            peso = round(random.uniform(0.1, 5.0), 2)
            cantidad = random.randint(10, 250)
        else:
            zona = "DRY"
            categoria = random.choice(categories_dry)
            nombre = f"{random.choice(product_names_dry)} #{random.randint(10, 99)}"
            rack_id = random.choice(dry_racks)
            peso = round(random.uniform(0.05, 15.0), 2)
            cantidad = random.randint(5, 500)
            
        products.append({
            "sku": sku,
            "nombre": nombre,
            "zona": zona,
            "rack_id": rack_id,
            "cantidad": cantidad,
            "peso_kg": peso,
            "categoria": categoria
        })

    with open("backend/data/products.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["sku", "nombre", "zona", "rack_id", "cantidad", "peso_kg", "categoria"])
        writer.writeheader()
        writer.writerows(products)

    print(f"Generated warehouse layout with {len(tc_racks)} Cold racks and {len(dry_racks)} Dry racks.")
    print(f"Generated {total_products} products in backend/data/products.csv.")

if __name__ == "__main__":
    generate_layout_and_products()
