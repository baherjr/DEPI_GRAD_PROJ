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

## Data Warehouse Schema (Star Schema)

### Dimension Tables

1. **DIM_PRODUCT**
   ```sql
   CREATE TABLE DIM_PRODUCT (
       product_id INT PRIMARY KEY,
       product_name VARCHAR(100),
       category VARCHAR(50),
       unit_price DECIMAL(10, 2),
       supplier_id INT
   );
   ```

2. **DIM_STORE**
   ```sql
   CREATE TABLE DIM_STORE (
       store_id INT PRIMARY KEY,
       store_name VARCHAR(100),
       city VARCHAR(50),
       state VARCHAR(50),
       country VARCHAR(50)
   );
   ```

3. **DIM_DATE**
   ```sql
   CREATE TABLE DIM_DATE (
       date_id INT PRIMARY KEY,
       full_date DATE,
       year INT,
       quarter INT,
       month INT,
       day INT,
       day_of_week VARCHAR(10)
   );
   ```

4. **DIM_CUSTOMER**
   ```sql
   CREATE TABLE DIM_CUSTOMER (
       customer_id INT PRIMARY KEY,
       customer_name VARCHAR(100),
       email VARCHAR(100),
       city VARCHAR(50),
       state VARCHAR(50),
       country VARCHAR(50)
   );
   ```

### Fact Table

**FACT_SALES**
```sql
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
```

### Indexes
To improve query performance, the following indexes have been created:

```sql
CREATE INDEX idx_product ON FACT_SALES(product_id);
CREATE INDEX idx_store ON FACT_SALES(store_id);
CREATE INDEX idx_date ON FACT_SALES(date_id);
CREATE INDEX idx_customer ON FACT_SALES(customer_id);
```

## Data Pipeline (DataPipeline.py)

The `DataPipeline.py` script implements an Extract, Transform, and Load (ETL) process for our data warehouse. Here's a detailed overview of its main components:

### 1. Database Connection
```python
def create_connection():
    connection_string = (
        "mssql+pyodbc://ATRXLO/RetailInventoryDWHStar?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
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
This function establishes a connection to the SQL Server database using SQLAlchemy. It now returns a connection object and includes error handling with logging.

### 2. Extract Function
```python
def extract(file_path):
    try:
        df = pd.read_csv(file_path)
        logging.info(f"Extracted {len(df)} records from {file_path}.")
        return df
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
        return pd.DataFrame()
    except Exception as e:
        logging.error(f"Error during extraction: {e}")
        return pd.DataFrame()
```
This function reads data from a CSV file and returns it as a pandas DataFrame. It now includes specific error handling for FileNotFoundError and improved logging.

### 3. Transform Function
```python
def transform(df, table_name):
    # General cleaning: Handle missing values in all datasets
    df.fillna({
        'store_id': 0,
        'store_name': 'Unknown',
        'city': 'Unknown',
        # ... (other columns)
    }, inplace=True)

    # Handle table-specific transformations
    if table_name == 'DIM_PRODUCT':
        # Product-specific transformations
    elif table_name == 'DIM_STORE':
        # Store-specific transformations

    # Generic data validation
    if 'unit_price' in df.columns:
        df = df[df['unit_price'] >= 0]
    if 'quantity' in df.columns:
        df = df[df['quantity'] >= 0]

    return df
```
This function cleans and validates the data, handling missing values, applying table-specific transformations, and performing generic data validation. It now includes more comprehensive missing value handling and table-specific logic.

### 4. Load Function
```python
def load(df, table_name):
    conn = create_connection()
    if conn is None:
        logging.error("No connection available to load data.")
        return

    try:
        df.to_sql(table_name, con=conn, if_exists='append', index=False)
        logging.info(f"Loaded {len(df)} records into {table_name}.")
    except Exception as e:
        logging.error(f"Error during loading to {table_name}: {e}")
    finally:
        conn.close()
```
This function loads the transformed data into the specified SQL Server table. It now includes proper connection management and error handling.

## 5. Verify Load Function
```python
def verify_load(table_name):
    conn = create_connection()
    if conn is None:
        logging.error("No connection available to verify load.")
        return

    query = f"SELECT COUNT(*) FROM {table_name}"
    count = pd.read_sql(query, conn)
    print(f"{table_name} record count: {count.iloc[0, 0]}")
    conn.close()
```
This new function verifies the number of records in each table after the load process, providing a simple data quality check.

### 6. Main ETL Function
```python
def run_etl(csv_file, table_name):
    extracted_data = extract(csv_file)
    logging.info(f"Extracted {len(extracted_data)} records from {csv_file}")

    transformed_data = transform(extracted_data, table_name)

    load(transformed_data, table_name)

    verify_load(table_name)
```
This function orchestrates the entire ETL process for a given CSV file and table, including the new verification step.

### Main Execution
The script ends with a main execution block that runs the ETL process for multiple tables:
```python
if __name__ == "__main__":
    run_etl('dim-product-csv.csv', 'DIM_PRODUCT')
    run_etl('dim-store-csv.csv', 'DIM_STORE')
    run_etl('dim-date-csv.csv', 'DIM_DATE')
    run_etl('dim-customer-csv.csv', 'DIM_CUSTOMER')
    run_etl('fact-sales-csv.csv', 'FACT_SALES')
```

This structure allows for easy processing of multiple tables in sequence.




### Script Overview

```python
import os
import schedule
import time
from DataPipeline import run_etl

def run_all_etl_jobs():
    print("Starting ETL jobs...")
    
    etl_jobs = [
        ('dim-product-csv.csv', 'DIM_PRODUCT'),
        ('dim-store-csv.csv', 'DIM_STORE'),
        ('dim-date-csv.csv', 'DIM_DATE'),
        ('dim-customer-csv.csv', 'DIM_CUSTOMER'),
        ('fact-sales-csv.csv', 'FACT_SALES')
    ]
    
    for csv_file, table_name in etl_jobs:
        csv_path = os.path.join('data', csv_file)
        if os.path.exists(csv_path):
            print(f"Processing {csv_file}...")
            run_etl(csv_path, table_name)
        else:
            print(f"Warning: {csv_file} not found in the data directory.")
    
    print("All ETL jobs completed.")

# Schedule the job to run daily at 1:00 AM
schedule.every().day.at("01:00").do(run_all_etl_jobs)

if __name__ == "__main__":
    print("ETL automation script started. Press Ctrl+C to exit.")
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Wait for 60 seconds before checking schedule again
    except KeyboardInterrupt:
        print("ETL automation script stopped.")
```

### Key Features

1. **Job Definition**: The script defines a list of ETL jobs, each consisting of a CSV file name and its corresponding table name in the data warehouse.

2. **File Checking**: Before running each ETL job, the script checks if the CSV file exists in the specified 'data' directory.

3. **Scheduled Execution**: The ETL process is scheduled to run daily at 1:00 AM using the `schedule` library.

4. **Continuous Operation**: The script runs continuously, checking every 60 seconds if there are any scheduled jobs to run.

5. **Graceful Termination**: The script can be stopped safely using a keyboard interrupt (Ctrl+C).

### Usage

To use this automation script:

1. Ensure all required CSV files are placed in a 'data' directory.
2. Run the script using Python: `python automated-etl-script.py`
3. The script will continue running until manually stopped.

### Considerations

- **Server Deployment**: For production use, consider deploying this script on a server that runs continuously.
- **Error Handling**: Implement more robust error handling and logging for production environments.
- **Monitoring**: Set up alerts to notify administrators of any failures in the ETL process.
- **Data Freshness**: Adjust the schedule as needed based on how frequently your source data is updated.

