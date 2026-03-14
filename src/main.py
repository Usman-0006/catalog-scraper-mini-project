from scraper.crawler import crawl_all_products
from scraper.exporters import export_products, export_summary

def main():
    print("Starting full scraper...")
    products = crawl_all_products()
    print(f"Total products scraped: {len(products)}")

    df = export_products(products)
    export_summary(df)

    print("CSV files saved in data/ folder")

if __name__ == "__main__":
    main()