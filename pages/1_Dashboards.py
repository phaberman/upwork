import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv  # NEW

from transformations.total_card import total_card
from transformations.quantity_card import quantity_card
from transformations.average_order_value_card import average_order_value_card
from transformations.top_products_card import top_products_card
from transformations.weekly_revenue import weekly_revenue
from transformations.customer_count_card import customer_count_card
from transformations.new_customer_count_card import new_customer_count_card
from transformations.top_customers_card import top_customers_card
from transformations.cumulative_customer_count import cumulative_customer_count

# --- Load environment variables ---
load_dotenv()

# --- Streamlit config ---
st.set_page_config(page_title="Dashboards", layout="wide")
st.title("Dashboards")

# --- Load data paths from environment variables ---
sales_data_path = os.getenv("SALES_DATA_PATH", "./data/sales.csv")
customers_data_path = os.getenv("CUSTOMERS_DATA_PATH", "./data/customers.csv")
customer_sales_path = os.getenv("CUSTOMER_SALES_PATH", "./data/customer_sales.csv")

# Create tabs
sales_tab, customers_tab = st.tabs(["Sales", "Customers"])

# --- SALES TAB ---
with sales_tab:

    # Load your data once (replace with actual data source)
    raw_df = pd.read_csv(sales_data_path)
    raw_df['created_at'] = pd.to_datetime(raw_df['created_at'])  # ensure datetime column

    # --- Date Filter ---
    col1, col2, col3 = st.columns(3)
    with col1:
        min_date = raw_df['created_at'].min().date()
        max_date = raw_df['created_at'].max().date()

        date_range = st.date_input(
            label="Filter by Date",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )

        # Handle case where only one date is selected (user mid-selection)
        if isinstance(date_range, tuple) and len(date_range) == 2:
            start_date, end_date = date_range
        else:
            start_date, end_date = min_date, max_date

    with col2:
        categories = raw_df['category'].dropna().unique().tolist()
        selected_categories = st.multiselect(
            label="Filter by Category",
            options=categories,
            default=None
        )

    with col3:
        products = raw_df['product'].dropna().unique().tolist()
        selected_products = st.multiselect(
            label="Filter by Product",
            options=products,
            default=None
        )

    # --- Apply Filters ---
    df = raw_df[
        (raw_df['created_at'] >= pd.to_datetime(start_date)) &
        (raw_df['created_at'] <= pd.to_datetime(end_date))
    ]

    if selected_categories:
        df = df[df['category'].isin(selected_categories)]

    if selected_products:
        df = df[df['product'].isin(selected_products)]

    st.divider()

    # --- Row 1: KPI cards ---
    col1, col2, col3 = st.columns(3)

    with col1:
        total = total_card(df)
        st.metric(label="Total Sales", value=f"${total:,.2f}")

    with col2:
        qty = quantity_card(df)
        st.metric(label="Total Quantity Sold", value=f"{qty:,}")

    with col3:
        avg_order_value = average_order_value_card(df)
        st.metric(label="Average Order Value", value=f"${avg_order_value:,.2f}")

    st.divider()

    # --- Row 2: Table and Chart ---
    left_col, right_col = st.columns([1, 2])

    with left_col:
        st.subheader("Top Products")
        st.dataframe(top_products_card(df), hide_index=True, width='stretch')

    with right_col:
        st.subheader("Weekly Revenue")
        fig = weekly_revenue(df)
        st.plotly_chart(fig, width='stretch')

# --- CUSTOMERS TAB ---
with customers_tab:

    # Data
    customer_df = pd.read_csv(customers_data_path)

    # --- Row 1: KPI cards ---
    col1, col2 = st.columns(2)

    with col1:
        customer_count = customer_count_card(customer_df)
        st.metric(label="Unique Customers", value=f"{customer_count:,}")

    with col2:
        new_customer_count = new_customer_count_card(customer_df)
        st.metric(label="New Customers This Year", value=f"{new_customer_count:,}")

    st.divider()

    # --- Row 1: Table and Chart --- #
    customer_sales = pd.read_csv(customer_sales_path)

    left_col, right_col = st.columns([1, 2])
    with left_col:
        st.subheader("Top Customers")
        st.dataframe(top_customers_card(customer_sales), hide_index=True, width='stretch')

    with right_col:
        st.subheader("Cumulative Customer Count")
        fig = cumulative_customer_count(customer_df)
        st.plotly_chart(fig, width='stretch')
