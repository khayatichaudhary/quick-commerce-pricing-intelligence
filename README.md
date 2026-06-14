# 🛒 Quick Commerce Pricing Intelligence
### Zepto vs Blinkit — Price, Discount & Strategy Analysis

![Python](https://img.shields.io/badge/Python-3.13-blue) ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-18.1-blue) ![Selenium](https://img.shields.io/badge/Scraping-Selenium-green) ![ML](https://img.shields.io/badge/ML-RandomForest-orange)

---

## 📌 What I Built

I scraped, stored, and analyzed real pricing data from Blinkit and Zepto across 3 Indian cities over 10 days to figure out — are these platforms actually different in how they price things, or is it just perception?

**Data collected:** June 5–14, 2026 | **49,184 products** | **3 cities** | **15 categories**

---

## 🔍 What I Found

### 1. They have completely different catalog strategies
| Platform | Products Common Across Cities |
|----------|-------------------------------|
| Blinkit  | 32.41% — hyperlocal inventory |
| Zepto    | 98.32% — same catalog everywhere |

Blinkit stocks different products in Delhi vs Mumbai vs Bangalore. Zepto sells the same things everywhere. That alone tells you a lot about how they think about the market.

### 2. Their discount strategies are polar opposites
| Platform | Products Discounted | Avg Discount |
|----------|---------------------|--------------|
| Blinkit  | 0%                  | None         |
| Zepto    | 89.9%               | 19.25%       |

Zepto looks cheaper — but that's because almost everything is discounted, not because base prices are lower. Blinkit charges full MRP on everything.

### 3. Category-wise, Zepto wins almost everywhere
- Zepto cheapest on: **Tea (-42.8%)**, **Soap (-30.7%)**
- Only category where Blinkit is cheaper: **Noodles (+1.58%)**
- On matched products overall: **Zepto is 18.88% cheaper**

### 4. Blinkit prices move more aggressively day to day
- Blinkit: Soap jumped **+17.3% in a single day**
- Zepto: Max daily change was only **+4.66%**

This suggests they're running different pricing algorithms — Blinkit adjusts more frequently, Zepto stays stable.

---

## 🧠 ML Model — What I Actually Learned

I built 3 Random Forest models and the first two taught me something more useful than the actual predictions:

| Model | Accuracy | What's actually happening |
|-------|----------|--------------------------|
| Model 1 (All data) | 96% | Just learned "Zepto = discount, Blinkit = no discount" — useless |
| Model 2 (Zepto-only) | 88% | Still not useful — 89% of Zepto has discounts anyway |
| **Model 3 (Predict HIGH discount >20%)** | **87.15%** | ✅ This one actually solves something |

The 96% model looked impressive until I checked feature importance — platform alone was 79% of the signal. It wasn't predicting discounts, it was just identifying the platform. I rebuilt it as a Zepto-only model that predicts which products get deep discounts (>20%), which is actually useful for a consumer or a business.

**Top features for predicting high discounts:** Price (76%) → Category (23%) → City (1%)

---

## 🔧 Tech Stack

| Component | Technology |
|-----------|-----------|
| Scraping | Selenium + Python |
| Database | PostgreSQL 18.1 |
| Analysis | Pandas, NumPy |
| Visualization | Matplotlib, Seaborn |
| Product Matching | TF-IDF (cosine similarity) + RapidFuzz |
| ML | Scikit-learn (Random Forest) |
| Automation | Windows Batch Script (`run_scraper.bat`) |

---

## 📁 Project Structure

```
quick_commerce_pricing/
├── notebooks/
│   └── zepto_blinkit_analysis.ipynb   # Main analysis notebook
├── scripts/
│   ├── blinkit_scraper.py             # Blinkit Selenium scraper
│   ├── zepto_scraper.py               # Zepto Selenium scraper
│   ├── selenium_scraper.py            # Base scraper
│   ├── export_data.py                 # Data export utilities
│   └── db_connect_example.py          # DB connection template
├── data/                              # Raw scraped data
├── database/                          # DB schema and setup
├── .env.example                       # Environment variables template
├── .gitignore
├── run_scraper.bat                    # One-click scraping automation
└── README.md
```

---

## ⚙️ Setup & Usage

### 1. Clone the repo
```bash
git clone https://github.com/khayatichaudhary/quick-commerce-pricing-intelligence.git
cd quick-commerce-pricing-intelligence
```

### 2. Install dependencies
```bash
pip install pandas numpy matplotlib seaborn sqlalchemy psycopg2 selenium rapidfuzz scikit-learn python-dotenv
```

### 3. Configure environment
```bash
cp .env.example .env
# Edit .env with your PostgreSQL credentials
```

### 4. Run scrapers
```bash
run_scraper.bat   # Windows
# OR
python scripts/blinkit_scraper.py
python scripts/zepto_scraper.py
```

### 5. Run analysis
Open `notebooks/zepto_blinkit_analysis.ipynb` in Jupyter.

---

## ⚠️ Honest Limitations

- **Blinkit discount data**: My scraper recorded 0% discounts for Blinkit throughout the collection period. This could be their actual pricing strategy OR a scraping gap — I flagged it in the notebook and recommend manual verification on the app.
- **Data period**: 10 days is enough to see trends but not enough for seasonal patterns.
- **Quantity extraction**: Only 4.1% of products had quantities I could parse from the name — per-unit comparison has a small sample.
- **Cities**: Only Delhi, Mumbai, Bangalore. Tier-2 cities would be interesting to add.

---

## 👩‍💻 Author

**Khayati Chaudhary**  
Chemical Engineering, MNNIT Allahabad | Aspiring Data Analyst  
[GitHub](https://github.com/khayatichaudhary)
