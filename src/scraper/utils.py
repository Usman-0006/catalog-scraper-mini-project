from urllib.parse import urljoin
import requests

def get_html(url):
    """Get HTML content safely"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Failed to fetch {url}: {e}")
        return None

def clean_text(text):
    """Strip whitespace and clean text"""
    if text:
        return text.strip()
    return ""

def normalize_price(price):
    """Convert price string to float"""
    try:
        price = price.replace("$", "").replace(",", "").strip()
        return float(price)
    except:
        return None

def resolve_url(base, link):
    """Join relative URLs to base"""
    return urljoin(base, link)