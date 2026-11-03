import pandas as pd
import plotly.express as px

# Load dataset
df = pd.read_csv("data/Sample - Superstore.csv", encoding="cp1252")

# Calculate category-wise sales
category_sales = df.groupby("Category")["Sales"].sum().reset_index()

# Create interactive bar chart
fig = px.bar(
    category_sales,
    x="Category",
    y="Sales",
    title="Sales by Product Category",
    text_auto=".2s",
    color="Category",
    labels={
        "Category": "Product Category",
        "Sales": "Total Sales ($)"
    }
)

# Display chart
fig.show()
# Calculate region-wise profit
region_profit = df.groupby("Region")["Profit"].sum().reset_index()

# Create interactive bar chart
fig2 = px.bar(
    region_profit,
    x="Region",
    y="Profit",
    title="Profit by Region",
    text_auto=".2s",
    color="Region",
    labels={
        "Region": "Sales Region",
        "Profit": "Total Profit ($)"
    }
)

# Display chart
fig2.show()
# Convert Order Date into datetime format
df["Order Date"] = pd.to_datetime(df["Order Date"])

# Calculate monthly sales
monthly_sales = (
    df.groupby(df["Order Date"].dt.to_period("M"))["Sales"]
    .sum()
    .reset_index()
)

# Convert period into string for Plotly
monthly_sales["Order Date"] = monthly_sales["Order Date"].astype(str)

# Create interactive line chart
fig3 = px.line(
    monthly_sales,
    x="Order Date",
    y="Sales",
    title="Monthly Sales Trend",
    markers=True,
    labels={
        "Order Date": "Month",
        "Sales": "Total Sales ($)"
    }
)

# Display chart
fig3.show()
# Calculate sales by sub-category
subcategory_sales = (
    df.groupby("Sub-Category")["Sales"]
    .sum()
    .reset_index()
)

# Sort sales in descending order
subcategory_sales = subcategory_sales.sort_values(
    by="Sales",
    ascending=True
)

# Create horizontal bar chart
fig4 = px.bar(
    subcategory_sales,
    x="Sales",
    y="Sub-Category",
    orientation="h",
    title="Sales by Sub-Category",
    text_auto=".2s",
    color="Sales",
    labels={
        "Sales": "Total Sales ($)",
        "Sub-Category": "Product Sub-Category"
    }
)

fig4.show()
# Calculate profit by sub-category
subcategory_profit = (
    df.groupby("Sub-Category")["Profit"]
    .sum()
    .reset_index()
)

# Sort profit values
subcategory_profit = subcategory_profit.sort_values(
    by="Profit",
    ascending=True
)

# Create interactive bar chart
fig5 = px.bar(
    subcategory_profit,
    x="Profit",
    y="Sub-Category",
    orientation="h",
    title="Profit by Sub-Category",
    text_auto=".2s",
    color="Profit",
    color_continuous_scale="RdYlGn",
    labels={
        "Profit": "Total Profit ($)",
        "Sub-Category": "Product Sub-Category"
    }
)

# Display chart
fig5.show()