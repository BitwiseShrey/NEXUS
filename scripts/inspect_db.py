import sqlite3
import os

db_path = os.path.join("data", "nexus.db")
print("Connecting to:", db_path)
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = [r[0] for r in cursor.fetchall()]
print(f"Total tables: {len(tables)}")
print("Tables:", tables)

for t in sorted(tables):
    cursor.execute(f"SELECT count(*) FROM {t}")
    count = cursor.fetchone()[0]
    print(f"  {t}: {count:,} rows")

# Check specific entities
print("\n--- Digital Twin Entities Verification ---")
for t in ["suppliers", "production_units", "warehouses", "distribution_hubs", "demand_zones", "corridors", "products", "inventory", "orders", "disruptions", "forecasts", "risk_events", "optimization_runs", "recommendations"]:
    if t in tables:
        cursor.execute(f"SELECT count(*) FROM {t}")
        print(f"  {t}: {cursor.fetchone()[0]}")
    else:
        print(f"  {t}: NOT FOUND")

conn.close()
