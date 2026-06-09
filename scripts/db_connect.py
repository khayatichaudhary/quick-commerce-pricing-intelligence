import psycopg2
from sqlalchemy import create_engine
import pandas as pd

# Database connection details
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "quick_commerce"
DB_USER = "postgres"
DB_PASSWORD = "password_here"  

def test_connection():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        print("✅ Database connected successfully!")
        conn.close()
    except Exception as e:
        print(f"❌ Connection failed: {e}")

def get_engine():
    engine = create_engine(
        "postgresql+psycopg2://",
        connect_args={
            "host": DB_HOST,
            "port": DB_PORT,
            "dbname": DB_NAME,
            "user": DB_USER,
            "password": DB_PASSWORD
        }
    )
    return engine

def test_save():
    engine = get_engine()
    test_data = pd.DataFrame({
        "platform": ["Blinkit"],
        "city": ["Delhi"],
        "product_name": ["Test Product"],
        "category": ["Test"],
        "price": [100.00],
        "original_price": [120.00],
        "discount_percentage": [16.67],
        "in_stock": [True]
    })
    test_data.to_sql("products", engine, if_exists="append", index=False)
    print("✅ Test data saved successfully!")

if __name__ == "__main__":
    test_connection()
    test_save()