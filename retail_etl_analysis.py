"""
retail_etl_analysis.py (SQLAlchemy version)
- Loads CSVs into MySQL using SQLAlchemy (mysql+mysqlconnector)
- Runs basic analysis with pandas and writes Excel summaries for Tableau
- Usage: python3 retail_etl_analysis.py
"""

import os
import pandas as pd
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus

# DB CONFIG (preconfigured)
USER = "root"
PASSWORD = quote_plus("binit@14")
HOST = "localhost"
DB = "retail_sales_db"
PORT = 3306

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "data_files")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# SQLAlchemy engine
engine = create_engine(f"mysql+mysqlconnector://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}", pool_pre_ping=True)

def create_schema():
    raw_sql_path = os.path.join(BASE_DIR, "schema_and_queries.sql")
    with open(raw_sql_path, "r") as f:
        sql = f.read()
    engine_no_db = create_engine(f"mysql+mysqlconnector://{USER}:{PASSWORD}@{HOST}:{PORT}", pool_pre_ping=True)
    with engine_no_db.connect() as conn:
        for stmt in [s.strip() for s in sql.split(";") if s.strip()]:
            try:
                conn.execute(text(stmt))
            except Exception as e:
                print("Skipping statement (may exist already):", e)
    engine_no_db.dispose()

def load_table_from_csv(table_name, csv_file):
    path = os.path.join(DATA_DIR, csv_file)
    df = pd.read_csv(path)
    if table_name == "sales":
        df["date"] = pd.to_datetime(df["date"])
    df.to_sql(name=table_name, con=engine, if_exists="append", index=False, method='multi', chunksize=2000)
    print(f"✅ Loaded {len(df)} rows into {table_name}")

def analyze_and_export():
    query = """
    SELECT sa.sale_id, sa.date, sa.quantity, sa.total_amount,
           p.product_id, p.product_name, p.category, p.sub_category, p.price,
           s.store_id, s.store_name, s.city, s.region,
           c.customer_id, c.customer_name, c.region AS customer_region, c.gender, c.age_group
    FROM sales sa
    JOIN products p ON sa.product_id = p.product_id
    JOIN stores s ON sa.store_id = s.store_id
    JOIN customers c ON sa.customer_id = c.customer_id
    """
    df = pd.read_sql_query(query, engine)
    df["month"] = pd.to_datetime(df["date"]).dt.to_period("M").astype(str)

    regional_rev = df.groupby(["region"])["total_amount"].sum().reset_index().sort_values("total_amount", ascending=False)
    regional_rev.to_excel(os.path.join(OUTPUT_DIR, "regional_revenue.xlsx"), index=False)

    monthly_rev = df.groupby(["month"])["total_amount"].sum().reset_index().sort_values("month")
    monthly_rev.to_excel(os.path.join(OUTPUT_DIR, "monthly_revenue.xlsx"), index=False)

    top_products = df.groupby(["product_id","product_name"])["total_amount"].sum().reset_index().sort_values("total_amount", ascending=False).head(20)
    top_products.to_excel(os.path.join(OUTPUT_DIR, "top_products.xlsx"), index=False)

    print("🎯 Analysis complete. Excel files saved to 'output' folder.")

def main():
    create_schema()
    load_table_from_csv("products", "products.csv")
    load_table_from_csv("stores", "stores.csv")
    load_table_from_csv("customers", "customers.csv")
    load_table_from_csv("sales", "sales.csv")
    analyze_and_export()

if __name__ == '__main__':
    main()
