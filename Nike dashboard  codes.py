import pandas as pd
import numpy as np
import streamlit as st
st.set_page_config(page_title="Nike Dashboard", layout="wide")
st.title("Nike Product Performance Dashboard")

# Set random seed for reproducibility
np.random.seed(42)

# Number of product records
num_records = 300

# Generate fields for the dataset
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

# Generate Total_Sales based on Units_Sold and random price per unit
price_per_unit = np.random.uniform(50, 200, size=num_records)
data["Total_Sales"] = (np.array(data["Units_Sold"]) * price_per_unit).round(2)

# Create DataFrame
df = pd.DataFrame(data)

# Save to CSV (optional)
df.to_csv("Nike_Product_Performance_Dataset.csv", index=False)

# Display first few rows
print(df.head())


import pandas as pd
import numpy as np

# Set random seed for reproducibili
