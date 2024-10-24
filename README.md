# DEPI_GRAD_PROJ

# Week 1
# Retail Inventory Management Database Documentation

## Database Schema

**The Retail Inventory Management database consists of the following tables:**

### Vehicles
- **vehicle_id**: Unique identifier for each vehicle
- **make**: Manufacturer of the vehicle
- **model**: Model name of the vehicle
- **year**: Manufacturing year of the vehicle
- **fuel_type**: Type of fuel used (e.g., Petrol, Diesel, Electric)
- **transmission**: Transmission type (e.g., Automatic, Manual)
- **engine**: Engine type or configuration
- **color**: Color of the vehicle
- **seating_capacity**: Number of passengers the vehicle can accommodate
- **drivetrain**: Drivetrain configuration (e.g., FWD, RWD, AWD)
- **max_power**: Maximum power output of the vehicle
- **max_torque**: Maximum torque of the vehicle
- **price**: Retail price of the vehicle
- **stock_level**: Current stock level of the vehicle
- **fuel_efficiency**: Fuel efficiency measured in miles per gallon (MPG) or equivalent

```sql
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
```

### Dealerships
- **dealership_id**: Unique identifier for each dealership
- **location**: Physical location of the dealership
- **owner_type**: Type of ownership (e.g., Company Owned, Franchise)
- **seller_type**: Type of seller (e.g., Dealer, Private)

```sql
CREATE TABLE Dealerships (
    dealership_id INT PRIMARY KEY,
    location VARCHAR(100),
    owner_type VARCHAR(50),
    seller_type VARCHAR(50)
);
```

### Sales
- **sale_id**: Unique identifier for each sale record
- **vehicle_id**: Foreign key reference to the Vehicles table
- **dealership_id**: Foreign key reference to the Dealerships table
- **sale_date**: Date when the sale occurred
- **quantity_sold**: Quantity of vehicles sold
- **total_amount**: Total sale amount for the transaction

```sql
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
```

### Inventory
- **vehicle_id**: Foreign key reference to the Vehicles table
- **stock_level**: Current stock level of the vehicle
- **last_updated**: Date when the stock level was last updated

```sql
CREATE TABLE Inventory (
    vehicle_id INT,
    stock_level INT,
    last_updated DATE,
    FOREIGN KEY (vehicle_id) REFERENCES Vehicles(vehicle_id)
);
```

The database schema establishes relationships between the tables using foreign key constraints. For example, the **Sales** table is linked to the **Vehicles** table through the `vehicle_id` column, and the **Inventory** table is linked to the **Vehicles** table via the same column.

## SQL Queries

**The SQL script provided includes the following queries:**

1. **Low Inventory Warning**: This query selects the vehicle make, model, and stock level for vehicles where the stock level is less than 5.

```sql
SELECT v.make, v.model, i.stock_level
FROM Inventory i
JOIN Vehicles v ON i.vehicle_id = v.vehicle_id
WHERE i.stock_level < 5;
```

2. **Total Sales by Dealership**: This query calculates the total sales for each dealership by summing the total amount of sales.

```sql
SELECT d.location, SUM(s.total_amount) AS total_sales
FROM Sales s
JOIN Dealerships d ON s.dealership_id = d.dealership_id
GROUP BY d.location;
```

3. **Best-Selling Vehicle**: This query finds the best-selling vehicle by summing the quantity sold and ordering the results.

```sql
SELECT v.make, v.model, SUM(s.quantity_sold) AS total_sold
FROM Sales s
JOIN Vehicles v ON s.vehicle_id = v.vehicle_id
GROUP BY v.make, v.model
ORDER BY total_sold DESC
LIMIT 1;
```

4. **Sales by Month**: This query summarizes total sales by month.

```sql
SELECT MONTH(s.sale_date) AS sale_month, SUM(s.total_amount) AS total_sales
FROM Sales s
GROUP BY MONTH(s.sale_date);
```

5. **Average Sale Price by Vehicle Model**: This query calculates the average sale price for each vehicle model.

```sql
SELECT v.make, v.model, AVG(s.total_amount) AS avg_sale_price
FROM Sales s
JOIN Vehicles v ON s.vehicle_id = v.vehicle_id
GROUP BY v.make, v.model;
```

6. **Vehicles Sold by Each Dealership**: This query calculates the total quantity sold for each vehicle by dealership.

