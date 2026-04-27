import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# -------------------- CONFIG --------------------
st.set_page_config(
    page_title="Walmart Sales Dashboard",
    layout="wide"
)

API_URL = "http://127.0.0.1:8000"

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

    # Map backend → frontend schema
    df["total_sales"] = df["revenue"]

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

category_summary = (
    df.groupby("category")
    .agg(
        Revenue=("total_sales", "sum"),
        Orders=("total_sales", "count"),
        Avg_Order_Value=("total_sales", "mean")
    )
    .sort_values(by="Revenue", ascending=False)
)

st.dataframe(category_summary.style.format({
    "Revenue": "${:,.0f}",
    "Avg_Order_Value": "${:.2f}"
}))

# -------------------- FILTER --------------------
st.subheader(" 📂 Category Comparison")

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

    ax1.xaxis.set_major_formatter(
        mticker.FuncFormatter(lambda x, _: f"${x:,.0f}")
    )

    plt.tight_layout()
    st.pyplot(fig1)

# -------- PIE CHART --------
with col2:
    st.markdown("### 📊 Revenue Contribution ")

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

col1.success(f"Top Category: {top.name} (${top['Revenue']:,.0f})")
col2.error(f"Lowest Category: {low.name} (${low['Revenue']:,.0f})")
# -------------------- FINAL INSIGHT --------------------
st.subheader("💡 Final Insight")

if not filtered.empty:
    top_category = filtered["Revenue"].idxmax()

    st.markdown(f"""
###  Key Result
- **Top Performing Category:** {top_category}  
- **Highest Revenue Contribution:** {top_category}  

Both the **bar chart** and **pie chart** indicate that *{top_category}* dominates overall sales.
""")
else:
    st.warning("Please select at least one category.")