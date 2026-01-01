import sqlite3
from pathlib import Path

db_path = Path(__file__).resolve().parents[1] / "retail_superstore.db"

con = sqlite3.connect(db_path)
cur = con.cursor()

cur.execute("SELECT COUNT(*) FROM retail_superstore;")
print("Row count:", cur.fetchone()[0])

cur.execute('SELECT "Category", ROUND(SUM("Profit"),2) FROM retail_superstore GROUP BY "Category";')
print("\nProfit by category:")
for row in cur.fetchall():
    print(row)

con.close()