```sql
SELECT d.location, v.make, v.model, SUM(s.quantity_sold) AS total_sold
FROM Sales s
JOIN Dealerships d ON s.dealership_id = d.dealership_id
JOIN Vehicles v ON s.vehicle_id = v.vehicle_id
GROUP BY d.location, v.make, v.model
ORDER BY d.location, total_sold DESC;
```

7. **Inventory and Sales Performance Analysis**: This query summarizes inventory and sales performance across all vehicles and dealerships.

```sql
WITH InventorySummary AS (
    SELECT v.vehicle_id, v.make, v.model, d.location, i.stock_level, v.fuel_efficiency
    FROM Vehicles v
    JOIN Inventory i ON v.vehicle_id = i.vehicle_id
    JOIN Dealerships d ON i.vehicle_id = d.dealership_id
),
SalesSummary AS (
    SELECT s.vehicle_id, SUM(s.quantity_sold) AS total_units_sold, SUM(s.total_amount) AS total_sales_amount
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
```

These queries provide a range of insights into the retail inventory management system, including inventory levels, sales performance, dealership statistics, and vehicle popularity.


# Week 2: Data Warehousing and Python Integration

## Overview
This week focuses on implementing a data warehouse to consolidate inventory and sales data, and integrating Python scripts for data extraction, cleaning, and preparation.

## Tasks

### 1. Data Warehouse Implementation
- **Objective**: Consolidate inventory and sales data for reporting and analysis.
- **Tool**: Microsoft SQL Data Warehouse
- **Steps**:
  1. Design the data warehouse schema (Star Schema implemented)
  2. Set up the Microsoft SQL Data Warehouse environment
  3. Configure data storage and partitioning
  4. Implement security measures and access controls

### 2. Data Loading (ETL Process)
- **Objective**: Integrate data into the warehouse using ETL processes.
- **Steps**:
  1. Extract data from source systems (e.g., inventory management, point of sale)
  2. Transform data to fit the data warehouse schema
  3. Load data into the appropriate tables in the data warehouse
  4. Set up scheduling for regular data updates

### 3. Python Scripting
- **Objective**: Extract data from SQL database, clean it, and prepare for analysis.
- **Tools**: Python (Pandas, SQLAlchemy)
- **Steps**:
  1. Set up Python environment with required libraries
  2. Write scripts to connect to the SQL database using SQLAlchemy
  3. Extract relevant data using SQL queries
  4. Use Pandas for data cleaning and transformation
  5. Prepare data for analysis (e.g., aggregations, feature engineering)

## Deliverables

1. **Data Warehouse Setup**
   - Fully configured Microsoft SQL Data Warehouse
   - Integrated inventory and sales data
   - Documentation on schema design and data flow

2. **Python Scripts**
   - Script for data extraction from SQL database
   - Script for data cleaning and preparation
   - Documentation on how to run the scripts and their functionalities

## Technical Specifications

- **Data Warehouse**: Microsoft SQL Data Warehouse
- **Programming Language**: Python 3.x
- **Python Libraries**: 
  - Pandas (for data manipulation)
  - SQLAlchemy (for database connectivity)
  - Any additional libraries used in the project

## Car Retail Data Warehouse Schema (Star Schema)



### Dimension Tables

1. **DimVehicle**
   ```sql
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
   ```

2. **DimDealership**
   ```sql
    CREATE TABLE DimDealership (
        DealershipKey INT PRIMARY KEY,
        DealershipID NVARCHAR(50),
        Location NVARCHAR(100),
		OwnerType NVARCHAR(100),
		SellerType NVARCHAR(100)
    );
   ```

3. **DimDate**
   ```sql
    CREATE TABLE DimDate (
        DateKey INT PRIMARY KEY,
        Date DATE,
        Year INT,
		Month INT,
        MonthName NVARCHAR(50),
        Quarter INT
    );
   ```

### Fact Tables

1. **FactSales**
   ```sql
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
   ```

2. **FactInventory**
   ```sql
    CREATE TABLE FactInventory (
        InventoryID INT,
        DateKey INT,
        VehicleKey INT,
        StockLevel INT,
        FOREIGN KEY (VehicleKey) REFERENCES DimVehicle(VehicleKey),
        FOREIGN KEY (DateKey) REFERENCES DimDate(DateKey),
		PRIMARY KEY (InventoryID, DateKey)
    );
   ```

### Indexes

To improve query performance, the following indexes have been created:

