import requests
from bs4 import BeautifulSoup
from .utils import resolve_url
from .parsers import parse_product_details

BASE_URL = "https://webscraper.io/test-sites/e-commerce/static"

def get_soup(url):
    """Fetch and parse HTML with error handling"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error parsing {url}: {e}")
        return None

def discover_categories():
    """Discover site structure (Requirement 2: Category and subcategory traversal)"""
    soup = get_soup(BASE_URL)
    structure = []
    if not soup: 
        print("Failed to discover categories from base URL")
        return structure

    try:
        # Find Category links in side menu - skip the first link (Home)
        cats = soup.select('ul#side-menu > li > a')[1:]
        print(f"Discovering categories... found {len(cats)} categories")
        
        for c in cats:
            c_name = c.text.strip()
            c_url = resolve_url(BASE_URL, c.get('href'))
            
            # Find Subcategories
            sub_soup = get_soup(c_url)
            if sub_soup:
                subs = sub_soup.select('ul.nav-second-level li a')
                for sub in subs:
                    sub_name = sub.text.strip()
                    sub_url = resolve_url(BASE_URL, sub.get('href'))
                    structure.append({
                        "category": c_name,
                        "subcategory": sub_name,
                        "url": sub_url
                    })
                    print(f"  Found: {c_name} -> {sub_name}")
            else:
                print(f"Warning: Could not load category page for {c_name}")
    except Exception as e:
        print(f"Error discovering categories: {e}")
    
    return structure

def get_all_products_from_subcategory(sub_url, category, subcategory):
    """Follows pagination and collects product links (Requirement 1: Multi-page crawling)"""
    all_data = []
    current_url = sub_url
    page_num = 1
    max_pages = 50  # Safety limit to prevent infinite loops
    
    while current_url and page_num <= max_pages:
        soup = get_soup(current_url)
        if not soup:
            print(f"Failed to load page {page_num}")
            break
        
        try:
            # Collect product links from listing page
            links = soup.select('div.thumbnail a.title')
            print(f"  Page {page_num}: Found {len(links)} products")
            
            for link in links:
                try:
                    p_url = resolve_url(BASE_URL, link.get('href'))
                    p_soup = get_soup(p_url)
                    if p_soup:
                        # Requirement 3: Detail page scraping
                        product = parse_product_details(p_soup, p_url, category, subcategory, page_num)
                        all_data.append(product)
                except Exception as e:
                    print(f"Error processing product link: {e}")
                    continue
            
            # Requirement 4: URL resolution for pagination
            next_btn = soup.select_one('ul.pagination li a[aria-label="Next »"]')
            if next_btn and next_btn.get('href'):
                current_url = resolve_url(BASE_URL, next_btn.get('href'))
                page_num += 1
            else:
                current_url = None  # No more pages
        
        except Exception as e:
            print(f"Error processing page {page_num}: {e}")
            break
    
    return all_data