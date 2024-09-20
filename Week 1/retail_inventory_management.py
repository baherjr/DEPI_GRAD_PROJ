from pyspark.sql import SparkSession
from pyspark.sql import functions as F

# Initialize Spark Session
spark = SparkSession.builder.appName("RetailInventoryManagement").getOrCreate()

# Sample data for Suppliers, Products, Inventory, and Sales tables
suppliers_data = [
    (1, 'Supplier A', 'contactA@example.com'),
    (2, 'Supplier B', 'contactB@example.com'),
    (3, 'Supplier C', 'contactC@example.com'),
    (4, 'Supplier D', 'contactD@example.com'),
    (5, 'Supplier E', 'contactE@example.com'),
    (6, 'Supplier F', 'contactF@example.com'),
    (7, 'Supplier G', 'contactG@example.com')
]

products_data = [
    (1, 'Laptop A', 'Electronics', 1, 1000.00),
    (2, 'Smartphone B', 'Electronics', 1, 700.00),
    (3, 'Tablet C', 'Electronics', 2, 400.00),
    (4, 'Headphones D', 'Accessories', 2, 150.00),
    (5, 'Keyboard E', 'Accessories', 3, 50.00),
    (6, 'Office Chair', 'Furniture', 4, 120.00),
    (7, 'Desk Lamp', 'Furniture', 4, 30.00),
    (8, 'Coffee Machine', 'Appliances', 5, 85.00),
    (9, 'Microwave Oven', 'Appliances', 5, 120.00),
    (10, 'Blender', 'Appliances', 5, 60.00),
    (11, 'Standing Desk', 'Furniture', 4, 300.00),
    (12, 'Wireless Mouse', 'Accessories', 3, 25.00),
    (13, 'Gaming Laptop', 'Electronics', 6, 1500.00),
    (14, 'Smartwatch', 'Electronics', 6, 250.00),
    (15, 'Air Conditioner', 'Appliances', 7, 400.00),
    (16, 'Water Heater', 'Appliances', 7, 350.00),
    (17, 'Vacuum Cleaner', 'Appliances', 5, 150.00),
    (18, 'Gaming Keyboard', 'Accessories', 3, 80.00)
]

inventory_data = [
    (1, 1, 'Warehouse 1', 20),
    (2, 2, 'Warehouse 1', 15),
    (3, 3, 'Warehouse 2', 30),
    (4, 4, 'Warehouse 2', 40),
    (5, 5, 'Warehouse 3', 50),
    (6, 6, 'Warehouse 3', 35),
    (7, 7, 'Warehouse 4', 60),
    (8, 8, 'Warehouse 4', 25),
    (9, 9, 'Warehouse 1', 10),
    (10, 10, 'Warehouse 2', 5),
    (11, 11, 'Warehouse 3', 20),
    (12, 12, 'Warehouse 1', 50),
    (13, 13, 'Warehouse 2', 15),
    (14, 14, 'Warehouse 4', 25),
    (15, 15, 'Warehouse 3', 8),
    (16, 16, 'Warehouse 2', 10)
]

sales_data = [
    (1, 1, 5, '2024-09-01', 950.00),
    (2, 2, 3, '2024-09-01', 700.00),
    (3, 3, 2, '2024-09-02', 400.00),
    (4, 4, 6, '2024-09-02', 150.00),
    (5, 5, 4, '2024-09-03', 45.00),
    (6, 6, 1, '2024-09-03', 120.00),
    (7, 7, 3, '2024-09-04', 30.00),
    (8, 8, 2, '2024-09-05', 85.00),
    (9, 9, 1, '2024-09-05', 115.00),
    (10, 10, 4, '2024-09-06', 55.00),
    (11, 11, 3, '2024-09-07', 280.00),
    (12, 12, 5, '2024-09-07', 25.00),
    (13, 13, 2, '2024-09-08', 1500.00),
    (14, 14, 4, '2024-09-08', 240.00),
    (15, 15, 1, '2024-09-09', 390.00),
    (16, 16, 2, '2024-09-09', 350.00)
]

# Create DataFrames
suppliers_df = spark.createDataFrame(suppliers_data, ["supplier_id", "supplier_name", "contact_info"])
products_df = spark.createDataFrame(products_data, ["product_id", "product_name", "category", "supplier_id", "price"])
inventory_df = spark.createDataFrame(inventory_data, ["inventory_id", "product_id", "warehouse_location", "quantity_in_stock"])
sales_df = spark.createDataFrame(sales_data, ["sale_id", "product_id", "quantity_sold", "sale_date", "sale_price"])

# Query 1: Products Running Low on Stock
low_stock_df = products_df.join(inventory_df, "product_id") \
    .filter(inventory_df.quantity_in_stock < 10) \
    .select("product_name", "warehouse_location", "quantity_in_stock")
low_stock_df.show()

# Query 2: Total Sales Revenue for Each Product
total_sales_revenue_df = products_df.join(sales_df, "product_id") \
    .groupBy("product_name") \
    .agg(F.sum(sales_df.quantity_sold * sales_df.sale_price).alias("total_sales_revenue")) \
    .orderBy(F.desc("total_sales_revenue"))
total_sales_revenue_df.show()

# Query 3: Daily Sales Summary
daily_sales_df = sales_df.groupBy("sale_date") \
    .agg(F.sum(sales_df.sale_price * sales_df.quantity_sold).alias("daily_sales")) \
    .orderBy("sale_date")
daily_sales_df.show()

# Query 4: Supplier-wise Product Distribution
supplier_distribution_df = suppliers_df.join(products_df, "supplier_id") \
    .groupBy("supplier_name") \
    .agg(F.count("product_id").alias("number_of_products"))
supplier_distribution_df.show()

# Query 5: Products with Highest Sales Volume
highest_sales_volume_df = products_df.join(sales_df, "product_id") \
    .groupBy("product_name") \
    .agg(F.sum(sales_df.quantity_sold).alias("total_quantity_sold")) \
    .orderBy(F.desc("total_quantity_sold"))
highest_sales_volume_df.show()

# Query 6: Sales by Warehouse Location
sales_by_warehouse_df = inventory_df.join(sales_df, "product_id") \
    .groupBy("warehouse_location") \
    .agg(F.sum(sales_df.quantity_sold * sales_df.sale_price).alias("warehouse_sales")) \
    .orderBy(F.desc("warehouse_sales"))
sales_by_warehouse_df.show()

# Query 7: Average Sales Price for Each Product
avg_sales_price_df = products_df.join(sales_df, "product_id") \
    .groupBy("product_name") \
    .agg(F.avg(sales_df.sale_price).alias("avg_sale_price")) \
    .orderBy(F.desc("avg_sale_price"))
avg_sales_price_df.show()

# Query 8: Inventory Status by Supplier
inventory_by_supplier_df = suppliers_df.join(products_df, "supplier_id") \
    .join(inventory_df, "product_id") \
    .groupBy("supplier_name") \
    .agg(F.sum(inventory_df.quantity_in_stock).alias("total_stock")) \
    .orderBy(F.desc("total_stock"))
inventory_by_supplier_df.show()

# Query 9: Products Never Sold
never_sold_df = products_df.join(sales_df, "product_id", "left_anti") \
    .select("product_name")
never_sold_df.show()

# Query 10: Most Popular Categories by Sales Revenue
popular_categories_df = products_df.join(sales_df, "product_id") \
    .groupBy("category") \
    .agg(F.sum(sales_df.quantity_sold * sales_df.sale_price).alias("total_category_sales")) \
    .orderBy(F.desc("total_category_sales"))
popular_categories_df.show()

# Stop the Spark Session
spark.stop()
