from scraper.crawler import crawl_products
from scraper.exporters import export_products, export_summary


def main():

    print("Starting scraper...")

    products = crawl_products()

    print("Products scraped:", len(products))

    df = export_products(products)

    export_summary(df)

    print("Files saved in data folder")


if __name__ == "__main__":
    main()