import pandas as pd

def top_customers_card(df: pd.DataFrame) -> pd.DataFrame:

    # Ensure the necessary columns are present
    if 'name' not in df.columns or 'total' not in df.columns:
        raise ValueError("DataFrame must contain 'name' and 'total' columns.")

    # Group by customer name and sum the total sales
    customer_totals = df.groupby('name')['total'].sum().reset_index()

    # Sort by total sales in descending order and get the top N customers
    top_customers = customer_totals.sort_values(by='total', ascending=False).head()

    # Title case column names for better presentation
    top_customers.columns = [col.title() for col in top_customers.columns]

    return top_customers
