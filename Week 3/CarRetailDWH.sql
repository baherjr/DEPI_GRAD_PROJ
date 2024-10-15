-- Create DimVehicle Table
IF OBJECT_ID(N'dbo.DimVehicle', N'U') IS NULL
BEGIN
    CREATE TABLE DimVehicle (
        VehicleKey INT PRIMARY KEY,
        VehicleID NVARCHAR(50),
        Make NVARCHAR(50),
        Model NVARCHAR(50),
        Year INT,
        FuelType NVARCHAR(50),
        Transmission NVARCHAR(50),
        Engine NVARCHAR(50),
        NumberOfDoors INT,
        Drivetrain NVARCHAR(50),
        MaxPower DECIMAL(10, 2),
        Price DECIMAL(10, 2)
    );
END

-- Create DimDealership Table
IF OBJECT_ID(N'dbo.DimDealership', N'U') IS NULL
BEGIN
    CREATE TABLE DimDealership (
        DealershipKey INT PRIMARY KEY,
        DealershipID NVARCHAR(50),
        Location NVARCHAR(100),
		OwnerType NVARCHAR(100),
		SellerType NVARCHAR(100)
    );
END

-- Create DimDate Table
IF OBJECT_ID(N'dbo.DimDate', N'U') IS NULL
BEGIN
    CREATE TABLE DimDate (
        DateKey INT PRIMARY KEY,
        Date DATE,
        Year INT,
		Month INT,
        MonthName NVARCHAR(50),
        Quarter INT
    );
END

-- Create FactSales Table
IF OBJECT_ID(N'dbo.FactSales', N'U') IS NULL
BEGIN
 CREATE TABLE FactSales (
        SaleID INT PRIMARY KEY,
        DateKey INT,
        VehicleKey INT,
        DealershipKey INT,
        QuantitySold INT,
        TotalAmount DECIMAL(10, 2),
        FOREIGN KEY (DateKey) REFERENCES DimDate(DateKey),  -- Reference to DimDate
        FOREIGN KEY (VehicleKey) REFERENCES DimVehicle(VehicleKey),  -- Reference to DimVehicle
        FOREIGN KEY (DealershipKey) REFERENCES DimDealership(DealershipKey)  -- Reference to DimDealership
    );
END

-- Create FactInventory Table
IF OBJECT_ID(N'dbo.FactInventory', N'U') IS NULL
BEGIN
    CREATE TABLE FactInventory (
        InventoryID INT,
        DateKey INT,
        VehicleKey INT,
        StockLevel INT,
        FOREIGN KEY (VehicleKey) REFERENCES DimVehicle(VehicleKey),
        FOREIGN KEY (DateKey) REFERENCES DimDate(DateKey),
		PRIMARY KEY (InventoryID, DateKey)
    );
END