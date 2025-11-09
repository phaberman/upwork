import pandas as pd

def top_products_card(df: pd.DataFrame) -> pd.DataFrame:

    top_products = df.groupby(['category', 'product']).agg({'quantity': 'sum'})

    top_products_sorted = top_products.sort_values(by='quantity', ascending=False).reset_index()

    top_products_sorted.columns = ['Category', 'Product', 'Quantity']

    return top_products_sorted.head(5)
