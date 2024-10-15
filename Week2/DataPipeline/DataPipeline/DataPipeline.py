import pandas as pd
import pyodbc
import os
import logging
from sqlalchemy import create_engine, Table, MetaData, insert
from dotenv import load_dotenv
from sqlalchemy import text

load_dotenv()

DB_CONFIG = {
    'mssql': {
        'server': os.getenv('MSSQL_SERVER'),
        'database': os.getenv('MSSQL_DATABASE'),
    },
}

# Configure logging
logging.basicConfig(level=logging.INFO)


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


def extract(file_path):
    """
    Extract data from a CSV file into a DataFrame.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        DataFrame: The extracted DataFrame or an empty DataFrame on error.
    """
    try:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(file_path)

        # Log the number of rows extracted
        logging.info(f"Extracted {len(df)} rows from {file_path}.")

        # Return the DataFrame
        return df
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}. Please check the path.")
        return pd.DataFrame()  # Return an empty DataFrame if the file is not found
    except pd.errors.EmptyDataError:
        logging.error(f"No data: The file at {file_path} is empty.")
        return pd.DataFrame()  # Return an empty DataFrame if the file is empty
    except pd.errors.ParserError:
        logging.error(f"Parsing error: Could not parse the file at {file_path}.")
        return pd.DataFrame()  # Return an empty DataFrame if there is a parsing error
    except Exception as e:
        logging.error(f"Error extracting data from {file_path}: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on any other error


def transform_dim_vehicle(df):
    """
    Transform the DimVehicle DataFrame.

    Args:
    - df (DataFrame): The DataFrame to transform.

    Returns:
    - DataFrame: Transformed DataFrame.
    """
    # Example transformation: Capitalize the 'Make' and 'Model' columns
    df['Make'] = df['Make'].str.upper()
    df['Model'] = df['Model'].str.title()

    # Convert 'Year' to integer
    df['Year'] = df['Year'].astype(int)

    # Ensure that 'FuelType', 'Transmission', and other categorical columns are in the right format
    df['FuelType'] = df['FuelType'].str.strip().str.lower()
    df['Transmission'] = df['Transmission'].str.strip().str.lower()

    # Check for any missing values in critical columns and handle them
    critical_columns = ['VehicleKey', 'VehicleID', 'Make', 'Model', 'Year', 'FuelType', 'Transmission']
    for col in critical_columns:
        if df[col].isnull().any():
            df[col].fillna('Unknown', inplace=True)

    # Remove any duplicates
    df.drop_duplicates(subset=['VehicleKey'], keep='last', inplace=True)

    # Ensure correct data types for numerical values
    df['MaxPower'] = pd.to_numeric(df['MaxPower'], errors='coerce')
    df['Price'] = pd.to_numeric(df['Price'], errors='coerce')

    # Additional transformations can be added as needed
    return df


def transform_dim_dealership(df):
    """
    Return the DimDealership DataFrame without any transformations.

    Args:
    - df (DataFrame): The DataFrame to transform.

    Returns:
    - DataFrame: The original DataFrame.
    """
    return df


def transform_dim_date(df):
    """
    Transform the DimDate DataFrame.

    Args:
    - df (DataFrame): The DataFrame to transform.

    Returns:
    - DataFrame: Transformed DataFrame.
    """
    # Ensure Date column is in datetime format
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    # Extract Day from the Date if it's not already present
    df['Day'] = df['Date'].dt.day

    # Strip whitespace from all string columns
    string_columns = ['MonthName']
    for col in string_columns:
        df[col] = df[col].str.strip()

    # Validate Month and Quarter columns
    df['Month'] = pd.to_numeric(df['Month'], errors='coerce')
    df['Quarter'] = pd.to_numeric(df['Quarter'], errors='coerce')

    # Check for any missing values in critical columns and handle them
    critical_columns = ['DateKey', 'Date', 'Year', 'Month', 'Day', 'Quarter']
    for col in critical_columns:
        if df[col].isnull().any():
            df[col].fillna('Unknown', inplace=True)

    # Remove duplicates based on DateKey
    df.drop_duplicates(subset=['DateKey'], keep='last', inplace=True)

    # Further processing can be added as needed
    return df


def transform_fact_sales(df):
    """
    Transform the FactSales DataFrame.

    Args:
    - df (DataFrame): The DataFrame to transform.

    Returns:
    - DataFrame: Transformed DataFrame.
    """
    # Ensure DateKey column is in the correct format
    df['DateKey'] = pd.to_numeric(df['DateKey'], errors='coerce')

    # Rename TotalAmount to Revenue for consistency with the SQL table
    df.rename(columns={'TotalAmount': 'Revenue'}, inplace=True)

    # Calculate SalesKey if needed, you may use an incremental integer or unique identifier logic
    df['SalesKey'] = range(1, len(df) + 1)

    # Strip whitespace from string columns if necessary
    string_columns = ['VehicleKey', 'DealershipKey']
    for col in string_columns:
        df[col] = df[col].astype(str).str.strip()

    # Validate QuantitySold and Revenue columns
    df['QuantitySold'] = pd.to_numeric(df['QuantitySold'], errors='coerce').fillna(0).astype(int)
    df['Revenue'] = pd.to_numeric(df['Revenue'], errors='coerce').fillna(0)

    # Check for missing values in critical columns and handle them
    critical_columns = ['SalesKey', 'VehicleKey', 'DealershipKey', 'DateKey', 'QuantitySold', 'Revenue']
    for col in critical_columns:
        if df[col].isnull().any():
            logging.warning(f"Missing values found in {col}. Filling with default values.")
            df[col].fillna(0, inplace=True)

    # Remove duplicates based on SalesKey
    df.drop_duplicates(subset=['SalesKey'], keep='last', inplace=True)

    return df


def transform_fact_inventory(df):
    """
    Transform the FactInventory DataFrame.

    Args:
    - df (DataFrame): The DataFrame to transform.

    Returns:
    - DataFrame: Transformed DataFrame.
    """
    # Ensure DateKey and VehicleKey columns are in the correct format
    df['DateKey'] = pd.to_numeric(df['DateKey'], errors='coerce')
    df['VehicleKey'] = df['VehicleKey'].astype(str).str.strip()
    df['DealershipKey'] = df['DealershipKey'].astype(str).str.strip()

    # Calculate InventoryKey if needed, you may use an incremental integer or unique identifier logic
    df['InventoryKey'] = range(1, len(df) + 1)

    # Validate StockLevel to ensure it's numeric
    df['StockLevel'] = pd.to_numeric(df['StockLevel'], errors='coerce').fillna(0)

    # Check for missing values in critical columns and handle them
    critical_columns = ['InventoryKey', 'VehicleKey', 'DealershipKey', 'DateKey', 'StockLevel']
    for col in critical_columns:
        if df[col].isnull().any():
            logging.warning(f"Missing values found in {col}. Filling with default values.")
            df[col].fillna(0, inplace=True)

    # Remove duplicates based on InventoryKey
    df.drop_duplicates(subset=['InventoryKey'], keep='last', inplace=True)

    return df


def load(df, table_name, conn):
    """
    Load the transformed DataFrame into the specified SQL table.

    Args:
        df (DataFrame): The DataFrame to load.
        table_name (str): The name of the table into which the DataFrame will be loaded.
        conn (Connection): The database connection object.
    """
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
        # If loading FactSales, check for DateKey existence in DimDate
        if table_name == 'FactSales':
            # Extract DateKey values from the DimDate table
            dim_date_query = text("SELECT DateKey FROM DimDate")
            dim_date_keys = pd.read_sql(dim_date_query, conn)['DateKey'].tolist()

            # Filter out rows with missing DateKeys
            df = df[df['DateKey'].isin(dim_date_keys)]

        # If loading FactInventory, check for DateKey existence in DimDate and VehicleKey existence in DimVehicle
        if table_name == 'FactInventory':
            # Extract DateKey values from the DimDate table
            dim_date_query = text("SELECT DateKey FROM DimDate")
            dim_date_keys = pd.read_sql(dim_date_query, conn)['DateKey'].tolist()
            # Extract VehicleKey values from the DimVehicle table
            dim_vehicle_query = text("SELECT VehicleKey FROM DimVehicle")
            dim_vehicle_keys = pd.read_sql(dim_vehicle_query, conn)['VehicleKey'].tolist()

            # Filter out rows with missing DateKeys and VehicleKeys
            df = df[df['DateKey'].isin(dim_date_keys) & df['VehicleKey'].isin(dim_vehicle_keys)]

        # Use the to_sql method for inserting data
        df.to_sql(table_name, conn, if_exists='append', index=False)
        logging.info(f"Loaded {len(df)} rows into {table_name}.")
        conn.commit()

    except Exception as e:
        logging.error(f"Error loading data into {table_name}: {e}")


def run_etl(conn):
    """
    Execute the ETL process: extract data from CSV files, transform the data,
    and load the transformed data into SQL tables.

    Args:
        conn (Connection): The database connection object.
    """
    try:
        # Extract data from CSV files
        dim_vehicle_df = extract('dim_vehicle.csv')
        dim_dealership_df = extract('dim_dealership.csv')
        dim_date_df = extract('dim_date.csv')
        fact_sales_df = extract('fact_sales.csv')
        fact_inventory_df = extract('fact_inventory.csv')

        # Log DataFrame columns
        logging.info(f"DimVehicle DataFrame columns: {dim_vehicle_df.columns.tolist()}")
        logging.info(f"DimDealership DataFrame columns: {dim_dealership_df.columns.tolist()}")
        logging.info(f"DimDate DataFrame columns: {dim_date_df.columns.tolist()}")
        logging.info(f"FactSales DataFrame columns: {fact_sales_df.columns.tolist()}")
        logging.info(f"FactInventory DataFrame columns: {fact_inventory_df.columns.tolist()}")

        # # Ensure all required columns are present in DataFrames
        required_columns_dim_dealership = ['DealershipKey', 'DealershipID', 'Location', 'OwnerType', 'SellerType']
        missing_columns_dim_dealership = [col for col in required_columns_dim_dealership if
                                          col not in dim_dealership_df.columns]

        if missing_columns_dim_dealership:
            logging.error(f"Missing columns in DimDealership: {missing_columns_dim_dealership}")
            return

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


if __name__ == "__main__":
    run_etl(create_connection())
