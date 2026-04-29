import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import os
# -------------------- CONFIG --------------------
st.set_page_config(
    page_title="Walmart Sales Dashboard",
    layout="wide"
)

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

# -------------------- SAFE API CALL --------------------
def safe_get(url):
    try:
        return requests.get(url, timeout=5).json()
    except:
        st.error("⚠️ Backend not running. Start FastAPI using: uvicorn backend.main:app --reload")
        st.stop()

# -------------------- LOAD DATA FROM BACKEND --------------------
@st.cache_data
def load_data():
    metrics = safe_get(f"{API_URL}/metrics")
    category_data = safe_get(f"{API_URL}/category-summary")

    df = pd.DataFrame(category_data)

    return metrics, df

metrics, df = load_data()

# -------------------- SIDEBAR --------------------
st.sidebar.title(" Project Flow")

st.sidebar.markdown("""
### 1️⃣ Data Collection  
- Source: Kaggle Walmart Dataset  

### 2️⃣ Data Cleaning  
- Handled missing values  
- Converted data types  
- Created `total_sales`  

### 3️⃣ Data Storage  
- Stored in SQLite  
- Table: `SalesClean`  

### 4️⃣ Backend  
- FastAPI (REST APIs)  

### 5️⃣ Visualization  
- Dashboard built using Streamlit  
""")

# -------------------- TITLE --------------------
st.title("📊 Walmart Metrics")

# -------------------- OVERALL METRICS --------------------
st.subheader("📌 Overall Data Distribution")

col1, col2, col3 = st.columns(3)

col1.metric("Total Revenue", f"${metrics['total_revenue']:,.0f}")
col2.metric("Total Orders", f"{metrics['total_orders']:,}")
col3.metric("Avg Order Value", f"${metrics['avg_order_value']:.2f}")

# -------------------- CATEGORY-WISE INSIGHTS --------------------
st.subheader("📂 Category-wise Insights")

category_summary = df.set_index("category").sort_values(by="revenue", ascending=False)

category_summary.rename(columns={
    "revenue": "Revenue",
    "orders": "Orders",
    "avg_order_value": "Avg_Order_Value"
}, inplace=True)

st.dataframe(category_summary.style.format({
    "Revenue": "${:,.0f}",
    "Avg_Order_Value": "${:.2f}"
}))

# -------------------- FILTER --------------------
st.subheader("📊 Category Selection & Comparison")

selected_categories = st.multiselect(
    "Select categories to compare",
    options=category_summary.index.tolist(),
    default=category_summary.index.tolist()
)

filtered = category_summary.loc[selected_categories]

# -------------------- SIDE-BY-SIDE CHARTS --------------------
col1, col2 = st.columns(2)
FIG_SIZE = (6, 4)

# -------- BAR CHART --------
with col1:
    st.markdown("### 📊 Revenue Comparison")

    fig1, ax1 = plt.subplots(figsize=FIG_SIZE)

    ax1.barh(filtered.index, filtered["Revenue"], color="#A7C7E7")

    ax1.set_xlabel("Revenue ($)")
    ax1.set_ylabel("Category")

    ax1.set_box_aspect(1)

    ax1.xaxis.set_major_formatter(
        mticker.FuncFormatter(lambda x, _: f"${x:,.0f}")
    )

    st.pyplot(fig1)
# -------- PIE CHART --------
with col2:
    st.markdown("### 🥧 Revenue Contribution ")

    fig2, ax2 = plt.subplots(figsize=FIG_SIZE)

    colors = plt.cm.Pastel1.colors

    if len(filtered) > 1:
        ax2.pie(
            filtered["Revenue"],
            labels=filtered.index,
            autopct="%1.1f%%",
            startangle=140,
            colors=colors,
            textprops={'fontsize': 9}
        )
    else:
        ax2.text(0.5, 0.5, "Select more than 1 category",
                 ha='center', va='center')

    ax2.set_title("Share of Total Revenue")

    plt.tight_layout()
    st.pyplot(fig2)

st.subheader("🏆 Top vs Lowest Category")

top = category_summary.iloc[0]
low = category_summary.iloc[-1]

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Top Category**")
    st.markdown(f"{top.name}")
    st.markdown(f"${top['Revenue']:,.0f}")

with col2:
    st.markdown("**Lowest Category**")
    st.markdown(f"{low.name}")
    st.markdown(f"${low['Revenue']:,.0f}")


# -------------------- ADDITIONAL INSIGHTS --------------------
st.subheader("📌 Additional Insights")

analysis_data = safe_get(f"{API_URL}/analysis-data")
adf = pd.DataFrame(analysis_data)

if not adf.empty:

    adf["date"] = pd.to_datetime(adf["date"], errors="coerce")
    adf = adf.dropna(subset=["date"])

    # ---------- PREP ----------
    adf["day"] = adf["date"].dt.day_name()

    day_sales = adf.groupby("day")["total_sales"].sum()

    days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    day_sales = day_sales.reindex(days_order)

    # ---------- SIDE BY SIDE ----------
    col1, col2 = st.columns(2)

    # ----- SALES BY DAY -----
    with col1:
        st.markdown("### 📅 Sales by Day")

        fig1, ax1 = plt.subplots(figsize=(6, 4))

        ax1.bar(day_sales.index, day_sales.values, color="#A7C7E7")

        ax1.set_ylabel("Sales ($)")
        ax1.set_xticks(range(len(day_sales.index)))
        ax1.set_xticklabels(day_sales.index, rotation=30)

        plt.tight_layout()
        st.pyplot(fig1)

    # ----- ORDER DISTRIBUTION -----
    with col2:
        st.markdown("### 📈 Order Value Distribution")

        fig2, ax2 = plt.subplots(figsize=(6, 4))

        ax2.hist(adf["total_sales"], bins=30, color="#F4C2C2")

        ax2.set_xlabel("Order Value ($)")
        ax2.set_ylabel("Count")

        plt.tight_layout()
        st.pyplot(fig2)
# -------------------- FINAL INSIGHT --------------------
st.subheader("💡 Final Insight")

if not filtered.empty:
    top_category = filtered["Revenue"].idxmax()
    total_revenue = filtered["Revenue"].sum()
    top_revenue = filtered["Revenue"].max()

    share = (top_revenue / total_revenue) * 100

    if share > 50:
        st.markdown(f"""
### Key Insight

- **{top_category} contributes ~{share:.1f}% of total revenue**, indicating a strong concentration of sales in a single category.

### 🎯 Interpretation:

-  The business is **highly dependent on one category**, which increases risk if demand shifts.
-  This category is a **major growth driver**, so optimizing pricing, inventory, or promotions here can significantly boost revenue.
-  Other categories are underperforming and may need targeted strategies to improve balance.
""")

    elif share > 30:
        st.markdown(f"""

- **{top_category} contributes ~{share:.1f}% of total revenue**, showing a noticeable lead over other categories.

### 🎯 Interpretation:

-  Revenue is **moderately concentrated**, with one category performing better than others.
-  There is opportunity to **scale this category further**, while also improving weaker categories for balanced growth.
""")

    else:
        st.markdown(f"""

- Revenue is **fairly distributed across categories**, with {top_category} contributing ~{share:.1f}%.

### Interpretation:

- The business has a **diversified revenue base**, reducing dependency risk.
- Growth can come from **multiple categories**, not just one dominant segment.
""")

else:
    st.warning("Please select at least one category.")