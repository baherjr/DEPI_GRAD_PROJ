-- Drop Foreign Key Constraints (for manual cleanup if necessary)
-- ALTER TABLE Products DROP CONSTRAINT IF EXISTS FK_Products_Suppliers;
-- ALTER TABLE Inventory DROP CONSTRAINT IF EXISTS FK_Inventory_Products;
-- ALTER TABLE Sales DROP CONSTRAINT IF EXISTS FK_Sales_Products;

-- Drop Tables if needed manually (for manual cleanup)
-- DROP TABLE IF EXISTS Suppliers CASCADE;
-- DROP TABLE IF EXISTS Products CASCADE;
-- DROP TABLE IF EXISTS Inventory CASCADE;
-- DROP TABLE IF EXISTS Sales CASCADE;

-- Create the Database
-- (No explicit command for database creation is required here since it's assumed you'll connect via pgAdmin to a specific DB)

-- Suppliers Table
CREATE TABLE Suppliers (
    supplier_id SERIAL PRIMARY KEY,
    supplier_name VARCHAR(255) NOT NULL,
    contact_info VARCHAR(255) NOT NULL
);

-- Products Table
CREATE TABLE Products (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    category VARCHAR(100),
    supplier_id INT REFERENCES Suppliers(supplier_id) ON DELETE SET NULL,
    price NUMERIC(10, 2)
);

-- Inventory Table
CREATE TABLE Inventory (
    inventory_id SERIAL PRIMARY KEY,
    product_id INT REFERENCES Products(product_id) ON DELETE CASCADE,
    warehouse_location VARCHAR(255),
    quantity_in_stock INT
);

-- Sales Table
CREATE TABLE Sales (
    sale_id SERIAL PRIMARY KEY,
    product_id INT REFERENCES Products(product_id) ON DELETE CASCADE,
    quantity_sold INT,
    sale_date DATE,
    sale_price NUMERIC(10, 2)
);

-- Insert Data into Suppliers
INSERT INTO Suppliers (supplier_name, contact_info) 
VALUES 
    ('Supplier A', 'contactA@example.com'), 
    ('Supplier B', 'contactB@example.com'),
    ('Supplier C', 'contactC@example.com'),
    ('Supplier D', 'contactD@example.com'),
    ('Supplier E', 'contactE@example.com'),
    ('Supplier F', 'contactF@example.com'),
    ('Supplier G', 'contactG@example.com');

-- Insert Data into Products
INSERT INTO Products (product_name, category, supplier_id, price) 
VALUES 
    ('Laptop A', 'Electronics', 1, 1000.00),
    ('Smartphone B', 'Electronics', 1, 700.00),
    ('Tablet C', 'Electronics', 2, 400.00),
    ('Headphones D', 'Accessories', 2, 150.00),
    ('Keyboard E', 'Accessories', 3, 50.00),
    ('Office Chair', 'Furniture', 4, 120.00),
    ('Desk Lamp', 'Furniture', 4, 30.00),
    ('Coffee Machine', 'Appliances', 5, 85.00),
    ('Microwave Oven', 'Appliances', 5, 120.00),
    ('Blender', 'Appliances', 5, 60.00),
    ('Standing Desk', 'Furniture', 4, 300.00),
    ('Wireless Mouse', 'Accessories', 3, 25.00),
    ('Gaming Laptop', 'Electronics', 6, 1500.00),
    ('Smartwatch', 'Electronics', 6, 250.00),
    ('Air Conditioner', 'Appliances', 7, 400.00),
    ('Water Heater', 'Appliances', 7, 350.00),
    ('Vacuum Cleaner', 'Appliances', 5, 150.00), 
    ('Gaming Keyboard', 'Accessories', 3, 80.00);

-- Insert Data into Inventory
INSERT INTO Inventory (product_id, warehouse_location, quantity_in_stock) 
VALUES 
    (1, 'Warehouse 1', 20),
    (2, 'Warehouse 1', 15),
    (3, 'Warehouse 2', 30),
    (4, 'Warehouse 2', 40),
    (5, 'Warehouse 3', 50),
    (6, 'Warehouse 3', 35),
    (7, 'Warehouse 4', 60),
    (8, 'Warehouse 4', 25),
    (9, 'Warehouse 1', 10),
    (10, 'Warehouse 2', 5),
    (11, 'Warehouse 3', 20),
    (12, 'Warehouse 1', 50),
    (13, 'Warehouse 2', 15),
    (14, 'Warehouse 4', 25),
    (15, 'Warehouse 3', 8),
    (16, 'Warehouse 2', 10);

