# DEPI_GRAD_PROJ

# Week 1
# Retail Inventory Management Database Documentation
## Database Schema
**The Retail Inventory Management database consists of the following tables:**

#### *Suppliers*
- supplier_id: Unique identifier for the supplier
- supplier_name: Name of the supplier
- contact_info: Contact information for the supplier

```sql
CREATE TABLE [dbo].[Suppliers] (
    [supplier_id] INT PRIMARY KEY,
    [supplier_name] VARCHAR(255) NOT NULL,
    [contact_info] VARCHAR(255) NOT NULL
) ON [PRIMARY];
```

#### *Products*

- product_id: Unique identifier for the product
- product_name: Name of the product
- category: Category the product belongs to
- supplier_id: Foreign key reference to the Suppliers table
- price: Price of the product

```sql
CREATE TABLE [dbo].[Products] (
    [product_id] INT PRIMARY KEY,
    [product_name] VARCHAR(255) NOT NULL,
    [category] VARCHAR(100),
    [supplier_id] INT,
    [price] DECIMAL(10, 2),
    FOREIGN KEY (supplier_id) REFERENCES dbo.Suppliers(supplier_id)
) ON [PRIMARY];
```

#### *Inventory*

- inventory_id: Unique identifier for the inventory record
- product_id: Foreign key reference to the Products table
- warehouse_location: Location of the product in the warehouse
- quantity_in_stock: Current quantity of the product in stock

```sql
CREATE TABLE [dbo].[Inventory] (
    [inventory_id] INT PRIMARY KEY,
    [product_id] INT,
    [warehouse_location] VARCHAR(255),
    [quantity_in_stock] INT,
    FOREIGN KEY (product_id) REFERENCES dbo.Products(product_id)
) ON [PRIMARY];
```
#### *Sales*

- sale_id: Unique identifier for the sale record
- product_id: Foreign key reference to the Products table
- quantity_sold: Quantity of the product sold
- sale_date: Date of the sale
- sale_price: Price at which the product was sold

```sql
CREATE TABLE [dbo].[Sales] (
    [sale_id] INT PRIMARY KEY,
    [product_id] INT,
    [quantity_sold] INT,
    [sale_date] DATE,
    [sale_price] DECIMAL(10, 2),
    FOREIGN KEY (product_id) REFERENCES dbo.Products(product_id)
) ON [PRIMARY];
```
</br>

The database schema establishes relationships between the tables using foreign key constraints. For example, the Products table is linked to the Suppliers table through the supplier_id column, and the Inventory and Sales tables are linked to the Products table through the product_id column.
</br>

## SQL Queries
**The SQL script provided includes the following queries:**

*1. Products Running Low on Stock:*
- This query selects the product name, warehouse location, and quantity in stock for products where the quantity in stock is less than 10.

```sql
SELECT p.product_name, i.warehouse_location, i.quantity_in_stock
FROM Products p
JOIN Inventory i ON p.product_id = i.product_id
WHERE i.quantity_in_stock < 10;
```

*2. Total Sales Revenue for Each Product:*
- This query calculates the total sales revenue for each product by multiplying the quantity sold and the sale price, then grouping the results by the product name.

```sql
SELECT p.product_name, SUM(s.quantity_sold * s.sale_price) AS total_sales_revenue
FROM Products p
JOIN Sales s ON p.product_id = s.product_id
GROUP BY p.product_name
ORDER BY total_sales_revenue DESC;
```

*3. Daily Sales Summary:*
- This query calculates the total daily sales by summing the sale price multiplied by the quantity sold, grouped by the sale date.

```sql
SELECT s.sale_date, SUM(s.sale_price * s.quantity_sold) AS daily_sales
FROM Sales s
GROUP BY s.sale_date
ORDER BY s.sale_date;
```

*4. Supplier-wise Product Distribution:*
- This query counts the number of products for each supplier by joining the Suppliers and Products tables and grouping the results by the supplier name.

```sql
SELECT su.supplier_name, COUNT(p.product_id) AS number_of_products
FROM Suppliers su
JOIN Products p ON su.supplier_id = p.supplier_id
GROUP BY su.supplier_name;
```

*5. Products with Highest Sales Volume:*
- This query finds the products with the highest total quantity sold by joining the Products and Sales tables and grouping the results by the product name.

```sql
SELECT p.product_name, SUM(s.quantity_sold) AS total_quantity_sold
FROM Products p
JOIN Sales s ON p.product_id = s.product_id
GROUP BY p.product_name
ORDER BY total_quantity_sold DESC;
```

*6. Sales by Warehouse Location:*
- This query calculates the total sales for each warehouse location by joining the Inventory and Sales tables and grouping the results by the warehouse location.

```sql
SELECT i.warehouse_location, SUM(s.quantity_sold * s.sale_price) AS warehouse_sales
FROM Inventory i
JOIN Sales s ON i.product_id = s.product_id
GROUP BY i.warehouse_location
ORDER BY warehouse_sales DESC;
```

*7. Average Sales Price for Each Product:*
- This query calculates the average sales price for each product by joining the Products and Sales tables and grouping the results by the product name.

