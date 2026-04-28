# 📊 Walmart Metrics

## 🚀 Project Overview

Walmart Metrics is a data pipeline and API-driven analytics system designed to process raw retail sales data into structured, queryable insights.

The project focuses on building a clean **data engineering + backend workflow**, where raw transactional data is transformed using Pandas, validated and stored in a relational database (SQLite), and exposed through RESTful APIs using FastAPI.

Instead of relying on unreliable dimensions (such as inconsistent timestamps or missing hierarchies), the system is intentionally designed around **robust, high-quality features (category-level aggregation)** to ensure stability, correctness, and meaningful insights.

Key highlights of the system include:

* End-to-end **data pipeline (raw → cleaned → structured storage)**
* Efficient **aggregation queries at the database/API layer**
* Clean separation of concerns between **data processing, storage, and serving**
* Lightweight but scalable **API-first architecture**

The frontend dashboard serves as a thin visualization layer, consuming backend APIs to display results, while the core logic and computation remain within the backend.


## 🧱 Architecture Pipeline & Flow

<img width="1536" height="1024" alt="ChatGPT Image Apr 28, 2026, 11_13_12 PM" src="https://github.com/user-attachments/assets/7264801d-4a46-4c4a-980e-41cf6bd62786" />


## 🔧 Tech Stack

* **Python**
* **Pandas** – data cleaning & transformation
* **SQLite** – lightweight database
* **FastAPI** – backend API layer
* **Streamlit** – frontend dashboard
* **Matplotlib** – visualizations

---

## ⚙️ Features

### 📌 Data Pipeline

* Ingested raw transactional data from source tables
* Performed structured data cleaning using Pandas
* Generated derived metrics such as `total_sales`
* Validated and removed inconsistent / invalid records
* Stored processed data in a normalized SQLite table (`SalesClean`)

---

### 🧠 Data Modeling & Aggregation

* Designed category-level aggregation logic
* Computed:

  * Total revenue per category
  * Order counts per category
  * Average order value
* Ensured aggregations are performed at the backend layer (not frontend)

---

### 🌐 Backend (FastAPI)

* Built RESTful APIs to expose processed data
* Implemented endpoints for:

  * Global metrics (`/metrics`)
  * Category-level summaries (`/category-summary`)
* Separated data access, computation, and API layers
* Designed lightweight and efficient query handling using SQLite

---

### 🖥️ Frontend (Streamlit)

* Acts as a thin client consuming backend APIs
* Displays aggregated insights without performing heavy computation
* Supports category-level comparison and filtering

---

## 🧪 Data Processing

Handled via a dedicated ETL script:

* Standardized column names for consistency
* Converted numeric fields (`quantity`, `unit_price`)
* Created derived metric: `total_sales = quantity × unit_price`
* Converted and validated date fields (with error handling)
* Removed invalid/null records to ensure clean dataset
* Persisted processed data into `SalesClean` table

---

## 🌐 API Endpoints

| Endpoint            | Description                        |
| ------------------- | ---------------------------------- |
| `/`                 | Service health check               |
| `/metrics`          | Global aggregated KPIs             |
| `/category-summary` | Category-level aggregated insights |

---

## 📊 Visualization Layer

* Category comparison (bar chart)
* Revenue distribution (pie chart)
* Summary tables for quick inspection

> Note: All computations are handled in the backend; the frontend is used only for visualization.

## ▶️ How to Run

### 1. Clone repo

```
git clone <your-repo>
cd project-folder
```

### 2. Install dependencies

```
pip install -r requirements.txt
```

### 3. Run backend

```
uvicorn backend.main:app --reload
```

### 4. Run frontend

```
streamlit run app.py
```

---

## 📁 Project Structure

```
project/
│
├── backend/
│   └── main.py
│
├── scripts/
│   └── create_clean_table.py
│
├── data/
│   └── walmart_sales.db
│
├── app.py
├── requirements.txt
└── README.md
```

---

## 💡 Key Learnings

* Built a full data pipeline from raw data → dashboard
* Implemented API-driven architecture
* Learned to align features with dataset limitations
* Focused on clean, stable, and explainable design

---

## 🚀 Future Improvements

* Add time-based filtering (if dataset improves)
* Improve dataset quality for deeper insights

---

## 📌 Summary

This project demonstrates how to build a **complete data analytics system** using:

* Data cleaning
* Database storage
* REST API backend
* Interactive frontend dashboard

All designed around **realistic constraints of the dataset**.
