import pandas as pd
from sqlalchemy import create_engine
import pyodbc


# Define the connection to SQL Server
def create_connection():
    # Change the connection string as needed
    connection_string = (
        "mssql+pyodbc://ATRXLO/RetailInventoryDWHStar?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
    )
    engine = create_engine(connection_string)
    return engine


# Extract function: Read data from CSV file
def extract(file_path):
    try:
        df = pd.read_csv(file_path)
        print(f"Extracted {len(df)} records from {file_path}.")
        return df
    except Exception as e:
        print(f"Error during extraction: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on error


# Transform function: Clean and validate data
def transform(df):
    # Check for missing values
    if df.isnull().values.any():
        print("Data contains missing values. Filling with default values or dropping rows.")
        df.fillna({
            'product_id': 0,  # or df['product_id'].mean() if numeric
            'product_name': 'Unknown',
            'category': 'Miscellaneous',
            'unit_price': 0.00,
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

    # Validate product_id (must be unique)
    if 'product_id' in df.columns and not df['product_id'].is_unique:
        print("Warning: Duplicate product_ids found.")
        df.drop_duplicates(subset=['product_id'], inplace=True)

    # Validate unit_price
    if 'unit_price' in df.columns:
        df = df[df['unit_price'] >= 0]  # Drop negative prices

    print(f"Transformed data contains {len(df)} records after validation.")
    return df


# Load function: Load data into SQL Server
def load(df, table_name):
    engine = create_connection()
    try:
        # Append data to the SQL table
        df.to_sql(table_name, con=engine, if_exists='append', index=False)
        print(f"Loaded {len(df)} records into {table_name}.")
    except Exception as e:
        print(f"Error during loading to {table_name}: {e}")


# Main ETL function for each table
def run_etl(csv_file_path, table_name):
    # Extract
    extracted_data = extract(csv_file_path)

    if not extracted_data.empty:
        # Transform
        transformed_data = transform(extracted_data)

        # Load
        load(transformed_data, table_name)


# Example usage
if __name__ == "__main__":
    # Specify the paths to your CSV files
    # run_etl('dim-product-csv.csv', 'DIM_PRODUCT')
    # run_etl('dim-store-csv.csv', 'DIM_STORE')
    # run_etl('dim-date-csv.csv', 'DIM_DATE')
    # run_etl('dim-customer-csv.csv', 'DIM_CUSTOMER')
    # run_etl('fact-sales-csv.csv', 'FACT_SALES')
    pass
