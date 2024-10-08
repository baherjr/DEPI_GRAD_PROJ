import os
import schedule
import time
from DataPipeline import run_etl

def run_all_etl_jobs():
    print("Starting ETL jobs...")
    
    # Define your CSV files and corresponding table names
    etl_jobs = [
        ('dim-product-csv.csv', 'DIM_PRODUCT'),
        ('dim-store-csv.csv', 'DIM_STORE'),
        ('dim-date-csv.csv', 'DIM_DATE'),
        ('dim-customer-csv.csv', 'DIM_CUSTOMER'),
        ('fact-sales-csv.csv', 'FACT_SALES')
    ]
    
    for csv_file, table_name in etl_jobs:
        csv_path = os.path.join('data', csv_file)  # Assuming CSV files are in a 'data' directory
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
