
from urllib.parse import urljoin
import re

def resolve_url(base, path):
    """
    Resolve relative URLs to absolute URLs (Requirement 4: URL resolution)
    
    Args:
        base: Base URL (e.g., https://example.com)
        path: Relative or absolute path
    
    Returns:
        Absolute URL
    """
    if not path:
        return ""
    return urljoin(base, path)

def clean_price(price_str):
    """
    Extract numeric price from string (Requirement 6: Data cleaning)
    
    Examples:
        "$12.99" -> 12.99
        "Price: $5.50" -> 5.50
        "" -> 0.0
    
    Args:
        price_str: Price string
    
    Returns:
        Float price value, or 0.0 if parse fails
    """
    if not price_str:
        return 0.0
    try:
        # Remove all non-numeric characters except decimal point
        cleaned = re.sub(r'[^\d.]', '', str(price_str).strip())
        return float(cleaned) if cleaned else 0.0
    except (ValueError, TypeError):
        return 0.0

def clean_text(text):
    """
    Clean whitespace and normalize text (Requirement 6: Data cleaning)
    
    Removes extra spaces, tabs, newlines, etc.
    
    Args:
        text: Text to clean
    
    Returns:
        Cleaned text string
    """
    if not text:
        return ""
    # Collapse multiple whitespaces and strip
    return " ".join(str(text).split())

def deduplicate_by_url(products):
    """
    Remove duplicate products by URL (Requirement 5: Deduplication)
    
    Args:
        products: List of product dictionaries
    
    Returns:
        List with duplicates removed, preserving order
    """
    seen = set()
    unique = []
    for product in products:
        url = product.get('product_url')
        if url not in seen:
            seen.add(url)
            unique.append(product)
    return unique
