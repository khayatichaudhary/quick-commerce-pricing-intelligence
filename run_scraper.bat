@echo off
cd C:\Users\khaya\quick_commerce_pricing
call venv\Scripts\activate.bat
echo Running Blinkit scraper...
python scripts/selenium_scraper.py
echo Running Zepto scraper...
python scripts/zepto_scraper.py
echo All scraping completed!
pause