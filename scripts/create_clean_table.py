import sqlite3
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "data", "walmart_sales.db")

conn = sqlite3.connect(DB_PATH)

df = pd.read_sql_query("SELECT * FROM SalesRaw", conn)

# CLEANING
df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

df['unit_price'] = pd.to_numeric(df['unit_price'], errors='coerce')
df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce')

df['total_sales'] = df['quantity'] * df['unit_price']

df['date'] = pd.to_datetime(df['date'], errors='coerce')

df.dropna(subset=['date', 'category', 'total_sales'], inplace=True)

df.to_sql('SalesClean', conn, if_exists='replace', index=False)

print("✅ Clean table created")

conn.close()