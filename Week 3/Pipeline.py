import pandas as pd
from sqlalchemy import create_engine
import logging
from urllib.parse import quote_plus  # For URL-encoding the password
from dotenv import load_dotenv
import os

# Configure logging
logging.basicConfig(level=logging.INFO)

# Load environment variables from .env file
load_dotenv()


# Define the connection to Azure SQL Database using SQLAlchemy
def create_connection():
    # Retrieve the password from the environment variable
    password = os.getenv('DB_PASSWORD')
    if not password:
        raise ValueError("Database password not found in environment variables")

    encoded_password = quote_plus(password)  # URL-encode the password to handle special characters

    connection_string = (
        f"mssql+pyodbc://bahror:{encoded_password}@demandforecastdb.database.windows.net:1433/DemandForecastDB"
        "?driver=ODBC+Driver+18+for+SQL+Server&Encrypt=yes&TrustServerCertificate=no&Connection+Timeout=30"
    )

    try:
        engine = create_engine(connection_string)
        conn = engine.connect()
        logging.info("Connection successful")
        return conn
    except Exception as e:
        logging.error(f"Connection failed: {e}")
        return None

# Extract function: Read data from CSV file
def extract(file_path):
    try:
        df = pd.read_csv(file_path)
        logging.info(f"Extracted {len(df)} records from {file_path}.")
        return df
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
        return pd.DataFrame()  # Return an empty DataFrame on error
    except Exception as e:
        logging.error(f"Error during extraction: {e}")
        return pd.DataFrame()


# Transform function: Clean and validate data
def transform(df, table_name):
    # General cleaning: Handle missing values in all datasets
    df.fillna({
        'store_id': 0,
        'store_name': 'Unknown',
        'city': 'Unknown',
        'state': 'Unknown',
        'country': 'Unknown',
        'date_id': 0,
        'full_date': pd.NaT,
        'year': 0,
        'quarter': 0,
        'month': 0,
        'day': 0,
        'day_of_week': 'Unknown',
        'customer_id': 0,
        'customer_name': 'Unknown',
        'email': 'Unknown',
        'quantity': 0,
        'total_amount': 0.00
    }, inplace=True)

    # Handle table-specific transformations
    if table_name == 'DIM_PRODUCT':
        if 'product_id' in df.columns:
            # Ensure supplier_id is included, fill with default value if missing
            if 'supplier_id' not in df.columns:
                df['supplier_id'] = 0  # Default supplier_id

            # No filtering on product_id here to avoid missing records
            logging.info("Transforming DIM_PRODUCT data.")
        else:
            logging.error("Column 'product_id' is missing from the product dataset.")

    elif table_name == 'DIM_STORE':
        # Perform any store-specific transformations
        if 'store_id' not in df.columns:
            logging.error("Column 'store_id' is missing from the store dataset.")

    # Add other table-specific transformations here (e.g., DIM_CUSTOMER, FACT_SALES)

    # Generic data validation: Drop rows with negative prices or quantities
    if 'unit_price' in df.columns:
        df = df[df['unit_price'] >= 0]
    if 'quantity' in df.columns:
        df = df[df['quantity'] >= 0]

    return df


# Load function: Load data into Azure SQL Database
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
        conn.close()  # Ensure the connection is closed


def verify_load(table_name):
    conn = create_connection()
    if conn is None:
        logging.error("No connection available to verify load.")
        return

    query = f"SELECT COUNT(*) FROM {table_name}"
    count = pd.read_sql(query, conn)
    print(f"{table_name} record count: {count.iloc[0, 0]}")
    conn.close()  # Ensure the connection is closed


# Main ETL function for each table
def run_etl(csv_file, table_name):
    # Extract
    extracted_data = extract(csv_file)
    logging.info(f"Extracted {len(extracted_data)} records from {csv_file}")

    # Transform
    transformed_data = transform(extracted_data, table_name)

    # Load
    load(transformed_data, table_name)

    # Verify load
    verify_load(table_name)


# Example usage
if __name__ == "__main__":
    run_etl('dim-product-csv.csv', 'DIM_PRODUCT')
    run_etl('dim-store-csv.csv', 'DIM_STORE')
    run_etl('dim-date-csv.csv', 'DIM_DATE')
    run_etl('dim-customer-csv.csv', 'DIM_CUSTOMER')
    run_etl('fact-sales-csv.csv', 'FACT_SALES')
