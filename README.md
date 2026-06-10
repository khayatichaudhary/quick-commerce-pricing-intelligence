# Quick Commerce Pricing Intelligence 🛒

A data engineering and analytics project tracking live pricing across Blinkit and Zepto — India's two largest quick commerce platforms.

## Background

Quick commerce has grown rapidly in India with Blinkit and Zepto competing aggressively for the same customers. I wanted to understand whether they actually price differently, and if so, why. This project collects daily pricing data automatically and analyses the patterns.

## What the data shows 📊

Collected 22,800+ product records across Delhi, Mumbai and Bangalore over multiple days. A few findings stood out:

Blinkit displays full MRP on every product with zero discounts. Zepto discounts nearly 90% of its catalog at an average 19% off. This suggests two fundamentally different pricing strategies — Blinkit competing on trust and convenience while Zepto competes on perceived value.

Zepto also maintains a nearly identical product catalog across all three cities (98% consistency) while Blinkit's catalog varies significantly by city (only 32% overlap). This points to a hyperlocal inventory model for Blinkit versus a standardised national approach for Zepto.

A Random Forest classifier trained on category and price data predicts high-discount products on Zepto with 87% accuracy. Rice and dal show the highest discount probability at 82% and 81% respectively.

## How it works ⚙️

Data is collected daily using Selenium with Chrome DevTools Protocol for GPS spoofing across cities. Products are stored in PostgreSQL and matched across platforms using TF-IDF vectorization — which found 550 comparable products versus only 27 from exact string matching.

Analysis and modelling done in Jupyter. Results visualised in an interactive Power BI dashboard.

## Stack 🛠️

Python, Selenium, PostgreSQL, SQLAlchemy, Pandas, Scikit-learn, Power BI, Windows Task Scheduler

## Structure 📁
scripts/          scraping and database utilities
notebooks/        exploratory analysis and ML models
dashboard/        Power BI dashboard file
run_scraper.bat   daily automation script
scripts/          scraping and database utilities
notebooks/        exploratory analysis and ML models
dashboard/        Power BI dashboard file
run_scraper.bat   daily automation script

## Running locally

Clone the repo, install dependencies with pip install -r requirements.txt, configure your PostgreSQL credentials in db_connect.py and run the scrapers.

## Status 🔄

Data collection is ongoing daily. Dashboard refresh and full analysis report planned after 20 days of data.
