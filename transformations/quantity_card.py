import pandas as pd

def quantity_card(df: pd.DataFrame) -> pd.DataFrame:

    metric = df['quantity'].sum()

    return metric
