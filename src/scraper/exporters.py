import pandas as pd


def export_products(products):

    df = pd.DataFrame(products)

    df.drop_duplicates(subset="product_url", inplace=True)

    df.to_csv("data/products.csv", index=False)

    return df


def export_summary(df):

    summary = df.groupby("title").agg(
        avg_price=("price", "mean"),
        min_price=("price", "min"),
        max_price=("price", "max"),
        total_products=("price", "count")
    )

    summary.to_csv("data/category_summary.csv")