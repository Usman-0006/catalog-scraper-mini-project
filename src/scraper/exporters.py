import pandas as pd

def export_products(products):
    """Save full products dataset"""
    df = pd.DataFrame(products)
    df.drop_duplicates(subset="product_url", inplace=True)
    df.to_csv("data/products.csv", index=False)
    return df

def export_summary(df):
    """Save category summary"""
    summary = df.groupby(["category", "subcategory"]).agg(
        total_products=("title", "count"),
        avg_price=("price", "mean"),
        min_price=("price", "min"),
        max_price=("price", "max"),
        missing_descriptions=("description", lambda x: x.isna().sum() + (x=='' ).sum())
    ).reset_index()

    summary.to_csv("data/category_summary.csv", index=False)