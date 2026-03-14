from bs4 import BeautifulSoup
from .utils import clean_text, normalize_price

def parse_categories(html):
    soup = BeautifulSoup(html, "html.parser")
    categories = []

    for link in soup.select(".sidebar-nav a"):
        name = clean_text(link.text)
        url = link.get("href")
        categories.append((name, url))

    return categories


def parse_products_from_listing(html):
    soup = BeautifulSoup(html, "html.parser")
    products = []

    cards = soup.select(".thumbnail")

    for card in cards:

        title = clean_text(card.select_one(".title").text)
        url = card.select_one(".title")["href"]
        price = normalize_price(card.select_one(".price").text)

        products.append({
            "title": title,
            "url": url,
            "price": price
        })

    return products


def parse_product_details(html):

    soup = BeautifulSoup(html, "html.parser")

    description_tag = soup.select_one(".description")

    if description_tag:
        description = clean_text(description_tag.text)
    else:
        description = ""

    return {
        "description": description
    }