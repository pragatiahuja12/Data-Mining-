import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Streamlit config
st.set_page_config(page_title="Nike Dashboard", layout="wide")
st.title("Nike Product Performance Dashboard")

# Generate dataset
np.random.seed(42)
num_records = 300
data = {
    "Product_ID": [f"NKE{1000+i}" for i in range(num_records)],
    "Product_Name": [f"Product_{i}" for i in range(num_records)],
    "Category": np.random.choice(["Footwear", "Apparel", "Accessories"], size=num_records),
    "Region": np.random.choice(["North America", "Europe", "Asia", "South America"], size=num_records),
    "Units_Sold": np.random.randint(50, 1000, size=num_records),
    "Customer_Rating": np.round(np.random.uniform(3.0, 5.0, size=num_records), 2),
    "Inventory_Level": np.random.randint(10, 500, size=num_records),
    "Date": pd.date_range(start="2023-01-01", periods=num_records, freq="D")
}
price_per_unit = np.random.uniform(50, 200, size=num_records)
data["Total_Sales"] = (np.array(data["Units_Sold"]) * price_per_unit).round(2)
df = pd.DataFrame(data)

# --- Filters ---
st.sidebar.header("🔎 Filter Options")
selected_region = st.sidebar.multiselect("Select Region", df["Region"].unique(), default=df["Region"].unique())
selected_category = st.sidebar.multiselect("Select Category", df["Category"].unique(), default=df["Category"].unique())

# Apply filters
filtered_df = df[(df["Region"].isin(selected_region)) & (df["Category"].isin(selected_category))]

# --- KPI Cards ---
st.subheader("📊 Key Metrics")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Sales", f"${filtered_df['Total_Sales'].sum():,.2f}")
col2.metric("Units Sold", f"{filtered_df['Units_Sold'].sum():,}")
col3.metric("Avg. Customer Rating", f"{filtered_df['Customer_Rating'].mean():.2f} / 5.0")
col4.metric("Avg. Inventory", f"{filtered_df['Inventory_Level'].mean():.0f} units")

# --- Line Chart: Sales Over Time ---
st.subheader("📈 Sales Trend Over Time")
sales_over_time = filtered_df.groupby("Date")["Total_Sales"].sum()
st.line_chart(sales_over_time)

# --- Bar Chart: Sales by Category ---
st.subheader("📊 Sales by Product Category")
category_sales = filtered_df.groupby("Category")["Total_Sales"].sum().sort_values()
st.bar_chart(category_sales)

# --- Heatmap: Inventory by Region and Category ---
st.subheader("🗺️ Inventory Levels by Region and Category")
pivot_inventory = filtered_df.pivot_table(index="Region", columns="Category", values="Inventory_Level", aggfunc="mean")
fig, ax = plt.subplots()
sns.heatmap(pivot_inventory, annot=True, fmt=".0f", cmap="Reds", ax=ax)
st.pyplot(fig)

# --- Download Button ---
st.download_button(
    label="📥 Download Filtered Dataset as CSV",
    data=filtered_df.to_csv(index=False).encode("utf-8"),
    file_name="Nike_Filtered_Product_Performance.csv",
    mime="text/csv"
)


