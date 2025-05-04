import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("Nike_Product_Performance_Dataset.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("🔍 Filter Data")
regions = st.sidebar.multiselect("Select Region(s):", options=df["Region"].unique(), default=df["Region"].unique())
categories = st.sidebar.multiselect("Select Category(s):", options=df["Category"].unique(), default=df["Category"].unique())
date_range = st.sidebar.date_input("Select Date Range:", [df["Date"].min(), df["Date"].max()])

# Apply filters
filtered_df = df[
    (df["Region"].isin(regions)) &
    (df["Category"].isin(categories)) &
    (df["Date"] >= pd.to_datetime(date_range[0])) &
    (df["Date"] <= pd.to_datetime(date_range[1]))
]

# Title and summary
st.title("Nike Product Performance Dashboard")
st.markdown("This dashboard visualizes Nike’s product performance across categories and regions.")

# KPI Cards
col1, col2, col3 = st.columns(3)
col1.metric("💰 Total Sales", f"${filtered_df['Total_Sales'].sum():,.2f}")
col2.metric("⭐ Average Rating", f"{filtered_df['Customer_Rating'].mean():.2f} / 5.0")
col3.metric("📦 Units Sold", f"{filtered_df['Units_Sold'].sum():,}")

# Line chart - Sales trend over time
sales_trend = filtered_df.groupby("Date")["Total_Sales"].sum().reset_index()
fig_line = px.line(sales_trend, x="Date", y="Total_Sales", title="📈 Sales Trend Over Time")
st.plotly_chart(fig_line)

# Bar chart - Sales by Category
sales_by_cat = filtered_df.groupby("Category")["Total_Sales"].sum().reset_index()
fig_bar = px.bar(sales_by_cat, x="Category", y="Total_Sales", title="📊 Sales by Category", text_auto=True)
st.plotly_chart(fig_bar)

# Scatter plot - Inventory vs Sales
fig_scatter = px.scatter(
    filtered_df,
    x="Inventory_Level",
    y="Total_Sales",
    color="Region",
    symbol="Category",
    title="📍 Inventory Level vs Total Sales"
)
st.plotly_chart(fig_scatter)

# Download filtered data
csv = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="📥 Download Filtered Data as CSV",
    data=csv,
    file_name="Nike_Filtered_Data.csv",
    mime="text/csv"
)

# Footer
st.markdown("---")
st.caption("Developed for ALY6040 Assignment 4 | Powered by Streamlit")



