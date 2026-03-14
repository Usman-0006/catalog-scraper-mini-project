import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from scraper.crawler import discover_categories, get_all_products_from_subcategory
from scraper.exporters import export_results

def main():
    """Main scraper workflow"""
    print("=" * 60)
    print("E-Commerce Scraper Starting")
    print("=" * 60)
    
    print("\n[Step 1] Discovering categories and subcategories...")
    categories = discover_categories()
    
    if not categories:
        print("ERROR: No categories found. Aborting.")
        return
    
    print(f"\n[OK] Found {len(categories)} subcategories total.\n")
    
    all_products = []
    
    print("[Step 2] Scraping products from each subcategory...")
    for idx, cat in enumerate(categories, 1):
        category = cat['category']
        subcategory = cat['subcategory']
        url = cat['url']
        
        print(f"\n({idx}/{len(categories)}) Scraping: {category} > {subcategory}")
        try:
            products = get_all_products_from_subcategory(url, category, subcategory)
            all_products.extend(products)
            print(f"  [OK] Collected {len(products)} products")
        except Exception as e:
            print(f"  [ERROR] Error scraping {category} > {subcategory}: {e}")
            continue
    
    print(f"\n[Step 3] Processing and exporting data...")
    print(f"Total products collected: {len(all_products)}")
    
    if all_products:
        export_results(all_products)
        print("\n" + "=" * 60)
        print("[OK] Scraping complete! Check the /data folder.")
        print("=" * 60)
    else:
        print("\n[ERROR] No products were scraped. Check for errors above.")

if __name__ == "__main__":
    main()