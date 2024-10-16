CREATE TABLE Vehicles (
    vehicle_id INT PRIMARY KEY,
    make VARCHAR(50),
    model VARCHAR(100),
    year INT,
    fuel_type VARCHAR(50),
    transmission VARCHAR(50),
    engine VARCHAR(50),
    color VARCHAR(50),
    seating_capacity INT,
    drivetrain VARCHAR(50),
    max_power VARCHAR(50),
    max_torque VARCHAR(50),
    price DECIMAL(10, 2),
    stock_level INT,
	fuel_efficiency DECIMAL(5, 2)
);
CREATE TABLE Dealerships (
    dealership_id INT PRIMARY KEY,
    location VARCHAR(100),
    owner_type VARCHAR(50),
    seller_type VARCHAR(50)
);
CREATE TABLE Sales (
    sale_id INT PRIMARY KEY,
    vehicle_id INT,
    dealership_id INT,
    sale_date DATE,
    quantity_sold INT,
    total_amount DECIMAL(10, 2),
    FOREIGN KEY (vehicle_id) REFERENCES Vehicles(vehicle_id),
    FOREIGN KEY (dealership_id) REFERENCES Dealerships(dealership_id)
);
CREATE TABLE Inventory (
    vehicle_id INT,
    stock_level INT,
    last_updated DATE,
    FOREIGN KEY (vehicle_id) REFERENCES Vehicles(vehicle_id)
);



INSERT INTO Vehicles (vehicle_id, make, model, year, fuel_type, transmission, engine, color, seating_capacity, drivetrain, max_power, max_torque, price, stock_level)
VALUES
    (1, 'Toyota', 'Camry', 2020, 'Petrol', 'Automatic', 'V6', 'Black', 5, 'FWD', '300 HP', '350 Nm', 28000.00, 10),
    (2, 'Honda', 'Civic', 2021, 'Diesel', 'Manual', 'I4', 'White', 5, 'FWD', '158 HP', '200 Nm', 22000.00, 15);
INSERT INTO Dealerships (dealership_id, location, owner_type, seller_type)
VALUES
    (1, 'New York', 'Company Owned', 'Dealer'),
    (2, 'Los Angeles', 'Franchise', 'Private');
INSERT INTO Sales (sale_id, vehicle_id, dealership_id, sale_date, quantity_sold, total_amount)
VALUES
    (1, 1, 1, '2024-10-14', 2, 56000.00),
    (2, 2, 2, '2024-10-15', 1, 22000.00);
INSERT INTO Inventory (vehicle_id, stock_level, last_updated)
VALUES
    (1, 8, '2024-10-14'), -- Updated after sale
    (2, 14, '2024-10-14'); -- Updated after sale
INSERT INTO Vehicles (vehicle_id, make, model, year, fuel_type, transmission, engine, color, seating_capacity, drivetrain, max_power, max_torque, price, stock_level)
VALUES
    (3, 'Ford', 'Mustang', 2019, 'Petrol', 'Automatic', 'V8', 'Red', 4, 'RWD', '450 HP', '550 Nm', 55000.00, 5),
    (4, 'BMW', 'X5', 2022, 'Petrol', 'Automatic', 'I6', 'Blue', 7, 'AWD', '335 HP', '450 Nm', 75000.00, 8),
    (5, 'Mercedes', 'C-Class', 2021, 'Diesel', 'Automatic', 'I4', 'Silver', 5, 'RWD', '255 HP', '400 Nm', 45000.00, 12),
    (6, 'Tesla', 'Model 3', 2023, 'Electric', 'Automatic', 'Electric', 'White', 5, 'AWD', '283 HP', '450 Nm', 45000.00, 20);
INSERT INTO Dealerships (dealership_id, location, owner_type, seller_type)
VALUES
    (3, 'Chicago', 'Franchise', 'Dealer'),
    (4, 'Houston', 'Company Owned', 'Dealer');
INSERT INTO Sales (sale_id, vehicle_id, dealership_id, sale_date, quantity_sold, total_amount)
VALUES
    (3, 3, 1, '2024-10-12', 1, 55000.00),
    (4, 4, 2, '2024-10-13', 2, 150000.00),
    (5, 5, 3, '2024-10-14', 1, 45000.00),
    (6, 6, 4, '2024-10-14', 3, 135000.00);
INSERT INTO Inventory (vehicle_id, stock_level, last_updated)
VALUES
    (3, 4, '2024-10-14'),
    (4, 6, '2024-10-14'),
    (5, 11, '2024-10-14'),
    (6, 17, '2024-10-14');
