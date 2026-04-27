from fastapi import FastAPI
import sqlite3
import pandas as pd

app = FastAPI(title="Walmart Sales API")

DB_PATH = "data/walmart_sales.db"

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

        df["date"] = pd.to_datetime(df["date"])

        # 🔥 Monthly trend
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
        return df.to_dict(orient="records")
    return summary.to_dict(orient="records")