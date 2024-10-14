import csv
from datetime import datetime, timedelta
import random


# Function to read CSV file
def read_csv(file_path):
    with open(file_path, 'r') as f:
        reader = csv.DictReader(f)
        return list(reader)


# Function to write CSV file
def write_csv(file_path, headers, data):
    with open(file_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(data)


# Read the input data
input_data = read_csv('data.csv')

# Create DimVehicle
vehicles = {}
vehicle_data = []
for idx, row in enumerate(input_data, 1):
    vehicle_id = f"{row['Make']}_{row['Model']}_{row['Year']}"
    if vehicle_id not in vehicles:
        vehicles[vehicle_id] = idx
        vehicle_data.append([
            idx,
            vehicle_id,
            row['Make'],
            row['Model'],
            row['Year'],
            row['Engine Fuel Type'],
            row['Transmission Type'],
            f"{row['Engine Cylinders']}-cylinder",
            row['Number of Doors'],
            row['Driven_Wheels'],
            row['Engine HP'],
            row['MSRP']
        ])

write_csv('DataPipeline/DataPipeline/dim_vehicle.csv',
          ['VehicleKey', 'VehicleID', 'Make', 'Model', 'Year', 'FuelType', 'Transmission', 'Engine', 'NumberOfDoors',
           'Drivetrain', 'MaxPower', 'Price'],
          vehicle_data)

# Create DimDealership (sample data)
dealerships = [
    [1, 'D001', 'New York, NY', 'Franchise', 'New Cars'],
    [2, 'D002', 'Los Angeles, CA', 'Independent', 'Used Cars'],
    [3, 'D003', 'Chicago, IL', 'Franchise', 'New and Used Cars'],
    [4, 'D004', 'Houston, TX', 'Franchise', 'New Cars'],
    [5, 'D005', 'Phoenix, AZ', 'Independent', 'Used Cars'],
    [6, 'D006', 'Philadelphia, PA', 'Franchise', 'New and Used Cars'],
    [7, 'D007', 'San Antonio, TX', 'Independent', 'Used Cars'],
    [8, 'D008', 'San Diego, CA', 'Franchise', 'New Cars'],
    [9, 'D009', 'Dallas, TX', 'Franchise', 'New and Used Cars'],
    [10, 'D010', 'San Jose, CA', 'Independent', 'Used Cars'],
    [11, 'D011', 'Austin, TX', 'Franchise', 'New Cars'],
    [12, 'D012', 'Jacksonville, FL', 'Independent', 'Used Cars'],
    [13, 'D013', 'San Francisco, CA', 'Franchise', 'New and Used Cars'],
    [14, 'D014', 'Columbus, OH', 'Independent', 'Used Cars'],
    [15, 'D015', 'Fort Worth, TX', 'Franchise', 'New Cars']
]

write_csv('DataPipeline/DataPipeline/dim_dealership.csv',
          ['DealershipKey', 'DealershipID', 'Location', 'OwnerType', 'SellerType'],
          dealerships)

# Create DimDate (for the year 2023)
date_data = []
start_date = datetime(2023, 1, 1)
for i in range(365):
    date = start_date + timedelta(days=i)
    date_data.append([
        int(date.strftime('%Y%m%d')),
        date.strftime('%Y-%m-%d'),
        date.year,
        date.month,
        date.strftime('%B'),
        (date.month - 1) // 3 + 1
    ])

write_csv('DataPipeline/DataPipeline/dim_date.csv',
          ['DateKey', 'Date', 'Year', 'Month', 'MonthName', 'Quarter'],
          date_data)

# Create FactSales
sales_data = []
for idx, row in enumerate(input_data, 1):
    vehicle_id = f"{row['Make']}_{row['Model']}_{row['Year']}"
    vehicle_key = vehicles[vehicle_id]
    date_key = random.randint(20230101, 20231231)
    dealership_key = random.randint(1, 15)
    quantity_sold = 1  # Assuming each row represents a single sale
    total_amount = float(row['MSRP'])

    sales_data.append([idx, date_key, vehicle_key, dealership_key, quantity_sold, total_amount])

write_csv('DataPipeline/DataPipeline/fact_sales.csv',
          ['SaleID', 'DateKey', 'VehicleKey', 'DealershipKey', 'QuantitySold', 'TotalAmount'],
          sales_data)

# Create FactInventory
inventory_data = []
for idx, vehicle_key in enumerate(vehicles.values(), 1):
    for month in range(1, 13):  # Generate inventory data for each month of 2023
        date_key = int(f"2023{month:02d}01")  # First day of each month
        stock_level = random.randint(0, 20)  # Random stock level between 0 and 20

        inventory_data.append([idx, date_key, vehicle_key, stock_level])

write_csv('DataPipeline/DataPipeline/fact_inventory.csv',
          ['InventoryID', 'DateKey', 'VehicleKey', 'StockLevel'],
          inventory_data)

print("CSV files have been created successfully.")