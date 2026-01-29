import sqlite3

DB_NAME = "factory.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def setup_database():
    """Initializes the database with tables and dummy data."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # 1. Inventory Table (With Constraint)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY,
            item_name TEXT UNIQUE,
            stock_qty INTEGER CHECK(stock_qty >= 0)
        )
    """)
    
    # 2. Shipment Log (No Constraints)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS shipment_log (
            id INTEGER PRIMARY KEY,
            item_name TEXT,
            qty_moved INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Reset Data
    cursor.execute("DELETE FROM inventory")
    cursor.execute("DELETE FROM shipment_log")
    
    # Seed Data
    items = [
        ("Steel Bolts M10", 50),
        ("Titanium Alloy Sheets", 5),  # Low stock item
        ("Hydraulic Fluid (L)", 20)
    ]
    cursor.executemany("INSERT INTO inventory (item_name, stock_qty) VALUES (?, ?)", items)
    
    conn.commit()
    conn.close()
    print("Database Initialized.")