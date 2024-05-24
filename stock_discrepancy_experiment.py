import pandas as pd
import numpy as np
import random

# Function to generate sample data
def generate_sample_data(num_products=200, num_records=1000):
    product_ids = list(range(1, num_products + 1))
    product_names = [f'Product_{i}' for i in product_ids]

    data = []
    for _ in range(num_records):
        product_id = random.choice(product_ids)
        product_name = product_names[product_id - 1]
        stock_before = random.randint(0, 50)
        stock_after = max(0, stock_before + random.randint(-5, 5))  # Ensure stock doesn't go negative
        discrepancy = stock_after - stock_before
        data.append([product_id, product_name, stock_before, stock_after, discrepancy])

    return pd.DataFrame(data, columns=['product_id', 'product_name', 'stock_before', 'stock_after', 'discrepancy'])

# Generate sample data
inventory_data = generate_sample_data()

# Save to CSV on local computer folder
inventory_data.to_csv('sample_inventory_data.csv', index=False)
print("Sample data generated and saved to 'sample_inventory_data.csv'.")

# Now load and validate the data using the previously defined functions
def calculate_metrics(inventory_data):
    total_skus = len(inventory_data)
    accurate_counts = inventory_data[inventory_data['discrepancy'] == 0].shape[0]
    discrepancies = inventory_data[inventory_data['discrepancy'] != 0].shape[0]
    total_discrepancy_amount = inventory_data['discrepancy'].abs().sum()
    out_of_stock = inventory_data[inventory_data['stock_after'] == 0].shape[0]
    stock_adjustments = inventory_data.shape[0]

    iar = (accurate_counts / total_skus) * 100
    dr = (discrepancies / total_skus) * 100
    ada = total_discrepancy_amount / discrepancies if discrepancies else 0
    oosr = (out_of_stock / total_skus) * 100
    saf = stock_adjustments  # Assuming each row is a stock adjustment
    cca = (accurate_counts / total_skus) * 100  # Assuming cycle count accuracy is the same as IAR

    return {
        'Inventory Accuracy Rate (IAR)': iar,
        'Discrepancy Rate (DR)': dr,
        'Average Discrepancy Amount (ADA)': ada,
        'Out-of-Stock Rate (OOSR)': oosr,
        'Stock Adjustment Frequency (SAF)': saf,
        'Cycle Count Accuracy (CCA)': cca
    }

# Load the sample data
inventory_data = pd.read_csv('sample_inventory_data.csv')

# Calculate and print the metrics
metrics = calculate_metrics(inventory_data)
for metric, value in metrics.items():
    print(f'{metric}: {value:.2f}%')


