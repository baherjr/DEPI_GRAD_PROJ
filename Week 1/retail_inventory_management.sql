-- Drop Foreign Key Constraints (for manual cleanup if necessary)
-- ALTER TABLE Products DROP CONSTRAINT FK_Products_Suppliers;
-- ALTER TABLE Inventory DROP CONSTRAINT FK_Inventory_Products;
-- ALTER TABLE Sales DROP CONSTRAINT FK_Sales_Products;

-- Drop Tables if needed manually (for manual cleanup)
-- DROP TABLE IF EXISTS dbo.Suppliers;
-- DROP TABLE IF EXISTS dbo.Products;
-- DROP TABLE IF EXISTS dbo.Inventory;
-- DROP TABLE IF EXISTS dbo.Sales;

-- Create the Database and use it
CREATE DATABASE RetailInventoryManagement;
GO

USE RetailInventoryManagement;
GO

-- Suppliers Table
CREATE TABLE [dbo].[Suppliers] (
    [supplier_id] INT PRIMARY KEY,
    [supplier_name] VARCHAR(255) NOT NULL,
    [contact_info] VARCHAR(255) NOT NULL
) ON [PRIMARY];
GO

-- Products Table
CREATE TABLE [dbo].[Products] (
    [product_id] INT PRIMARY KEY,
    [product_name] VARCHAR(255) NOT NULL,
    [category] VARCHAR(100),
    [supplier_id] INT,
    [price] DECIMAL(10, 2),
    FOREIGN KEY (supplier_id) REFERENCES dbo.Suppliers(supplier_id)
) ON [PRIMARY];
GO

-- Inventory Table
CREATE TABLE [dbo].[Inventory] (
    [inventory_id] INT PRIMARY KEY,
    [product_id] INT,
    [warehouse_location] VARCHAR(255),
    [quantity_in_stock] INT,
    FOREIGN KEY (product_id) REFERENCES dbo.Products(product_id)
) ON [PRIMARY];
GO

-- Sales Table
CREATE TABLE [dbo].[Sales] (
    [sale_id] INT PRIMARY KEY,
    [product_id] INT,
    [quantity_sold] INT,
    [sale_date] DATE,
    [sale_price] DECIMAL(10, 2),
    FOREIGN KEY (product_id) REFERENCES dbo.Products(product_id)
) ON [PRIMARY];
GO



-- Sample Data 
INSERT INTO Suppliers (supplier_id, supplier_name, contact_info) 
VALUES 
    (1, 'Supplier A', 'contactA@example.com'), 
    (2, 'Supplier B', 'contactB@example.com'),
    (3, 'Supplier C', 'contactC@example.com'),
    (4, 'Supplier D', 'contactD@example.com'),
    (5, 'Supplier E', 'contactE@example.com');

INSERT INTO Suppliers (supplier_id, supplier_name, contact_info) 
VALUES 
    (6, 'Supplier F', 'contactF@example.com'),
    (7, 'Supplier G', 'contactG@example.com');



INSERT INTO Products (product_id, product_name, category, supplier_id, price) 
VALUES 
    (1, 'Laptop A', 'Electronics', 1, 1000.00),
    (2, 'Smartphone B', 'Electronics', 1, 700.00),
    (3, 'Tablet C', 'Electronics', 2, 400.00),
    (4, 'Headphones D', 'Accessories', 2, 150.00),
    (5, 'Keyboard E', 'Accessories', 3, 50.00),
    (6, 'Office Chair', 'Furniture', 4, 120.00),
    (7, 'Desk Lamp', 'Furniture', 4, 30.00),
    (8, 'Coffee Machine', 'Appliances', 5, 85.00),
    (9, 'Microwave Oven', 'Appliances', 5, 120.00),
    (10, 'Blender', 'Appliances', 5, 60.00);

INSERT INTO Products (product_id, product_name, category, supplier_id, price) 
VALUES 
    (11, 'Standing Desk', 'Furniture', 4, 300.00),
    (12, 'Wireless Mouse', 'Accessories', 3, 25.00),
    (13, 'Gaming Laptop', 'Electronics', 6, 1500.00),
    (14, 'Smartwatch', 'Electronics', 6, 250.00),
    (15, 'Air Conditioner', 'Appliances', 7, 400.00),
    (16, 'Water Heater', 'Appliances', 7, 350.00);

-- Adding unsold products for testing Query 9
INSERT INTO Products (product_id, product_name, category, supplier_id, price) 
VALUES 
    (17, 'Vacuum Cleaner', 'Appliances', 5, 150.00), 
    (18, 'Gaming Keyboard', 'Accessories', 3, 80.00);




INSERT INTO Inventory (inventory_id, product_id, warehouse_location, quantity_in_stock) 
VALUES 
    (1, 1, 'Warehouse 1', 20),
    (2, 2, 'Warehouse 1', 15),
    (3, 3, 'Warehouse 2', 30),
    (4, 4, 'Warehouse 2', 40),
    (5, 5, 'Warehouse 3', 50),
    (6, 6, 'Warehouse 3', 35),
    (7, 7, 'Warehouse 4', 60),
    (8, 8, 'Warehouse 4', 25),
    (9, 9, 'Warehouse 1', 10),
    (10, 10, 'Warehouse 2', 5);

INSERT INTO Inventory (inventory_id, product_id, warehouse_location, quantity_in_stock) 
VALUES 
    (11, 11, 'Warehouse 3', 20),
    (12, 12, 'Warehouse 1', 50),
    (13, 13, 'Warehouse 2', 15),
    (14, 14, 'Warehouse 4', 25),
    (15, 15, 'Warehouse 3', 8),   -- Air Conditioner, running low
    (16, 16, 'Warehouse 2', 10);  -- Water Heater, running low

INSERT INTO Sales (sale_id, product_id, quantity_sold, sale_date, sale_price) 
VALUES 
    (1, 1, 5, '2024-09-01', 950.00),  -- Laptop A sold at a discounted price
    (2, 2, 3, '2024-09-01', 700.00),  -- Smartphone B sold at full price
    (3, 3, 2, '2024-09-02', 400.00),  -- Tablet C
    (4, 4, 6, '2024-09-02', 150.00),  -- Headphones D
    (5, 5, 4, '2024-09-03', 45.00),   -- Keyboard E sold at a discounted price
    (6, 6, 1, '2024-09-03', 120.00),  -- Office Chair
    (7, 7, 3, '2024-09-04', 30.00),   -- Desk Lamp
    (8, 8, 2, '2024-09-05', 85.00),   -- Coffee Machine
    (9, 9, 1, '2024-09-05', 115.00),  -- Microwave Oven sold at a discounted price
    (10, 10, 4, '2024-09-06', 55.00); -- Blender sold at a discounted price


INSERT INTO Sales (sale_id, product_id, quantity_sold, sale_date, sale_price) 
VALUES 
    (11, 11, 3, '2024-09-07', 280.00),  -- Standing Desk sold at a discounted price
    (12, 12, 5, '2024-09-07', 25.00),   -- Wireless Mouse
    (13, 13, 2, '2024-09-08', 1500.00), -- Gaming Laptop
    (14, 14, 4, '2024-09-08', 240.00),  -- Smartwatch sold at a discounted price
    (15, 15, 1, '2024-09-09', 390.00),  -- Air Conditioner sold at a discounted price
    (16, 16, 2, '2024-09-09', 350.00);  -- Water Heater



-- SQL queries for inventory tracking and sales
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
