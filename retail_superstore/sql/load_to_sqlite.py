import pandas as pd
import sqlite3
from pathlib import Path

# Paths
root = Path(__file__).resolve().parents[1]   # retail_superstore/
csv_path = root / "data" / "superstore.csv"
db_path = root / "retail_superstore.db"

print(f"Loading CSV from: {csv_path}")
print(f"Creating DB at:    {db_path}")

# Read CSV
df = pd.read_csv(csv_path, encoding="latin1")
df["Order Date"] = pd.to_datetime(df["Order Date"])
df["Ship Date"] = pd.to_datetime(df["Ship Date"])

# Write to DB
con = sqlite3.connect(db_path)
df.to_sql("retail_superstore", con, if_exists="replace", index=False)
con.close()

print(f"Done! {len(df)} rows written to table 'retail_superstore'.")
