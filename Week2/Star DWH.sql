-- Star Schema
-- Dimension tables
CREATE TABLE DIM_PRODUCT (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100),
    category VARCHAR(50),
    unit_price DECIMAL(10, 2),
    supplier_id INT
);

CREATE TABLE DIM_STORE (
    store_id INT PRIMARY KEY,
    store_name VARCHAR(100),
    city VARCHAR(50),
    state VARCHAR(50),
    country VARCHAR(50)
);

CREATE TABLE DIM_DATE (
    date_id INT PRIMARY KEY,
    full_date DATE,
    year INT,
    quarter INT,
    month INT,
    day INT,
    day_of_week VARCHAR(10)
);

CREATE TABLE DIM_CUSTOMER (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(100),
    email VARCHAR(100),
    city VARCHAR(50),
    state VARCHAR(50),
    country VARCHAR(50)
);

-- Fact table
CREATE TABLE FACT_SALES (
    sale_id INT PRIMARY KEY,
    product_id INT,
    store_id INT,
    date_id INT,
    customer_id INT,
    quantity INT,
    total_amount DECIMAL(10, 2),
    FOREIGN KEY (product_id) REFERENCES DIM_PRODUCT(product_id),
    FOREIGN KEY (store_id) REFERENCES DIM_STORE(store_id),
    FOREIGN KEY (date_id) REFERENCES DIM_DATE(date_id),
    FOREIGN KEY (customer_id) REFERENCES DIM_CUSTOMER(customer_id)
);

-- Create indexes for better query performance in Star Schema
CREATE INDEX idx_product ON FACT_SALES(product_id);
CREATE INDEX idx_store ON FACT_SALES(store_id);
CREATE INDEX idx_date ON FACT_SALES(date_id);
CREATE INDEX idx_customer ON FACT_SALES(customer_id);