import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("Nike_Product_Performance_Dataset.csv")
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    return df.dropna(subset=["Date"])

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

# Page Title
st.title("👟 Nike Product Performance Dashboard")
st.markdown("Analyze sales, rating, and inventory trends for Nike products by category, region, and time.")

# Tabs for layout
tab1, tab2, tab3 = st.tabs(["📊 Overview", "📦 Product Insights", "🔍 Data Preview"])

with tab1:
    # KPIs
    col1, col2, col3 = st.columns(3)
    col1.metric("💰 Total Sales", f"${filtered_df['Total_Sales'].sum():,.2f}")
    col2.metric("⭐ Avg Rating", f"{filtered_df['Customer_Rating'].mean():.2f} / 5.0")
    col3.metric("📦 Units Sold", f"{filtered_df['Units_Sold'].sum():,}")

    # Line chart
    sales_trend = filtered_df.groupby("Date")["Total_Sales"].sum().reset_index()
    sales_trend.sort_values("Date", inplace=True)
    fig_line = px.line(sales_trend, x="Date", y="Total_Sales", title=f"📈 Sales Trend ({date_range[0]} to {date_range[1]})")
    st.plotly_chart(fig_line)

    # Bar chart
    sales_by_cat = filtered_df.groupby("Category")["Total_Sales"].sum().reset_index()
    fig_bar = px.bar(sales_by_cat, x="Category", y="Total_Sales", title="📊 Sales by Category", text_auto=True)
    st.plotly_chart(fig_bar)

    # Heatmap: Inventory by Region x Category
    pivot = filtered_df.pivot_table(index="Region", columns="Category", values="Inventory_Level", aggfunc="mean")
    st.subheader("🗺️ Avg Inventory by Region and Category")
    st.dataframe(pivot.style.background_gradient(cmap="Reds"))

with tab2:
    # Top products by sales
    top_products = filtered_df.groupby("Product_Name")["Total_Sales"].sum().nlargest(10).reset_index()
    st.subheader("🏆 Top 10 Products by Sales")
    fig_top = px.bar(top_products, x="Total_Sales", y="Product_Name", orientation='h', title="Top 10 Products", text_auto=True)
    st.plotly_chart(fig_top)

    # Inventory vs Sales
    fig_scatter = px.scatter(
        filtered_df,
        x="Inventory_Level",
        y="Total_Sales",
        color="Region",
        symbol="Category",
        title="📍 Inventory Level vs Total Sales"
    )
    st.plotly_chart(fig_scatter)

with tab3:
    st.subheader("📋 Filtered Data Preview")
    st.dataframe(filtered_df.head(50))
    st.download_button(
        label="📥 Download Filtered Data as CSV",
        data=filtered_df.to_csv(index=False).encode("utf-8"),
        file_name="Nike_Filtered_Data.csv",
        mime="text/csv"
    )

# Footer
st.markdown("---")
st.caption("Developed for ALY6040 Assignment 4 | Enhanced with tabs, heatmaps, and product insights.")




