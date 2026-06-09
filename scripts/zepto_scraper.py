from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from sqlalchemy import text
import pandas as pd
import time
from db_connect import get_engine

CITIES = {
    "Delhi": {"lat": 28.6139, "lon": 77.2090},
    "Mumbai": {"lat": 19.0760, "lon": 72.8777},
    "Bangalore": {"lat": 12.9716, "lon": 77.5946},
}

def create_driver(city="Delhi"):
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    
    coords = CITIES[city]
    driver.execute_cdp_cmd("Emulation.setGeolocationOverride", {
        "latitude": coords["lat"],
        "longitude": coords["lon"],
        "accuracy": 100
    })
    
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    print(f"GPS set to {city}: {coords['lat']}, {coords['lon']}")
    return driver

def scrape_zepto(driver, search_term, city):
    print(f"Searching {search_term} in {city} on Zepto...")
    
    driver.get(f"https://www.zeptonow.com/search?query={search_term}")
    time.sleep(5)
    
    for _ in range(5):
        driver.execute_script("window.scrollBy(0, 800)")
        time.sleep(1)
    driver.execute_script("window.scrollTo(0, 0)")
    time.sleep(1)
    
    products = []
    
    try:
        images = driver.find_elements(
            By.XPATH, "//div[@data-slot-id='ProductImageWrapper']//img[@alt]"
        )
        
        price_elements = driver.find_elements(
            By.XPATH, "//*[@data-slot-id='EdlpPrice']"
        )
        
        print(f"Found {len(images)} images and {len(price_elements)} prices")
        
        for i in range(min(len(images), len(price_elements))):
            try:
                name = images[i].get_attribute("alt").strip()
                
                price_text = price_elements[i].text.strip()
                price_lines = [p.replace("₹", "").replace(",", "").strip()
                               for p in price_text.split("\n") if p.strip()]
                
                price = float(price_lines[0]) if price_lines else 0
                original_price = float(price_lines[1]) if len(price_lines) > 1 else price
                discount = round(((original_price - price) / original_price * 100), 2) if original_price > price else 0
                
                if name and price > 0 and len(name) > 5:
                    products.append({
                        "platform": "Zepto",
                        "city": city,
                        "product_name": name,
                        "category": search_term,
                        "price": price,
                        "original_price": original_price,
                        "discount_percentage": discount,
                        "in_stock": True,
                        "scraped_date": pd.Timestamp.today().date()
                    })
            except:
                continue
    
    except Exception as e:
        print(f"Zepto scraping failed: {e}")
    
    return products

def save_to_db(products):
    if not products:
        print("No products to save")
        return
    engine = get_engine()
    
    with engine.connect() as conn:
        conn.execute(
            text("DELETE FROM products WHERE platform = 'Zepto' AND scraped_date = CURRENT_DATE")
        )
        conn.commit()
    print("Cleared today's Zepto data")
    
    df = pd.DataFrame(products)
    df.to_sql("products", engine, if_exists="append", index=False)
    print(f"Saved {len(products)} products!")

if __name__ == "__main__":
    search_terms = ["milk", "bread", "eggs", "butter", "chips",
                "biscuits", "rice", "dal", "sugar", "tea",
                "shampoo", "soap", "toothpaste", "noodles", "juice"]
    
    cities = ["Delhi", "Mumbai", "Bangalore"]
    all_products = []
    
    for city in cities:
        print(f"\n===== Scraping Zepto {city} =====")
        driver = create_driver(city)
        
        try:
            driver.get("https://www.zeptonow.com")
            time.sleep(5)
            
            for term in search_terms:
                products = scrape_zepto(driver, term, city)
                all_products.extend(products)
                time.sleep(3)
        
        finally:
            driver.quit()
    
    save_to_db(all_products)
    print(f"\nTotal Zepto products: {len(all_products)}")