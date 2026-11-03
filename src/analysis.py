import pandas as pd


# ==========================================
# 1. LOAD DATASET
# ==========================================

df = pd.read_csv(
    "data/Sample - Superstore.csv",
    encoding="cp1252"
)

print("\n========== FIRST FIVE RECORDS ==========")
print(df.head())


# ==========================================
# 2. BASIC DATASET INFORMATION
# ==========================================

print("\n========== DATASET SHAPE ==========")
print(df.shape)

print("\n========== COLUMN NAMES ==========")
print(df.columns)

print("\n========== DATASET INFORMATION ==========")
df.info()

print("\n========== STATISTICAL SUMMARY ==========")
print(df.describe())


# ==========================================
# 3. DATA CLEANING AND EXPLORATION
# ==========================================

print("\n========== MISSING VALUES ==========")
print(df.isnull().sum())

print("\n========== DUPLICATE RECORDS ==========")
print(df.duplicated().sum())

print("\n========== PRODUCT CATEGORIES ==========")
print(df["Category"].unique())

print("\n========== CATEGORY COUNTS ==========")
print(df["Category"].value_counts())


# ==========================================
# 4. DATE CONVERSION
# ==========================================

df["Order Date"] = pd.to_datetime(df["Order Date"])
df["Ship Date"] = pd.to_datetime(df["Ship Date"])

print("\n========== UPDATED DATA TYPES ==========")
print(df.dtypes)


# ==========================================
# 5. SHIPPING DAYS ANALYSIS
# ==========================================

df["Shipping Days"] = (
    df["Ship Date"] - df["Order Date"]
).dt.days

print("\n========== SHIPPING DAYS ==========")
print(
    df[["Order Date", "Ship Date", "Shipping Days"]].head()
)


# ==========================================
# 6. BUSINESS KPI ANALYSIS
# ==========================================

total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()
total_quantity = df["Quantity"].sum()

total_orders = df["Order ID"].nunique()
total_customers = df["Customer ID"].nunique()

average_order_value = total_sales / total_orders
profit_margin = (total_profit / total_sales) * 100

print("\n========== BUSINESS KPIs ==========")

print("Total Sales:", round(total_sales, 2))
print("Total Profit:", round(total_profit, 2))
print("Total Quantity Sold:", total_quantity)
print("Total Orders:", total_orders)
print("Total Customers:", total_customers)
print("Average Order Value:", round(average_order_value, 2))
print("Profit Margin:", round(profit_margin, 2), "%")


# ==========================================
# 7. CATEGORY-WISE ANALYSIS
# ==========================================

category_analysis = df.groupby("Category").agg({
    "Sales": "sum",
    "Profit": "sum",
    "Quantity": "sum"
})

category_analysis["Profit Margin"] = (
    category_analysis["Profit"] /
    category_analysis["Sales"]
) * 100

print("\n========== CATEGORY ANALYSIS ==========")
print(category_analysis.round(2))


# ==========================================
# 8. REGION-WISE ANALYSIS
# ==========================================

region_analysis = df.groupby("Region").agg({
    "Sales": "sum",
    "Profit": "sum",
    "Quantity": "sum"
})

region_analysis["Profit Margin"] = (
    region_analysis["Profit"] /
    region_analysis["Sales"]
) * 100

print("\n========== REGION ANALYSIS ==========")
print(region_analysis.round(2))


# ==========================================
# 9. EXTRACT YEAR AND MONTH
# ==========================================

df["Year"] = df["Order Date"].dt.year
df["Month"] = df["Order Date"].dt.month


# ==========================================
# 10. MONTHLY SALES ANALYSIS
# ==========================================

monthly_sales = df.groupby("Month")["Sales"].sum()

print("\n========== MONTHLY SALES ANALYSIS ==========")
print(monthly_sales.round(2))


# ==========================================
# 11. HIGHEST AND LOWEST SALES MONTH
# ==========================================

highest_month = monthly_sales.idxmax()
lowest_month = monthly_sales.idxmin()

print("\n========== SALES PERFORMANCE ==========")

print("Highest Sales Month:", highest_month)
print("Highest Sales:", round(monthly_sales.max(), 2))

print("Lowest Sales Month:", lowest_month)
print("Lowest Sales:", round(monthly_sales.min(), 2))


# ==========================================
# 12. MONTHLY SALES BY YEAR
# ==========================================

yearly_monthly_sales = df.groupby(
    ["Year", "Month"]
)["Sales"].sum()

print("\n========== MONTHLY SALES BY YEAR ==========")
print(yearly_monthly_sales.round(2))


# ==========================================
# 13. SUB-CATEGORY ANALYSIS
# ==========================================

subcategory_analysis = df.groupby("Sub-Category").agg({
    "Sales": "sum",
    "Profit": "sum",
    "Quantity": "sum"
})

subcategory_analysis = subcategory_analysis.sort_values(
    by="Sales",
    ascending=False
)

print("\n========== SUB-CATEGORY ANALYSIS ==========")
print(subcategory_analysis.round(2))


# ==========================================
# 14. SUB-CATEGORY PROFIT MARGIN
# ==========================================

subcategory_analysis["Profit Margin"] = (
    subcategory_analysis["Profit"] /
    subcategory_analysis["Sales"]
) * 100

print("\n========== SUB-CATEGORY PROFIT MARGIN ==========")
print(subcategory_analysis.round(2))


# ==========================================
# 15. HIGHEST AND LOWEST PROFIT SUB-CATEGORY
# ==========================================

highest_profit_subcategory = (
    subcategory_analysis["Profit"].idxmax()
)

lowest_profit_subcategory = (
    subcategory_analysis["Profit"].idxmin()
)

print("\n========== SUB-CATEGORY PERFORMANCE ==========")

print("Highest Profit Sub-Category:", highest_profit_subcategory)

print("Lowest Profit Sub-Category:", lowest_profit_subcategory)


# ==========================================
# END OF ANALYSIS
# ==========================================

print("\n========== ANALYSIS COMPLETED SUCCESSFULLY ==========")