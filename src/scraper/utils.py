from urllib.parse import urljoin
import requests

def get_html(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except Exception:
        return None


def clean_text(text):
    if text:
        return text.strip()
    return ""


def normalize_price(price):
    try:
        price = price.replace("$", "").strip()
        return float(price)
    except:
        return None


def resolve_url(base, link):
    return urljoin(base, link)