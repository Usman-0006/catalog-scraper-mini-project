from .utils import clean_price, clean_text, resolve_url

BASE_URL = "https://webscraper.io/test-sites/e-commerce/static"

def parse_product_details(soup, url, category, subcategory, page_ref):
    """Extract product details from product page (Requirement: Detail page scraping)"""
    try:
        title = soup.select_one('div.caption h4:nth-of-type(2)')
        price = soup.select_one('h4.price')
        desc = soup.select_one('p.description')
        reviews = soup.select_one('div.ratings p.pull-right')
        
        # Extract image URL (Requirement: Image URL optional)
        image_elem = soup.select_one('div.thumbnail img')
        image_url = resolve_url(BASE_URL, image_elem.get('src')) if image_elem else ""
        
        # Extract additional specs if available
        specs = soup.select('div.well p')
        detail_spec = clean_text(specs[0].text) if specs else "Static Test Site Item"
        
        return {
            "category": category,
            "subcategory": subcategory,
            "title": clean_text(title.text) if title else "N/A",
            "price": clean_price(price.text) if price else 0.0,
            "product_url": url,
            "image_url": image_url,
            "description": clean_text(desc.text) if desc else "",
            "review_count": clean_text(reviews.text) if reviews else "0 reviews",
            "detail_spec": detail_spec,
            "source_page": page_ref
        }
    except Exception as e:
        print(f"Error parsing product details from {url}: {e}")
        return {
            "category": category,
            "subcategory": subcategory,
            "title": "ERROR",
            "price": 0.0,
            "product_url": url,
            "image_url": "",
            "description": "",
            "review_count": "0 reviews",
            "detail_spec": "",
            "source_page": page_ref
        }