-- Insert Data into Sales
INSERT INTO Sales (product_id, quantity_sold, sale_date, sale_price) 
VALUES 
    (1, 5, '2024-09-01', 950.00),  
    (2, 3, '2024-09-01', 700.00),
    (3, 2, '2024-09-02', 400.00),
    (4, 6, '2024-09-02', 150.00),
    (5, 4, '2024-09-03', 45.00),   
    (6, 1, '2024-09-03', 120.00),  
    (7, 3, '2024-09-04', 30.00),
    (8, 2, '2024-09-05', 85.00),   
    (9, 1, '2024-09-05', 115.00),  
    (10, 4, '2024-09-06', 55.00),  
    (11, 3, '2024-09-07', 280.00),  
    (12, 5, '2024-09-07', 25.00),
    (13, 2, '2024-09-08', 1500.00), 
    (14, 4, '2024-09-08', 240.00),
    (15, 1, '2024-09-09', 390.00),  
    (16, 2, '2024-09-09', 350.00);  

-- Queries for Inventory Tracking and Sales Analysis

-- Query 1: Products Running Low on Stock
SELECT p.product_name, i.warehouse_location, i.quantity_in_stock
FROM Products p
JOIN Inventory i ON p.product_id = i.product_id
WHERE i.quantity_in_stock < 10;

-- Query 2: Total Sales Revenue for Each Product
SELECT p.product_name, SUM(s.quantity_sold * s.sale_price) AS total_sales_revenue
FROM Products p
JOIN Sales s ON p.product_id = s.product_id
GROUP BY p.product_name
ORDER BY total_sales_revenue DESC;

-- Query 3: Daily Sales Summary
SELECT s.sale_date, SUM(s.sale_price * s.quantity_sold) AS daily_sales
FROM Sales s
GROUP BY s.sale_date
ORDER BY s.sale_date;

-- Query 4: Supplier-wise Product Distribution
SELECT su.supplier_name, COUNT(p.product_id) AS number_of_products
FROM Suppliers su
JOIN Products p ON su.supplier_id = p.supplier_id
GROUP BY su.supplier_name;

-- Query 5: Products with Highest Sales Volume
SELECT p.product_name, SUM(s.quantity_sold) AS total_quantity_sold
FROM Products p
JOIN Sales s ON p.product_id = s.product_id
GROUP BY p.product_name
ORDER BY total_quantity_sold DESC;

-- Query 6: Sales by Warehouse Location
SELECT i.warehouse_location, SUM(s.quantity_sold * s.sale_price) AS warehouse_sales
FROM Inventory i
JOIN Sales s ON i.product_id = s.product_id
GROUP BY i.warehouse_location
ORDER BY warehouse_sales DESC;

-- Query 7: Average Sales Price for Each Product
SELECT p.product_name, AVG(s.sale_price) AS avg_sale_price
FROM Products p
JOIN Sales s ON p.product_id = s.product_id
GROUP BY p.product_name
ORDER BY avg_sale_price DESC;

-- Query 8: Inventory Status by Supplier
SELECT su.supplier_name, SUM(i.quantity_in_stock) AS total_stock
FROM Suppliers su
JOIN Products p ON su.supplier_id = p.supplier_id
JOIN Inventory i ON p.product_id = i.product_id
GROUP BY su.supplier_name
ORDER BY total_stock DESC;

-- Query 9: Products Never Sold
SELECT p.product_name
FROM Products p
LEFT JOIN Sales s ON p.product_id = s.product_id
WHERE s.sale_id IS NULL;

-- Query 10: Most Popular Categories by Sales Revenue
SELECT p.category, SUM(s.quantity_sold * s.sale_price) AS total_category_sales
FROM Products p
JOIN Sales s ON p.product_id = s.product_id
GROUP BY p.category
ORDER BY total_category_sales DESC;
