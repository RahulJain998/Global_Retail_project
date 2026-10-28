import numpy as np
import pandas as pd


np.random.seed(42)
n_rows = 100000

print("Generating 100,000 synthetic sales records...")


transaction_ids = [f"TXN-{100000 + i}" for i in range(n_rows)]
start_date = pd.to_datetime("2024-01-01")
dates = [
    start_date + pd.Timedelta(days=int(np.random.randint(0, 730)), hours=int(np.random.randint(0, 24)))
    for _ in range(n_rows)
]
customer_ids = [f"CUST-{np.random.randint(1000, 5000)}" for i in range(n_rows)]
regions = np.random.choice(["North", "South", "East", "West", "Central"], size=n_rows, p=[0.25, 0.20, 0.25, 0.15, 0.15])
categories = np.random.choice(["Electronics", "Apparel", "Home & Kitchen", "Sports"], size=n_rows, p=[0.4, 0.3, 0.2, 0.1])

product_dict = {
    "Electronics": ["MacBook Pro", "Wireless Mouse", "4K Monitor", "Mechanical Keyboard"],
    "Apparel": ["Denim Jacket", "Cotton T-Shirt", "Running Shoes", "Formal Trousers"],
    "Home & Kitchen": ["Air Fryer", "Coffee Maker", "Blender", "Electric Kettle"],
    "Sports": ["Yoga Mat", "Dumbbell Set", "Resistance Bands", "Running Backpack"]
}

products = [np.random.choice(product_dict[cat]) for cat in categories]
quantities = np.random.choice([1, 2, 3, 4, 5], size=n_rows, p=[0.5, 0.25, 0.15, 0.07, 0.03])
unit_prices = np.round(np.random.uniform(20.0, 1500.0, size=n_rows), 2)
discounts = np.random.choice([0.0, 0.05, 0.10, 0.15, 0.20], size=n_rows, p=[0.4, 0.3, 0.15, 0.1, 0.05])
payment_methods = np.random.choice(["Credit Card", "UPI", "Net Banking", "Cash on Delivery"], size=n_rows)

raw_df = pd.DataFrame({
    "transaction_id": transaction_ids,
    "order_date": dates,
    "customer_id": customer_ids,
    "region": regions,
    "product_category": categories,
    "product_name": products,
    "quantity": quantities,
    "unit_price": unit_prices,
    "discount_percentage": discounts,
    "payment_method": payment_methods
})

# print(raw_df.head())


raw_df['revenue'] = raw_df["quantity"] * raw_df["unit_price"] * (1 - raw_df["discount_percentage"])


raw_df.loc[np.random.choice(n_rows, 1500), "unit_price"] = np.nan
raw_df.loc[np.random.choice(n_rows, 800), "region"] = None

# 2. Inject duplicate rows
raw_df = pd.concat([raw_df, raw_df.sample(n=500, random_state=42)], ignore_index=True)

print(f"Raw dataset shape (with anomalies): {raw_df.shape}")
raw_df.to_csv("sales_data_raw.csv", index=False)

print(raw_df.info())

print("\nStarting Data Cleaning Pipeline...")