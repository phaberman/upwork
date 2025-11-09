import pandas as pd

def new_customer_count_card(df: pd.DataFrame) -> int:
    current_year = pd.Timestamp.now().year
    df['created_at'] = pd.to_datetime(df['created_at'])
    new_customers_df = df[df['created_at'].dt.year == current_year]
    metric = new_customers_df['name'].nunique()
    return metric
