from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
import pyodbc


def get_connection():
    try:
        # List available drivers
        drivers = [driver for driver in pyodbc.drivers()]
        print("Available ODBC drivers:", drivers)

        # Choose the appropriate driver (prefer newer versions)
        driver = next((driver for driver in drivers if 'SQL Server' in driver), None)
        if not driver:
            raise ValueError("No SQL Server ODBC driver found")

        # Construct the connection string
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


# Test the connection
if __name__ == "__main__":
    conn = get_connection()
    if conn:
        print("Connection successful")
        conn.close()
    else:
        print("Failed to connect to the database")