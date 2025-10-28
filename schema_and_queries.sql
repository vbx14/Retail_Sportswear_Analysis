
-- Schema for retail_sales_db (sportswear)
CREATE DATABASE IF NOT EXISTS retail_sales_db;
USE retail_sales_db;

DROP TABLE IF EXISTS sales;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS stores;

CREATE TABLE stores (
  store_id INT PRIMARY KEY,
  store_name VARCHAR(255),
  city VARCHAR(100),
  region VARCHAR(50)
);

CREATE TABLE products (
  product_id INT PRIMARY KEY,
  product_name VARCHAR(255),
  category VARCHAR(100),
  sub_category VARCHAR(100),
  price DECIMAL(10,2)
);

CREATE TABLE customers (
  customer_id INT PRIMARY KEY,
  customer_name VARCHAR(255),
  region VARCHAR(50),
  gender VARCHAR(20),
  age_group VARCHAR(20)
);

CREATE TABLE sales (
  sale_id INT PRIMARY KEY,
  product_id INT,
  customer_id INT,
  store_id INT,
  date DATE,
  quantity INT,
  total_amount DECIMAL(12,2),
  FOREIGN KEY (product_id) REFERENCES products(product_id),
  FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
  FOREIGN KEY (store_id) REFERENCES stores(store_id)
);
