from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
from db_connect import get_engine

CITIES = {
    "Delhi": {"lat": 28.6139, "lon": 77.2090},
    "Mumbai": {"lat": 19.0760, "lon": 72.8777},
    "Bangalore": {"lat": 12.9716, "lon": 77.5946},
    "Hyderabad": {"lat": 17.3850, "lon": 78.4867}
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

def set_location_via_url(driver, city="Delhi"):
    print(f"Opening Blinkit for {city}...")
    coords = CITIES[city]
    url = f"https://blinkit.com/?lat={coords['lat']}&lon={coords['lon']}"
    driver.get(url)
    time.sleep(5)
    
    try:
        wait = WebDriverWait(driver, 5)
        allow_btn = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//*[contains(text(),'Allow') or contains(text(),'allow')]")
        ))
        allow_btn.click()
        print("Allowed location access!")
        time.sleep(3)
    except:
        print("No location popup appeared — continuing...")

def search_and_scrape(driver, search_term, city, platform="Blinkit"):
    print(f"Searching for {search_term} in {city}...")
    
    driver.get(f"https://blinkit.com/s/?q={search_term}")
    time.sleep(4)
    # Scroll down to load all products
    for _ in range(5):
        driver.execute_script("window.scrollBy(0, 800)")
        time.sleep(1)
    driver.execute_script("window.scrollTo(0, 0)")
    time.sleep(1)
    
    products = []
    
    try:
        product_names = driver.find_elements(
            By.XPATH, "//*[contains(@class,'tw-text-300') and contains(@class,'tw-font-semibold')]"
        )
        price_elements = driver.find_elements(
            By.XPATH, "//*[contains(@class,'tw-text-200') and contains(@class,'tw-font-semibold') and contains(text(),'₹')]"
        )
        
        print(f"Found {len(product_names)} names and {len(price_elements)} prices")
        
        for i in range(min(len(product_names), len(price_elements))):
            try:
                name = product_names[i].text.strip()
                price_text = price_elements[i].text.replace("₹", "").replace(",", "").strip()
                price = float(price_text) if price_text else 0
                
                if name and price > 0 and len(name) > 5 and name != "ADD" and not any(p["product_name"] == name and p["category"] == search_term for p in products):
                    products.append({
                        "platform": platform,
                        "city": city,
                        "product_name": name,
                        "category": search_term,
                        "price": price,
                        "original_price": price,
                        "discount_percentage": 0,
                        "in_stock": True,
                        "scraped_date": pd.Timestamp.today().date()
                    })
            except Exception as e:
                continue
    
    except Exception as e:
        print(f"Scraping failed for {search_term}: {e}")
    
    return products

def save_to_db(products):
    if not products:
        print("No products to save")
        return
    engine = get_engine()
    from sqlalchemy import text
    with engine.connect() as conn:
        conn.execute(
            text("DELETE FROM products WHERE platform = 'Blinkit' AND scraped_date = CURRENT_DATE")
        )
        conn.commit()
    print("Cleared today's Blinkit data")
    df = pd.DataFrame(products)
    df.to_sql("products", engine, if_exists="append", index=False)
    print(f"Saved {len(products)} products to database!")

search_terms = [
    "milk", "bread", "eggs", "butter", "chips",
    "biscuits", "rice", "dal", "sugar", "tea",
    "shampoo", "soap", "toothpaste", "noodles", "juice"
]

cities = ["Delhi", "Mumbai", "Bangalore"]
all_products = []

for city in cities:
    print(f"\n========== Scraping {city} ==========")
    driver = create_driver(city)
    
    try:
        set_location_via_url(driver, city)
        
        for term in search_terms:
            products = search_and_scrape(driver, term, city)
            all_products.extend(products)
            time.sleep(3)
    
    finally:
        driver.quit()

save_to_db(all_products)
print(f"\nTotal products scraped across all cities: {len(all_products)}")