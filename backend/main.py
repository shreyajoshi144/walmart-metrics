import os
from fastapi import FastAPI
import sqlite3
import pandas as pd
app = FastAPI(title="Walmart Sales API")
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "walmart_sales.db")

if not os.path.exists(DB_PATH):
    raise FileNotFoundError("Database not found. Run ETL script first.")

def get_connection():
    return sqlite3.connect(DB_PATH)


@app.get("/")
def home():
    return {"message": "API Running 🚀"}


@app.get("/metrics")
def get_metrics():
    conn = get_connection()
    df = pd.read_sql("SELECT total_sales FROM SalesClean", conn)
    conn.close()

    return {
        "total_revenue": float(df["total_sales"].sum()),
        "total_orders": int(len(df)),
        "avg_order_value": float(df["total_sales"].mean())
    }


@app.get("/category-summary")
def category_summary():
    conn = get_connection()
    df = pd.read_sql("SELECT category, total_sales FROM SalesClean", conn)
    conn.close()

    summary = (
        df.groupby("category")
        .agg(
            revenue=("total_sales", "sum"),
            orders=("total_sales", "count"),
            avg_order_value=("total_sales", "mean")
        )
        .reset_index()
    )

    return summary.to_dict(orient="records")


@app.get("/category/{category_name}")
def category_detail(category_name: str):
    conn = get_connection()

    df = pd.read_sql(
        "SELECT date, total_sales FROM SalesClean WHERE category = ?",
        conn,
        params=(category_name,)
    )

    conn.close()

    if df.empty:
        return {"error": "No data found"}


    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"])

    if df.empty:
        return {"error": "No valid date data"}

    monthly = (
        df.set_index("date")
        .resample("M")["total_sales"]
        .sum()
        .reset_index()
    )

    return {
        "total_revenue": float(df["total_sales"].sum()),
        "total_orders": int(len(df)),
        "avg_order_value": float(df["total_sales"].mean()),
        "monthly_trend": monthly.to_dict(orient="records")
    }

# -------------------- PRODUCT SUMMARY --------------------
@app.get("/product-summary")
def product_summary():
    conn = get_connection()
    df = pd.read_sql("SELECT product_name, total_sales FROM SalesClean", conn)
    conn.close()

    summary = (
        df.groupby("product_name")
        .agg(
            revenue=("total_sales", "sum"),
            orders=("total_sales", "count"),
            avg_order_value=("total_sales", "mean")
        )
        .reset_index()
    )

    return summary.to_dict(orient="records")

# -------------------- FULL DATA FOR ANALYSIS --------------------
@app.get("/analysis-data")
def analysis_data():
    conn = get_connection()
    df = pd.read_sql(
        "SELECT date, category, unit_price, quantity, total_sales FROM SalesClean",
        conn
    )
    conn.close()

    return df.to_dict(orient="records")