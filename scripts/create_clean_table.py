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
=======

# Connect to the SQL database
conn = sqlite3.connect('/Users/shreyajoshi/Downloads/Walmart_Sales_Insights/data/walmart_sales.db')

# Load raw data from SalesRaw
df = pd.read_sql_query("SELECT * FROM SalesRaw", conn)

# CLEANING
# Standardize column names
df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

# Ensure numeric columns are correct
df['unit_price'] = pd.to_numeric(df['unit_price'], errors='coerce').fillna(0)
df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce').fillna(0)
df['total_sales'] = df['quantity'] * df['unit_price']

# Convert date column
df['date'] = pd.to_datetime(df['date'], format='%m/%d/%Y', errors='coerce')

# Fill missing categorical values
df['product_name'] = df['product_name'].fillna('Unknown')
df['category'] = df['category'].fillna('Unknown')

# WRITE CLEAN TABLE
df.to_sql('SalesClean', conn, if_exists='replace', index=False)

print("Clean SQL table 'SalesClean' created successfully in 'walmart_sales.db'!")

conn.close()

