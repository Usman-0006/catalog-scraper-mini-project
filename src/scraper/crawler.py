from .utils import get_html, resolve_url
from .parsers import parse_categories, parse_products_from_listing, parse_product_details
from bs4 import BeautifulSoup
import time

BASE_URL = "https://webscraper.io/test-sites/e-commerce/static"

def crawl_all_products():
    all_products = []

    main_html = get_html(BASE_URL)
    if not main_html:
        return all_products

    categories = parse_categories(main_html)

    for category_name, category_url in categories:
        category_url = resolve_url(BASE_URL, category_url)
        print(f"Scraping category: {category_name}")

        subcat_html = get_html(category_url)
        if not subcat_html:
            continue

        subcategories = parse_categories(subcat_html)
        if not subcategories:
            subcategories = [(category_name, category_url)]

        for subcat_name, subcat_url in subcategories:
            subcat_url = resolve_url(BASE_URL, subcat_url)
            print(f"  Scraping subcategory: {subcat_name}")

            page = 1
            while True:
                paged_url = f"{subcat_url}?page={page}"
                page_html = get_html(paged_url)
                if not page_html:
                    break

                products = parse_products_from_listing(page_html)
                if not products:
                    break

                print(f"    Page {page}: {len(products)} products found")

                for product in products:
                    product_url = resolve_url(BASE_URL, product["url"])
                    html = get_html(product_url)
                    if not html:
                        continue

                    details = parse_product_details(html)
                    product.update(details)
                    product["category"] = category_name
                    product["subcategory"] = subcat_name
                    product["product_url"] = product_url
                    all_products.append(product)

                    # Optional: short delay to be safe
                    time.sleep(0.2)

                # Check if “Next” page exists
                soup = BeautifulSoup(page_html, "html.parser")
                next_btn = soup.select_one(".pagination li.active + li a")
                if not next_btn:
                    break

                page += 1

    return all_products