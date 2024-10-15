import os
from urllib.parse import quote_plus
from sqlalchemy import create_engine, text, exc  # Updated import for text() and exc
import sqlalchemy as sa  # Import sqlalchemy as sa
from sqlalchemy.exc import SQLAlchemyError
import pyodbc
import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
DB_CONFIG = {
    'mssql': {
        'server': os.getenv('MSSQL_SERVER'),
        'database': os.getenv('MSSQL_DATABASE'),
        'driver': 'SQL Server',  # This will be overridden if a suitable driver is found
    },
    'postgresql': {
        'host': os.getenv('POSTGRESQL_HOST'),
        'database': os.getenv('POSTGRESQL_DATABASE'),
        'user': os.getenv('POSTGRESQL_USER'),
        'password': os.getenv('POSTGRESQL_PASSWORD'),
        'port': os.getenv('POSTGRESQL_PORT')
    }
}


def get_mssql_connection():
    try:
        drivers = [driver for driver in pyodbc.drivers() if 'SQL Server' in driver]
        print("Available SQL Server ODBC drivers:", drivers)

        if not drivers:
            raise ValueError("No SQL Server ODBC driver found")

        DB_CONFIG['mssql']['driver'] = drivers[0]

        connection_string = (
            f"mssql+pyodbc://{DB_CONFIG['mssql']['server']}/"
            f"{DB_CONFIG['mssql']['database']}?driver={DB_CONFIG['mssql']['driver'].replace(' ', '+')}"
            "&trusted_connection=yes"
        )

        print(f"Attempting to connect to MSSQL with: {connection_string}")

        engine = create_engine(connection_string)
        connection = engine.connect()

        # Metadata query to check for DimVehicle table
        metadata_query = """
        SELECT [INFORMATION_SCHEMA].[TABLES].[TABLE_NAME] 
        FROM [INFORMATION_SCHEMA].[TABLES] 
        WHERE 
            ([INFORMATION_SCHEMA].[TABLES].[TABLE_TYPE] = CAST(:table_type1 AS NVARCHAR(255)) 
            OR [INFORMATION_SCHEMA].[TABLES].[TABLE_TYPE] = CAST(:table_type2 AS NVARCHAR(255)))
            AND [INFORMATION_SCHEMA].[TABLES].[TABLE_NAME] = CAST(:table_name AS NVARCHAR(255)) 
            AND [INFORMATION_SCHEMA].[TABLES].[TABLE_SCHEMA] = CAST(:table_schema AS NVARCHAR(255));
        """

        params = {
            'table_type1': 'BASE TABLE',
            'table_type2': 'VIEW',
            'table_name': 'DimVehicle',  # Check if this table exists
            'table_schema': 'dbo'
        }

        # Execute the metadata query
        result = connection.execute(sa.text(metadata_query), params)
        tables = result.fetchall()

        if tables:
            # Accessing the first column (TABLE_NAME) using index 0
            print(f"Table DimVehicle exists: {tables[0][0]}")
        else:
            print("Table DimVehicle does not exist")

        return connection

    except (SQLAlchemyError, pyodbc.Error) as e:
        print(f"Error connecting to MSSQL: {e}")
        return None



def get_postgresql_connection():
    try:
        encoded_password = quote_plus(DB_CONFIG['postgresql']['password'])
        connection_string = (
            f"postgresql://{DB_CONFIG['postgresql']['user']}:"
            f"{encoded_password}@"
            f"{DB_CONFIG['postgresql']['host']}:"
            f"{DB_CONFIG['postgresql']['port']}/"
            f"{DB_CONFIG['postgresql']['database']}"
        )

        print(f"Attempting to connect to PostgreSQL with: {connection_string}")

        engine = create_engine(connection_string)
        return engine.connect()
    except (SQLAlchemyError, psycopg2.Error) as e:
        print(f"Error connecting to PostgreSQL (Method 1): {e}")

        try:
            engine = create_engine(
                'postgresql://',
                connect_args=DB_CONFIG['postgresql']
            )
            print("Attempting to connect to PostgreSQL with key-value pairs")
            return engine.connect()
        except (SQLAlchemyError, psycopg2.Error) as e2:
            print(f"Error connecting to PostgreSQL (Method 2): {e2}")
            return None


def get_connection(db_type='mssql'):
    if db_type.lower() == 'mssql':
        return get_mssql_connection()
    elif db_type.lower() == 'postgresql':
        return get_postgresql_connection()
    else:
        raise ValueError("Unsupported database type. Use 'mssql' or 'postgresql'.")


# Test the connections
if __name__ == "__main__":
    for db_type in ['mssql', 'postgresql']:
        print(f"\nTesting {db_type.upper()} connection:")
        conn = get_connection(db_type)
        if conn:
            print(f"Connection to {db_type.upper()} successful")
            conn.close()
        else:
            print(f"Failed to connect to {db_type.upper()}")
