# Walmart Metrics: Retail Sales Analytics & Reporting Platform

## Overview

Walmart Metrics is an end-to-end retail analytics project that transforms raw transactional sales data into actionable business insights through data processing, API-driven analytics, and interactive dashboards.

The project combines data engineering, business intelligence, and reporting practices to support revenue analysis, sales trend monitoring, customer behavior analysis, and executive decision-making.

The solution includes:

* Data cleaning and transformation using Python and Pandas
* Structured data storage using SQLite
* REST API development using FastAPI
* Interactive reporting with Streamlit
* Business intelligence dashboards using Tableau
* KPI monitoring and trend analysis for business stakeholders

The objective was to simulate a real-world analytics workflow where raw retail transactions are transformed into reliable reporting assets for business users.

## Tech Stack

Python • Pandas • SQLite • FastAPI • Streamlit • Tableau • Matplotlib

---

## Business Objectives

The project was designed to answer key business questions:

* How is overall sales performance trending?
* Which product categories generate the highest revenue?
* Which branches contribute the most sales?
* What seasonal patterns impact revenue?
* Which payment methods drive the largest transaction volume?
* How do customer ratings vary across categories?
* What growth opportunities exist across time periods?

## Live Demo

🚀 Streamlit Dashboard  
https://walmart-metrics.onrender.com/

## Tableau Dashboards

📊 Executive Sales Dashboard  
https://public.tableau.com/views/WalmartSalesOverview_17808167397040/Dashboard1?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link

📈 Sales Trends & Seasonality Dashboard  
https://public.tableau.com/views/WalmartSalesTrends_17808168171460/Dashboard2?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link
## Dashboard Preview

### Executive Sales Dashboard
<img width="1470" height="956" alt="Screenshot 2026-06-14 at 6 04 14 PM" src="https://github.com/user-attachments/assets/c3454d73-1e24-42eb-a252-637ef33910cc" />

### Sales Trends Dashboard
<img width="1463" height="768" alt="Screenshot 2026-06-14 at 6 04 27 PM" src="https://github.com/user-attachments/assets/9144720a-b7a7-42a0-b072-88955e4df7f8" />


---

## Data Pipeline

<img width="1536" height="1024" alt="ChatGPT Image Jun 7, 2026, 01_34_33 PM" src="https://github.com/user-attachments/assets/9c735b28-6184-4fe1-a949-3594341ec7d4" />


### Data Ingestion

Raw retail transaction data was collected and processed through an ETL workflow.

### Data Cleaning

The dataset was standardized by:

* Handling missing values
* Removing invalid records
* Standardizing column names
* Validating date fields
* Converting numerical columns to appropriate formats

### Feature Engineering

Derived business metrics were created, including:

* Total Sales
* Revenue After Margin
* Profit Margin
* Average Order Value
* Category-Level Aggregations

### Storage Layer

Cleaned data was stored in a structured SQLite database to support reporting and API consumption.

---

## Analytics & Reporting

### Executive Sales Dashboard

Provides a high-level view of business performance through:

* Total Revenue
* Units Sold
* Customer Rating
* Transaction Volume
* Revenue by Category
* Branch Performance
* Payment Method Distribution

### Sales Trends & Seasonality Dashboard

Analyzes temporal performance patterns:

* Revenue by Year
* Revenue by Day of Week
* Month-over-Month Growth
* Revenue Heatmap
* Seasonal Performance Analysis

### Key Business Insights

* Revenue demonstrates strong year-end seasonality, with November and December consistently outperforming most months.
* Tuesday generates the highest weekly revenue, while Monday represents the lowest-performing sales day.
* Fashion Accessories and Home & Lifestyle contribute significantly to overall revenue performance.
* Revenue growth exhibits clear seasonal fluctuations, creating opportunities for targeted promotional campaigns.

---

## API Endpoints

| Endpoint          | Description              |
| ----------------- | ------------------------ |
| /                 | Service Health Check     |
| /metrics          | Global KPI Metrics       |
| /category-summary | Category-Level Analytics |

---

## 📁 Project Structure

```
Walmart-Metrics/
│
├── data/
│   ├── walmart_sales_data.csv
│   ├── sales_clean_data.csv
│   ├── walmart_dashboard_data.csv
│   └── walmart_sales.db
│
├── backend/
│   └── main.py
│
├── scripts/
│   └── create_clean_table.py
│
├── tableau/
│   ├── Executive_Sales_Monitoring.twbx
│   └── Sales_Trends_Seasonality.twbx
│
├── dashboard/
│   ├── streamlit_app.py
│   └── assets/
│
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Dashboard Highlights

### Dashboard 1: Walmart Sales Dashboard

Executive reporting dashboard focused on:

* Revenue Monitoring
* KPI Tracking
* Category Analysis
* Branch Performance
* Payment Method Insights

### Dashboard 2: Walmart Sales Trends

Trend-focused dashboard analyzing:

* Revenue Trends
* Seasonality Patterns
* Weekly Sales Behavior
* Growth Analysis

---

## How to Run

### Clone Repository

```bash
git clone <repository-url>
cd walmart-metrics
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Backend

```bash
uvicorn backend.main:app --reload
```

### Run Frontend

```bash
streamlit run app.py
```

---



## Future Enhancements

* Automated dashboard refresh pipelines
* Advanced customer segmentation
* Forecasting and predictive analytics
* Interactive drill-down reporting
* Cloud deployment and orchestration

