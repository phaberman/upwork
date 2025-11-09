import pandas as pd

def customer_count_card(df: pd.DataFrame) -> int:

    metric = df['name'].nunique()

    return metric
