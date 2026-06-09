import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql+psycopg2://",
    connect_args={
        "host": "localhost",
        "port": "5432",
        "dbname": "quick_commerce",
        "user": "postgres",
        "password": "ginnivinni100@"
    }
)

# Export all data
df = pd.read_sql("SELECT * FROM products", engine)
df.to_csv("dashboard/products_data.csv", index=False)
print(f"Exported {len(df)} records to dashboard/products_data.csv")