```sql
SELECT p.product_name, AVG(s.sale_price) AS avg_sale_price
FROM Products p
JOIN Sales s ON p.product_id = s.product_id
GROUP BY p.product_name
ORDER BY avg_sale_price DESC;
```

*8. Inventory Status by Supplier:*
- This query calculates the total stock for each supplier by joining the Suppliers, Products, and Inventory tables and grouping the results by the supplier name.

```sql
SELECT su.supplier_name, SUM(i.quantity_in_stock) AS total_stock
FROM Suppliers su
JOIN Products p ON su.supplier_id = p.supplier_id
JOIN Inventory i ON p.product_id = i.product_id
GROUP BY su.supplier_name
ORDER BY total_stock DESC;
```

*9. Products Never Sold:*
- This query finds the products that have never been sold by performing a left join between the Products and Sales tables and selecting products where the sale ID is null.

```sql
SELECT p.product_name
FROM Products p
LEFT JOIN Sales s ON p.product_id = s.product_id
WHERE s.sale_id IS NULL;
```

*10. Most Popular Categories by Sales Revenue:*
- This query calculates the total sales revenue for each product category by joining the Products and Sales tables and grouping the results by the product category.

```sql
SELECT p.category, SUM(s.quantity_sold * s.sale_price) AS total_category_sales
FROM Products p
JOIN Sales s ON p.product_id = s.product_id
GROUP BY p.category
ORDER BY total_category_sales DESC;
```
</br>


These queries provide a range of insights into the retail inventory management system, including inventory levels, sales performance, supplier relationships, and product popularity.
</br>

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

The data pipeline script (`DataPipeline.py`) handles the Extract, Transform, and Load (ETL) process for our data warehouse. Here's an overview of its main components:

### 1. Database Connection
```python
def create_connection():
    connection_string = (
        "mssql+pyodbc://ATRXLO/RetailInventoryDWHStar?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
    )
    engine = create_engine(connection_string)
    return engine
```
This function establishes a connection to the SQL Server database using SQLAlchemy.

### 2. Extract Function
```python
def extract(file_path):
    try:
        df = pd.read_csv(file_path)
        print(f"Extracted {len(df)} records from {file_path}.")
        return df
    except Exception as e:
        print(f"Error during extraction: {e}")
        return pd.DataFrame()
```
This function reads data from a CSV file and returns it as a pandas DataFrame.

### 3. Transform Function
```python
def transform(df):
    # Handle missing values
    if df.isnull().values.any():
        print("Data contains missing values. Filling with default values or dropping rows.")
        df.fillna({
            'product_id': 0,
            'product_name': 'Unknown',
            # ... [other columns] ...
        }, inplace=True)

    # Validate product_id (must be unique)
    if 'product_id' in df.columns and not df['product_id'].is_unique:
        print("Warning: Duplicate product_ids found.")
        df.drop_duplicates(subset=['product_id'], inplace=True)

    # Validate unit_price
    if 'unit_price' in df.columns:
        df = df[df['unit_price'] >= 0]  # Drop negative prices

    print(f"Transformed data contains {len(df)} records after validation.")
    return df
```
This function cleans and validates the data, handling missing values, duplicate product IDs, and negative prices.

### 4. Load Function
```python
def load(df, table_name):
    engine = create_connection()
    try:
        df.to_sql(table_name, con=engine, if_exists='append', index=False)
        print(f"Loaded {len(df)} records into {table_name}.")
    except Exception as e:
        print(f"Error during loading to {table_name}: {e}")
```
This function loads the transformed data into the specified SQL Server table.

### 5. Main ETL Function
```python
def run_etl(csv_file_path, table_name):
    extracted_data = extract(csv_file_path)
    if not extracted_data.empty:
        transformed_data = transform(extracted_data)
        load(transformed_data, table_name)
```
This function orchestrates the entire ETL process for a given CSV file and table.

## Database Configuration (config.py)

The `config.py` file handles the database connection configuration:

```python
def get_connection():
    try:
        drivers = [driver for driver in pyodbc.drivers()]
        print("Available ODBC drivers:", drivers)

        driver = next((driver for driver in drivers if 'SQL Server' in driver), None)
        if not driver:
            raise ValueError("No SQL Server ODBC driver found")

        connection_string = (
            f"mssql+pyodbc://ATRXLO/RetailInventoryDWHStar"
            f"?driver={driver.replace(' ', '+')}"
            "&trusted_connection=yes"
        )

        print(f"Attempting to connect with: {connection_string}")

        engine = create_engine(connection_string)
        return engine.connect()
    except SQLAlchemyError as e:
        print(f"SQLAlchemy error occurred: {e}")
        return None
    except pyodbc.Error as e:
        print(f"PYODBC error occurred: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
```

This function:
1. Lists available ODBC drivers
2. Selects an appropriate SQL Server driver
3. Constructs a connection string
4. Attempts to create a database connection
5. Handles various types of connection errors

## ETL Automation (automated-etl-script.py)

To ensure regular updates of the data warehouse, an automation script has been implemented. This script schedules and runs the ETL jobs on a daily basis.

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

