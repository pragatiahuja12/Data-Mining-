import streamlit as st
import pandas as pd
import numpy as np

# Streamlit app setup
st.set_page_config(page_title="Nike Product Performance Dashboard", layout="wide")
st.title("Nike Product Performance Dashboard")

# Generate dataset
np.random.seed(42)
num_records = 300

# Simulate Nike product performance data
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

# Calculate Total Sales
price_per_unit = np.random.uniform(50, 200, size=num_records)
data["Total_Sales"] = (np.array(data["Units_Sold"]) * price_per_unit).round(2)

# Create DataFrame
df = pd.DataFrame(data)

# Show a preview
st.subheader("Sample Data")
st.dataframe(df.head())

# Download button
csv = df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Download Full Dataset as CSV",
    data=csv,
    file_name="Nike_Product_Performance_Dataset.csv",
    mime="text/csv"
)

