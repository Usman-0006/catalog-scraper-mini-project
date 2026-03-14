import pandas as pd
import os

def export_results(data_list):
   
 
    os.makedirs('data', exist_ok=True)
    
    if not data_list:
        print("Warning: No data to export")
        return
    
    df = pd.DataFrame(data_list)
    
    print(f"\nData Export Summary:")
    print(f"  Total records scraped: {len(df)}")
    
    initial_count = len(df)
    df = df.drop_duplicates(subset=['product_url'], keep='first')
    duplicates_removed = initial_count - len(df)
    print(f"  Duplicates removed: {duplicates_removed}")
    print(f"  Final records: {len(df)}")
    
    df['price'] = pd.to_numeric(df['price'], errors='coerce').fillna(0.0)
   
    df['description'] = df['description'].fillna("")
    df['image_url'] = df['image_url'].fillna("")
    
   
    df.to_csv('data/products.csv', index=False, encoding='utf-8')
    print(f"  Exported: data/products.csv")
    
    summary = df.groupby(['category', 'subcategory']).agg(
        total_products=('title', 'count'),
        average_price=('price', 'mean'),
        min_price=('price', 'min'),
        max_price=('price', 'max'),
        missing_descriptions=('description', lambda x: (x == "").sum()),
        products_with_images=('image_url', lambda x: (x != "").sum())
    ).reset_index()
    
    summary['duplicates_removed'] = summary.apply(
        lambda row: duplicates_removed if len(df) > 0 else 0, axis=1
    )
    
    
    summary['average_price'] = summary['average_price'].round(2)
    summary['min_price'] = summary['min_price'].round(2)
    summary['max_price'] = summary['max_price'].round(2)
    
    summary.to_csv('data/category_summary.csv', index=False, encoding='utf-8')
    print(f"  Exported: data/category_summary.csv")
    
    
    print(f"\nCategory Summary:")
    print(summary.to_string(index=False))