```sql
    CREATE INDEX IX_DimVehicle_VehicleID ON DimVehicle (VehicleID);
    CREATE INDEX IX_DimVehicle_Make ON DimVehicle (Make);
    CREATE INDEX IX_DimVehicle_Model ON DimVehicle (Model);
    CREATE INDEX IX_DimVehicle_Year ON DimVehicle (Year);
    CREATE INDEX IX_DimDealership_DealershipID ON DimDealership (DealershipID);
    CREATE INDEX IX_DimDealership_Location ON DimDealership (Location);
    CREATE INDEX IX_DimDate_Year ON DimDate (Year);
    CREATE INDEX IX_DimDate_Month ON DimDate (Month);
    CREATE INDEX IX_DimDate_Quarter ON DimDate (Quarter);
    CREATE INDEX IX_FactSales_DateKey ON FactSales (DateKey);
    CREATE INDEX IX_FactSales_VehicleKey ON FactSales (VehicleKey);
    CREATE INDEX IX_FactSales_DealershipKey ON FactSales (DealershipKey);
    CREATE INDEX IX_FactInventory_DateKey ON FactInventory (DateKey);
    CREATE INDEX IX_FactInventory_VehicleKey ON FactInventory (VehicleKey);
```

## Data Pipeline (DataPipeline.py)

The `DataPipeline.py` script implements an Extract, Transform, and Load (ETL) process for a vehicle sales data warehouse. Here's a detailed overview of its main components:

### 1. Imports and Configuration

```python
import pandas as pd
import pyodbc
import os
import logging
from sqlalchemy import create_engine, Table, MetaData, insert
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    'mssql': {
        'server': os.getenv('MSSQL_SERVER'),
        'database': os.getenv('MSSQL_DATABASE'),
    },
}

logging.basicConfig(level=logging.INFO)
```

This section imports necessary libraries, loads environment variables, and sets up logging and database configuration.

### 2. Database Connection

```python
def create_connection():
    connection_string = (
        f"mssql+pyodbc://{DB_CONFIG['mssql']['server']}/{DB_CONFIG['mssql']['database']}?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
    )
    try:
        engine = create_engine(connection_string)
        conn = engine.connect()
        logging.info("Connection successful")
        return conn
    except Exception as e:
        logging.error(f"Connection failed: {e}")
        return None
```

This function establishes a connection to the SQL Server database using SQLAlchemy. It returns a connection object and includes error handling with logging.

### 3. Extract Function

```python
def extract(file_path):
    try:
        df = pd.read_csv(file_path)
        logging.info(f"Extracted {len(df)} rows from {file_path}.")
        return df
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}. Please check the path.")
        return pd.DataFrame()
    except pd.errors.EmptyDataError:
        logging.error(f"No data: The file at {file_path} is empty.")
        return pd.DataFrame()
    except pd.errors.ParserError:
        logging.error(f"Parsing error: Could not parse the file at {file_path}.")
        return pd.DataFrame()
    except Exception as e:
        logging.error(f"Error extracting data from {file_path}: {e}")
        return pd.DataFrame()
```

This function reads data from a CSV file and returns it as a pandas DataFrame. It includes specific error handling for various scenarios and improved logging.

### 4. Transform Functions

The script includes several transform functions for different tables:

```python
def transform_dim_vehicle(df):
    # Transformation logic for DimVehicle table
    # ...

def transform_dim_dealership(df):
    # No transformations for DimDealership table
    return df

def transform_dim_date(df):
    # Transformation logic for DimDate table
    # ...

def transform_fact_sales(df):
    # Transformation logic for FactSales table
    # ...

def transform_fact_inventory(df):
    # Transformation logic for FactInventory table
    # ...
```

These functions clean and validate the data, handling missing values, applying table-specific transformations, and performing data type conversions.


### 5. Load Function

