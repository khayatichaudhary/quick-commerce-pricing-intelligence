import requests
import pandas as pd
import time
from db_connect import get_engine

# Headers from Blinkit's API
headers = {
    "authority": "blinkit.com",
    "accept": "*/*",
    "accept-language": "en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7",
    "access_token": "null",
    "app_client": "consumer_web",
    "app_version": "1010101010",
    "auth_key": "c761ec3633c22afad934fb17a66385c1c06c5472b4898b866b7306186d0bb477",
    "content-type": "application/json",
    "device_id": "4a4654d04de80abc",
    "lat": "28.5561437",
    "lon": "77.0999623",
    "origin": "https://blinkit.com",
    "referer": "https://blinkit.com/s/?q=milk",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36",
}

# Search function
def search_products(query, city="Delhi"):
    url = f"https://blinkit.com/v1/layout/search?q={query}&search_type=type_to_search"
    
    try:
        response = requests.post(url, headers=headers, json={})
        print(f"Status code: {response.status_code}")
        print(f"Response text: {response.text[:500]}")
        data = response.json()
        
        if not data.get("is_success"):
            print(f"API returned unsuccessful response for {query}")
            return []
        
        products = []
        # Navigate through response to find products
        snippets = data.get("response", {}).get("snippets", [])
        
        for snippet in snippets:
            items = snippet.get("data", {}).get("items", [])
            for item in items:
                product = item.get("product", {})
                if product:
                    name = product.get("name", "")
                    price = product.get("price", 0)
                    mrp = product.get("mrp", 0)
                    discount = round(((mrp - price) / mrp * 100), 2) if mrp > 0 else 0
                    category = product.get("category", "")
                    in_stock = product.get("is_available", True)
                    
                    products.append({
                        "platform": "Blinkit",
                        "city": city,
                        "product_name": name,
                        "category": category,
                        "price": price,
                        "original_price": mrp,
                        "discount_percentage": discount,
                        "in_stock": in_stock
                    })
        
        print(f"Found {len(products)} products for '{query}'")
        return products
    
    except Exception as e:
        print(f"Error scraping {query}: {e}")
        return []

# Save to database
def save_to_db(products):
    if not products:
        print("No products to save")
        return
    
    engine = get_engine()
    df = pd.DataFrame(products)
    df.to_sql("products", engine, if_exists="append", index=False)
    print(f"Saved {len(products)} products to database!")

# Main function
if __name__ == "__main__":
    search_terms = ["milk", "bread", "eggs", "butter", "chips"]
    all_products = []
    
    for term in search_terms:
        products = search_products(term)
        all_products.extend(products)
        time.sleep(2)  # Wait 2 seconds between requests to be respectful
    
    save_to_db(all_products)
    print(f"Total products scraped: {len(all_products)}")