import pandas as pd
import sqlite3

# Load CSV dataset

df = pd.read_csv(
    "data/Sample - Superstore.csv",
    encoding="cp1252"
)

# Create SQLite database

connection = sqlite3.connect("sales.db")

# Store dataset in SQL table

df.to_sql(
    "sales",
    connection,
    if_exists="replace",
    index=False
)

print("Database created successfully!")

# ---------------- SQL QUERIES ----------------

# 1. Total Sales and Profit

query1 = """
SELECT
    SUM(Sales) AS Total_Sales,
    SUM(Profit) AS Total_Profit
FROM sales;
"""

result1 = pd.read_sql_query(query1, connection)

print("\nTotal Sales and Profit:")
print(result1)


# 2. Sales by Category

query2 = """
SELECT
    Category,
    SUM(Sales) AS Total_Sales
FROM sales
GROUP BY Category
ORDER BY Total_Sales DESC;
"""

result2 = pd.read_sql_query(query2, connection)

print("\nSales by Category:")
print(result2)


# 3. Profit by Region

query3 = """
SELECT
    Region,
    SUM(Profit) AS Total_Profit
FROM sales
GROUP BY Region
ORDER BY Total_Profit DESC;
"""

result3 = pd.read_sql_query(query3, connection)

print("\nProfit by Region:")
print(result3)


# 4. Top 10 Products by Sales

query4 = """
SELECT
    "Product Name",
    SUM(Sales) AS Total_Sales
FROM sales
GROUP BY "Product Name"
ORDER BY Total_Sales DESC
LIMIT 10;
"""

result4 = pd.read_sql_query(query4, connection)

print("\nTop 10 Products:")
print(result4)


# Close database connection

connection.close()

print("\nSQL Analysis Completed Successfully!")