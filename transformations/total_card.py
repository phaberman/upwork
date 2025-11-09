import pandas as pd

def total_card(df: pd.DataFrame) -> pd.DataFrame:

    metric = df['total'].sum()

    return metric