```python
def load(df, table_name, conn):
    if df.empty:
        logging.warning(f"No data to load for {table_name}.")
        return

    # Log columns present in the DataFrame
    logging.info(f"Columns in {table_name}: {df.columns.tolist()}")

    required_columns = {
        'DimVehicle': ['VehicleKey', 'VehicleID', 'Make', 'Model', 'Year', 'FuelType', 'Transmission',
                       'Engine', 'NumberOfDoors', 'Drivetrain', 'MaxPower', 'Price'],
        'DimDealership': ['DealershipKey', 'DealershipID', 'Location', 'OwnerType', 'SellerType'],
        'DimDate': ['DateKey', 'Date', 'Year', 'MonthName', 'Quarter'],
        'FactSales': ['SaleID', 'DateKey', 'VehicleKey', 'DealershipKey', 'QuantitySold', 'TotalAmount'],
        'FactInventory': ['InventoryID', 'DateKey', 'VehicleKey', 'StockLevel']
    }

    # Check for missing columns
    missing_columns = [col for col in required_columns[table_name] if col not in df.columns]
    if missing_columns:
        logging.error(f"Missing columns in {table_name}: {missing_columns}")
        return

    try:
        # Additional checks for FactSales and FactInventory
        # ...

        # Use the to_sql method for inserting data
        df.to_sql(table_name, conn, if_exists='append', index=False)
        logging.info(f"Loaded {len(df)} rows into {table_name}.")
        conn.commit()

    except Exception as e:
        logging.error(f"Error loading data into {table_name}: {e}")
```

This function loads the transformed data into the specified SQL Server table. It includes checks for required columns, foreign key constraints, and proper error handling.

### 6. Main ETL Function

```python
def run_etl(conn):
    try:
        # Extract data from CSV files
        dim_vehicle_df = extract('dim_vehicle.csv')
        dim_dealership_df = extract('dim_dealership.csv')
        dim_date_df = extract('dim_date.csv')
        fact_sales_df = extract('fact_sales.csv')
        fact_inventory_df = extract('fact_inventory.csv')

        # Log DataFrame columns
        # ...

        # Load data into SQL tables
        load(dim_vehicle_df, 'DimVehicle', conn)
        load(dim_dealership_df, 'DimDealership', conn)
        load(dim_date_df, 'DimDate', conn)
        load(fact_sales_df, 'FactSales', conn)
        load(fact_inventory_df, 'FactInventory', conn)

    except Exception as e:
        logging.error(f"ETL process failed: {e}")
    finally:
        if conn:
            conn.close()
            logging.info("Database connection closed.")
```

This function orchestrates all tables' ETL process, including extraction, transformation, and loading steps.

### Main Execution

The script ends with a main execution block that runs the ETL process:

```python
if __name__ == "__main__":
    run_etl(create_connection())
```

This structure allows for the processing of multiple tables in sequence, with proper error handling and logging throughout the ETL pipeline.
# Week 3

## Azure Analytics Tools Integration

### Tools Used

#### 1. Azure Data Studio
Azure Data Studio is an integrated development environment designed for data professionals. It provides a user-friendly interface for managing and working with databases.

**Key Features:**
- **Query Development and Testing:** Allows for efficient creation, execution, and testing of SQL queries.
- **Database Management Tasks:** Supports a variety of database management functions, including monitoring and administration.
- **Integrated Development Environment:** Offers a rich set of tools for data development and analysis.
- **Built-in Version Control Support:** Facilitates collaboration and versioning of SQL scripts and notebooks.

#### 2. Azure Synapse Analytics
Azure Synapse Analytics is an integrated analytics service that combines big data and data warehousing.

**Key Features:**
- **Parallel Processing Capabilities:** Enables high-performance data processing through parallel execution of queries.
- **Data Integration Workflows:** Streamlines the process of integrating and transforming data from multiple sources.
- **Large-scale Data Transformations:** Provides tools for executing complex data transformations across large datasets.
- **Performance Optimization Features:** Offers advanced capabilities for tuning and optimizing query performance.

### Integration Benefits

- **Seamless Workflow:** The integration of Azure Data Studio and Azure Synapse Analytics allows for a smooth transition between development and deployment, enhancing overall efficiency.
- **Enhanced Productivity:** Users can leverage the strengths of both tools to accelerate their data analytics processes, leading to quicker insights.
- **Comprehensive Analytics:** The combined capabilities provide a robust framework for handling diverse analytics requirements, from data ingestion to advanced querying and reporting.

## Price Prediction Model

### Objective
Develop a predictive model to forecast Manufacturer's Suggested Retail Price (MSRP) for vehicles, enabling data-driven pricing insights based on historical trends.

### Chosen Approach
Implementation of the SARIMA (Seasonal ARIMA) model, selected for its ability to capture both temporal patterns and seasonal variations in vehicle pricing.

### Data Foundation
Analysis based on a comprehensive vehicle dataset, incorporating temporal features (Year) and historical pricing data (Actual MSRP) for accurate predictions.



