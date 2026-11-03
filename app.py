import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3


# ---------------- PAGE CONFIGURATION ----------------

st.set_page_config(
    page_title="Sales Analysis Dashboard",
    page_icon="📊",
    layout="wide"
)


# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>

.stApp {
    background-color: #101827;
    color: #F1F5F9;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

h1, h2, h3 {
    color: #F8FAFC !important;
}

p, label {
    color: #CBD5E1;
}

section[data-testid="stSidebar"] {
    background-color: #172337;
}

div[data-testid="stMetric"] {
    background-color: #1E2B40;
    border: 1px solid #334155;
    padding: 18px;
    border-radius: 12px;
}

div[data-testid="stMetricLabel"] {
    color: #A9B8CC !important;
}

div[data-testid="stMetricValue"] {
    color: #FFFFFF !important;
}

.stDownloadButton button {
    background-color: #2563EB;
    color: white;
    border-radius: 8px;
}

hr {
    border-color: #334155;
}

</style>
""", unsafe_allow_html=True)


# ---------------- LOAD DATA ----------------

@st.cache_data
def load_data():

    df = pd.read_csv(
        "data/Sample - Superstore.csv",
        encoding="cp1252"
    )

    df["Order Date"] = pd.to_datetime(df["Order Date"])
    df["Ship Date"] = pd.to_datetime(df["Ship Date"])

    return df


df = load_data()


# ---------------- DASHBOARD HEADER ----------------

st.markdown(
    """
    <div style="
        background: linear-gradient(90deg, #172337, #263F60);
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #334155;
        margin-bottom: 25px;
    ">
        <h1 style="color: white; margin-bottom: 8px;">
            📊 Superstore Sales Dashboard
        </h1>

        <p style="color: #CBD5E1; font-size: 16px; margin: 0;">
            Business Intelligence | Sales Performance | Profit Analysis
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


# ---------------- SIDEBAR FILTERS ----------------

st.sidebar.title("🔎 Dashboard Filters")

selected_region = st.sidebar.multiselect(
    "Select Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

selected_category = st.sidebar.multiselect(
    "Select Category",
    options=df["Category"].unique(),
    default=df["Category"].unique()
)

date_range = st.sidebar.date_input(
    "Select Order Date Range",
    value=(
        df["Order Date"].min().date(),
        df["Order Date"].max().date()
    )
)


# ---------------- FILTER DATA ----------------

filtered_df = df.copy()

filtered_df = filtered_df[
    filtered_df["Region"].isin(selected_region)
]

filtered_df = filtered_df[
    filtered_df["Category"].isin(selected_category)
]

if len(date_range) == 2:

    start_date = pd.to_datetime(date_range[0])
    end_date = pd.to_datetime(date_range[1])

    filtered_df = filtered_df[
        (filtered_df["Order Date"] >= start_date) &
        (filtered_df["Order Date"] < end_date + pd.Timedelta(days=1))
    ]

else:
    filtered_df = filtered_df.iloc[0:0]


# ---------------- DASHBOARD CONTENT ----------------

if filtered_df.empty:

    st.warning(
        "No data available for the selected filters. Please change your filters."
    )

else:

    # ---------------- KPI METRICS ----------------

    st.markdown("## 📈 Business Performance Overview")

    st.caption(
        "Key business metrics based on your selected filters."
    )

    total_sales = filtered_df["Sales"].sum()

    total_profit = filtered_df["Profit"].sum()

    total_orders = filtered_df["Order ID"].nunique()

    total_customers = filtered_df["Customer ID"].nunique()

    total_quantity = filtered_df["Quantity"].sum()

    average_order_value = (
        total_sales / total_orders
        if total_orders != 0 else 0
    )

    profit_margin = (
        (total_profit / total_sales) * 100
        if total_sales != 0 else 0
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "💰 Total Sales",
        f"${total_sales:,.2f}"
    )

    col2.metric(
        "📈 Total Profit",
        f"${total_profit:,.2f}"
    )

    col3.metric(
        "📦 Total Orders",
        f"{total_orders:,}"
    )

    col4, col5, col6 = st.columns(3)

    col4.metric(
        "👥 Total Customers",
        f"{total_customers:,}"
    )

    col5.metric(
        "🛒 Average Order Value",
        f"${average_order_value:,.2f}"
    )

    col6.metric(
        "📊 Profit Margin",
        f"{profit_margin:.2f}%"
    )

    st.divider()


    # ---------------- CHART SECTION ----------------

    st.markdown("## 📊 Sales & Profit Analysis")

    st.caption(
        "Explore category, regional and product-level performance."
    )


    # CHART 1: SALES BY CATEGORY

    category_sales = (
        filtered_df.groupby("Category")["Sales"]
        .sum()
        .reset_index()
    )

    fig1 = px.bar(
        category_sales,
        x="Category",
        y="Sales",
        color="Category",
        title="Sales by Product Category",
        template="plotly_dark"
    )

    fig1.update_layout(
        paper_bgcolor="#1E2B40",
        plot_bgcolor="#1E2B40",
        font_color="#F1F5F9"
    )


    # CHART 2: PROFIT BY REGION

    region_profit = (
        filtered_df.groupby("Region")["Profit"]
        .sum()
        .reset_index()
    )

    fig2 = px.bar(
        region_profit,
        x="Region",
        y="Profit",
        color="Region",
        title="Profit by Region",
        template="plotly_dark"
    )

    fig2.update_layout(
        paper_bgcolor="#1E2B40",
        plot_bgcolor="#1E2B40",
        font_color="#F1F5F9"
    )


    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(
            fig1,
            use_container_width=True
        )

    with col2:
        st.plotly_chart(
            fig2,
            use_container_width=True
        )


    # CHART 3: MONTHLY SALES TREND

    monthly_sales = (
        filtered_df.groupby(
            filtered_df["Order Date"].dt.to_period("M")
        )["Sales"]
        .sum()
        .reset_index()
    )

    monthly_sales["Order Date"] = (
        monthly_sales["Order Date"].dt.to_timestamp()
    )

    fig3 = px.line(
        monthly_sales,
        x="Order Date",
        y="Sales",
        markers=True,
        title="Monthly Sales Trend",
        template="plotly_dark"
    )

    fig3.update_traces(
        line_color="#60A5FA",
        marker_color="#38BDF8"
    )

    fig3.update_layout(
        paper_bgcolor="#1E2B40",
        plot_bgcolor="#1E2B40",
        font_color="#F1F5F9"
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )


    # CHART 4: SALES BY SUB-CATEGORY

    subcategory_sales = (
        filtered_df.groupby("Sub-Category")["Sales"]
        .sum()
        .reset_index()
        .sort_values("Sales")
    )

    fig4 = px.bar(
        subcategory_sales,
        x="Sales",
        y="Sub-Category",
        orientation="h",
        title="Sales by Sub-Category",
        template="plotly_dark"
    )

    fig4.update_layout(
        paper_bgcolor="#1E2B40",
        plot_bgcolor="#1E2B40",
        font_color="#F1F5F9"
    )


    # CHART 5: PROFIT BY SUB-CATEGORY

    subcategory_profit = (
        filtered_df.groupby("Sub-Category")["Profit"]
        .sum()
        .reset_index()
        .sort_values("Profit")
    )

    fig5 = px.bar(
        subcategory_profit,
        x="Profit",
        y="Sub-Category",
        orientation="h",
        color="Profit",
        color_continuous_scale="RdYlGn",
        title="Profit by Sub-Category",
        template="plotly_dark"
    )

    fig5.update_layout(
        paper_bgcolor="#1E2B40",
        plot_bgcolor="#1E2B40",
        font_color="#F1F5F9"
    )


    col3, col4 = st.columns(2)

    with col3:
        st.plotly_chart(
            fig4,
            use_container_width=True
        )

    with col4:
        st.plotly_chart(
            fig5,
            use_container_width=True
        )


    # ---------------- BUSINESS INSIGHTS ----------------

    st.divider()

    st.markdown("## 💡 Business Insights")

    st.caption(
        "Important business findings based on the selected filters."
    )

    category_performance = (
        filtered_df.groupby("Category")["Sales"]
        .sum()
    )

    best_category = category_performance.idxmax()

    region_performance = (
        filtered_df.groupby("Region")["Profit"]
        .sum()
    )

    best_region = region_performance.idxmax()

    subcategory_performance = (
        filtered_df.groupby("Sub-Category")["Profit"]
        .sum()
    )

    lowest_subcategory = subcategory_performance.idxmin()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info(
            f"🏆 **Top Sales Category**\n\n"
            f"{best_category}"
        )

    with col2:
        st.success(
            f"📍 **Highest Profit Region**\n\n"
            f"{best_region}"
        )

    with col3:
        st.warning(
            f"📉 **Lowest Profit Sub-Category**\n\n"
            f"{lowest_subcategory}"
        )


    # ---------------- SQL BUSINESS ANALYSIS ----------------

    st.divider()

    st.markdown("## 🗄️ SQL Business Analysis")

    st.caption(
        "Business analysis performed using SQLite queries."
    )

    connection = sqlite3.connect("sales.db")

    filtered_df.to_sql(
        "filtered_sales",
        connection,
        if_exists="replace",
        index=False
    )


    # QUERY 1: SALES BY CATEGORY

    query1 = """
    SELECT
        Category,
        ROUND(SUM(Sales), 2) AS Total_Sales
    FROM filtered_sales
    GROUP BY Category
    ORDER BY Total_Sales DESC;
    """

    category_sql = pd.read_sql_query(
        query1,
        connection
    )


    # QUERY 2: PROFIT BY REGION

    query2 = """
    SELECT
        Region,
        ROUND(SUM(Profit), 2) AS Total_Profit
    FROM filtered_sales
    GROUP BY Region
    ORDER BY Total_Profit DESC;
    """

    region_sql = pd.read_sql_query(
        query2,
        connection
    )


    # QUERY 3: TOP 5 PRODUCTS BY SALES

    query3 = """
    SELECT
        "Product Name",
        ROUND(SUM(Sales), 2) AS Total_Sales
    FROM filtered_sales
    GROUP BY "Product Name"
    ORDER BY Total_Sales DESC
    LIMIT 5;
    """

    top_products_sql = pd.read_sql_query(
        query3,
        connection
    )


    # DISPLAY SQL RESULTS

    st.subheader("Sales by Category")

    st.dataframe(
        category_sql,
        use_container_width=True,
        hide_index=True
    )

    st.subheader("Profit by Region")

    st.dataframe(
        region_sql,
        use_container_width=True,
        hide_index=True
    )

    st.subheader("Top 5 Products by Sales")

    st.dataframe(
        top_products_sql,
        use_container_width=True,
        hide_index=True
    )

    connection.close()


    # ---------------- DOWNLOAD FILTERED DATA ----------------

    st.divider()

    st.subheader("Download Filtered Sales Data")

    csv_data = filtered_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="📥 Download Sales Data",
        data=csv_data,
        file_name="filtered_sales_data.csv",
        mime="text/csv"
    )


# ---------------- FOOTER ----------------

st.divider()

st.caption(
    "Sales Data Analysis Project | "
    "Built using Python, Pandas, Plotly and Streamlit"
)