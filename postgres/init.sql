--create commerce
CREATE SCHEMA commerce;

-- Use commerce schema
SET
    search_path TO commerce;

--create table users
CREATE TABLE users(
    id INT PRIMARY KEY,
    username VARCHAR (225) NOT NULL,
    password VARCHAR (225) NOT NULL
);

--create table products
CREATE TABLE products(
    id INT PRIMARY KEY,
    NAME VARCHAR(225) NOT NULL,
    description TEXT,
    price REAL NOT NULL
);

--Modify replica changes

ALTER TABLE 
    users REPLICA IDENTITY FULL;

ALTER TABLE
    products REPLICA IDENTITY FULL;

--create checkouts table enriched with userinfo
CREATE TABLE attributed_checkouts (
    checkout_id VARCHAR PRIMARY KEY,
    user_name VARCHAR,
    click_id VARCHAR,
    product_id VARCHAR,
    payment_method VARCHAR,
    total_amount DECIMAL(2,5),
    billing_address VARCHAR,
    shipping_address VARCHAR,
    user_agent VARCHAR,
    ip_address VARCHAR,
    click_time TIMESTAMP
);
