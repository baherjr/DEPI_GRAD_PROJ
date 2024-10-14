-- Create the DimVehicle table
CREATE TABLE DimVehicle (
    VehicleKey INT PRIMARY KEY,
    VehicleID VARCHAR(100) NOT NULL,
    Make VARCHAR(50) NOT NULL,
    Model VARCHAR(50) NOT NULL,
    Year INT NOT NULL,
    FuelType VARCHAR(50) NOT NULL,
    Transmission VARCHAR(50) NOT NULL,
    Engine VARCHAR(50) NOT NULL,
    NumberOfDoors INT NOT NULL,
    Drivetrain VARCHAR(50) NOT NULL,
    MaxPower INT NOT NULL,
    Price DECIMAL(10, 2) NOT NULL
);

-- Create the DimDealership table
CREATE TABLE DimDealership (
    DealershipKey INT PRIMARY KEY,
    DealershipID VARCHAR(20) NOT NULL,
    Location VARCHAR(100) NOT NULL,
    OwnerType VARCHAR(50) NOT NULL,
    SellerType VARCHAR(50) NOT NULL
);

-- Create the DimDate table
CREATE TABLE DimDate (
    DateKey INT PRIMARY KEY,
    Date DATE NOT NULL,
    Year INT NOT NULL,
    Month INT NOT NULL,
    MonthName VARCHAR(10) NOT NULL,
    Quarter INT NOT NULL
);

-- Create the FactSales table
CREATE TABLE FactSales (
    SaleID INT PRIMARY KEY,
    DateKey INT NOT NULL,
    VehicleKey INT NOT NULL,
    DealershipKey INT NOT NULL,
    QuantitySold INT NOT NULL,
    TotalAmount DECIMAL(12, 2) NOT NULL,
    FOREIGN KEY (DateKey) REFERENCES DimDate(DateKey),
    FOREIGN KEY (VehicleKey) REFERENCES DimVehicle(VehicleKey),
    FOREIGN KEY (DealershipKey) REFERENCES DimDealership(DealershipKey)
);

-- Create the FactInventory table
CREATE TABLE FactInventory (
    InventoryID INT PRIMARY KEY,
    DateKey INT NOT NULL,
    VehicleKey INT NOT NULL,
    StockLevel INT NOT NULL,
    FOREIGN KEY (DateKey) REFERENCES DimDate(DateKey),
    FOREIGN KEY (VehicleKey) REFERENCES DimVehicle(VehicleKey)
);

-- Create indexes for better query performance
CREATE INDEX idx_dimvehicle_vehicleid ON DimVehicle(VehicleID);
CREATE INDEX idx_dimdealership_dealershipid ON DimDealership(DealershipID);
CREATE INDEX idx_dimdate_date ON DimDate(Date);
CREATE INDEX idx_factsales_datekey ON FactSales(DateKey);
CREATE INDEX idx_factsales_vehiclekey ON FactSales(VehicleKey);
CREATE INDEX idx_factsales_dealershipkey ON FactSales(DealershipKey);
CREATE INDEX idx_factinventory_datekey ON FactInventory(DateKey);
CREATE INDEX idx_factinventory_vehiclekey ON FactInventory(VehicleKey);