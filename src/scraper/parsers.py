from bs4 import BeautifulSoup
from .utils import clean_text, normalize_price

def parse_categories(html):
    """Return list of (category_name, url)"""
    soup = BeautifulSoup(html, "html.parser")
    categories = []
    for link in soup.select(".sidebar-nav a"):
        name = clean_text(link.text)
        url = link.get("href")
        categories.append((name, url))
    return categories

def parse_products_from_listing(html):
    """Return products from listing page"""
    soup = BeautifulSoup(html, "html.parser")
    products = []

    for card in soup.select(".thumbnail"):
        title_tag = card.select_one(".title")
        price_tag = card.select_one(".price")

        if not title_tag or not price_tag:
            continue

        title = clean_text(title_tag.text)
        url = title_tag.get("href")
        price = normalize_price(price_tag.text)

        products.append({
            "title": title,
            "url": url,
            "price": price
        })
    return products

def parse_product_details(html):
    """Return additional details from product page"""
    soup = BeautifulSoup(html, "html.parser")

    desc_tag = soup.select_one(".description")
    description = clean_text(desc_tag.text) if desc_tag else ""

    # review count or rating if exists
    review_tag = soup.select_one(".ratings p.pull-right")
    review_count = clean_text(review_tag.text) if review_tag else ""

    return {
        "description": description,
        "review_count": review_count
    }