INSERT INTO Vehicles (vehicle_id, make, model, year, fuel_type, transmission, engine, color, seating_capacity, drivetrain, max_power, max_torque, price, stock_level, fuel_efficiency)
VALUES
    (7, 'Honda', 'Civic', 2021, 'Petrol', 'Manual', 'I4', 'Black', 5, 'FWD', '158 HP', '138 Nm', 22000.00, 15, 33.0),
    (8, 'Toyota', 'Camry', 2022, 'Hybrid', 'Automatic', 'I4', 'Gray', 5, 'FWD', '208 HP', '149 Nm', 25000.00, 10, 52.0),
    (9, 'Nissan', 'Altima', 2023, 'Petrol', 'Automatic', 'I4', 'White', 5, 'AWD', '182 HP', '178 Nm', 24000.00, 8, 28.0),
    (10, 'Chevrolet', 'Malibu', 2021, 'Petrol', 'Automatic', 'I4', 'Red', 5, 'FWD', '160 HP', '184 Nm', 23000.00, 12, 29.0);
INSERT INTO Dealerships (dealership_id, location, owner_type, seller_type)
VALUES
    (5, 'Philadelphia', 'Franchise', 'Dealer'),
    (6, 'Phoenix', 'Company Owned', 'Dealer');
INSERT INTO Sales (sale_id, vehicle_id, dealership_id, sale_date, quantity_sold, total_amount)
VALUES
    (7, 7, 5, '2024-10-12', 2, 44000.00),
    (8, 8, 6, '2024-10-13', 1, 25000.00),
    (9, 9, 5, '2024-10-14', 1, 24000.00),
    (10, 10, 6, '2024-10-15', 1, 23000.00);


-- Query for Low Inventory Warning
SELECT v.make, v.model, i.stock_level
FROM Inventory i
JOIN Vehicles v ON i.vehicle_id = v.vehicle_id
WHERE i.stock_level < 5;

--Query for Total Sales by Dealership:
SELECT d.location, SUM(s.total_amount) AS total_sales
FROM Sales s
JOIN Dealerships d ON s.dealership_id = d.dealership_id
GROUP BY d.location;

-- Query for Best-Selling Vehicle
SELECT TOP 1 v.make, v.model, SUM(s.quantity_sold) AS total_sold
FROM Sales s
JOIN Vehicles v ON s.vehicle_id = v.vehicle_id
GROUP BY v.make, v.model
ORDER BY total_sold DESC;

-- Query for Sales by Month:
SELECT MONTH(s.sale_date) AS sale_month, SUM(s.total_amount) AS total_sales
FROM Sales s
GROUP BY MONTH(s.sale_date);

-- Query for Average Sale Price by Vehicle Model:
SELECT v.make, v.model, AVG(s.total_amount) AS avg_sale_price
FROM Sales s
JOIN Vehicles v ON s.vehicle_id = v.vehicle_id
GROUP BY v.make, v.model;

--Query for Vehicles Sold by Each Dealership:
SELECT d.location, v.make, v.model, SUM(s.quantity_sold) AS total_sold
FROM Sales s
JOIN Dealerships d ON s.dealership_id = d.dealership_id
JOIN Vehicles v ON s.vehicle_id = v.vehicle_id
GROUP BY d.location, v.make, v.model
ORDER BY d.location, total_sold DESC;

-- Inventory and Sales Performance Analysis

WITH InventorySummary AS (
    SELECT
        v.vehicle_id,
        v.make,
        v.model,
        d.location,
        i.stock_level,
        v.fuel_efficiency
    FROM Vehicles v
    JOIN Inventory i ON v.vehicle_id = i.vehicle_id
    JOIN Dealerships d ON i.vehicle_id = d.dealership_id
),
SalesSummary AS (
    SELECT
        s.vehicle_id,
        SUM(s.quantity_sold) AS total_units_sold,
        SUM(s.total_amount) AS total_sales_amount
    FROM Sales s
    GROUP BY s.vehicle_id
)
SELECT 
    isum.make,
    isum.model,
    isum.location,
    isum.stock_level,
    COALESCE(ss.total_units_sold, 0) AS total_units_sold,
    COALESCE(ss.total_sales_amount, 0) AS total_sales_amount,
    isum.fuel_efficiency
FROM InventorySummary isum
LEFT JOIN SalesSummary ss ON isum.vehicle_id = ss.vehicle_id
ORDER BY isum.location, isum.make, isum.model;


