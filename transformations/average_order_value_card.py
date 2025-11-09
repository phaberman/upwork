import pandas as pd

def average_order_value_card(df: pd.DataFrame) -> pd.DataFrame:

    metric = df['total'].mean()

    return metric
