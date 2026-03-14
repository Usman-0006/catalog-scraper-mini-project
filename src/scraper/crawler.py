from .utils import get_html, resolve_url
from .parsers import parse_products_from_listing, parse_product_details

BASE_URL = "https://webscraper.io/test-sites/e-commerce/static"


def crawl_products():

    products = []

    start_html = get_html(BASE_URL)

    if not start_html:
        return products

    listing = parse_products_from_listing(start_html)

    for product in listing:

        product_url = resolve_url(BASE_URL, product["url"])

        html = get_html(product_url)

        if not html:
            continue

        details = parse_product_details(html)

        product.update(details)

        product["product_url"] = product_url

        products.append(product)

    return products