
# Retail Sales Insights Dashboard (Sportswear)

## Overview
This project is a ready-to-run sportswear retail analytics pipeline using Python (pandas), SQLAlchemy (MySQL), and Tableau.
It includes synthetic datasets (50k sales), SQL schema, an ETL/analysis script, and sample outputs for Tableau.

## Files
- data_files/products.csv
- data_files/stores.csv
- data_files/customers.csv
- data_files/sales.csv
- schema_and_queries.sql
- retail_etl_analysis.py
- output/ (generated Excel summaries)
- README.md

## Requirements
- Python 3.9+ (3.11 tested)
- MySQL Server (local or remote)
- Python packages: pandas, sqlalchemy, mysql-connector-python, openpyxl
  Install with:
  ```bash
  pip install pandas sqlalchemy mysql-connector-python openpyxl
  ```

## MySQL Credentials (preconfigured in script)
- Host: localhost
- Port: 3306
- User: root
- Password: your_password
- Database: retail_sales_db

## Quick Start
1. Unzip the project folder.
2. Ensure MySQL server is running and accessible with correct credentials.
3. From the project root folder, run:
   ```bash
   python3 retail_etl_analysis.py
   ```
   This will create the database & tables, load CSVs, and generate Excel summaries in the `output/` folder.

## Tableau setup and connection guide (macOS)
1. Download Tableau Public (free) or Tableau Desktop (trial) from: https://www.tableau.com/
2. Install following the vendor instructions for your OS.
3. Open Tableau and choose **"MySQL"** under connectors (or use **"Microsoft Excel"** to load generated Excel files).
4. If connecting to MySQL:
   - Host: `localhost`
   - Port: `3306`
   - Username: `root`
   - Password: `your_password`
   - Database: `retail_sales_db`
5. Recommended Tableau sheets to build:
   - Regional Revenue (bar chart or map) using `output/regional_revenue.xlsx` or directly from DB
   - Monthly Revenue Trend (line chart) from `output/monthly_revenue.xlsx`
   - Top Products (bar chart) from `output/top_products.xlsx`
   - Customer segments: age_group vs revenue, gender vs revenue (use full DB if needed)
6. Publish dashboard to Tableau Public (optional) to showcase on your portfolio.
   - Check mine: https://public.tableau.com/app/profile/binit.semwal/viz/Retail_Sportswear_Analysis/

## Notes
- To re-generate data or change volume, replace CSVs in `data_files/`.
