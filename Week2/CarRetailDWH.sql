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


-- Create indexes for DimVehicle Table
IF OBJECT_ID(N'dbo.DimVehicleIndex', N'U') IS NULL
BEGIN
    CREATE INDEX IX_DimVehicle_VehicleID ON DimVehicle (VehicleID);
    CREATE INDEX IX_DimVehicle_Make ON DimVehicle (Make);
    CREATE INDEX IX_DimVehicle_Model ON DimVehicle (Model);
    CREATE INDEX IX_DimVehicle_Year ON DimVehicle (Year);
END

-- Create indexes for DimDealership Table
IF OBJECT_ID(N'dbo.DimDealershipIndex', N'U') IS NULL
BEGIN
    CREATE INDEX IX_DimDealership_DealershipID ON DimDealership (DealershipID);
    CREATE INDEX IX_DimDealership_Location ON DimDealership (Location);
END

-- Create indexes for DimDate Table
IF OBJECT_ID(N'dbo.DimDateIndex', N'U') IS NULL
BEGIN
    CREATE INDEX IX_DimDate_Year ON DimDate (Year);
    CREATE INDEX IX_DimDate_Month ON DimDate (Month);
    CREATE INDEX IX_DimDate_Quarter ON DimDate (Quarter);
END

-- Create indexes for FactSales Table
IF OBJECT_ID(N'dbo.FactSalesIndex', N'U') IS NULL
BEGIN
    CREATE INDEX IX_FactSales_DateKey ON FactSales (DateKey);
    CREATE INDEX IX_FactSales_VehicleKey ON FactSales (VehicleKey);
    CREATE INDEX IX_FactSales_DealershipKey ON FactSales (DealershipKey);
END

-- Create indexes for FactInventory Table
IF OBJECT_ID(N'dbo.FactInventoryIndex', N'U') IS NULL
BEGIN
    CREATE INDEX IX_FactInventory_DateKey ON FactInventory (DateKey);
    CREATE INDEX IX_FactInventory_VehicleKey ON FactInventory (VehicleKey);
END
