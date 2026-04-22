import pandas as pd
import sqlite3
import os
DATA_DIR = os.path.join(os.path.dirname(__file__), "archive")
DB_PATH = os.path.join(os.path.dirname(__file__), "retail.db")

def load_csvs():
    customers = pd.read_csv(os.path.join(DATA_DIR, "olist_customers_dataset.csv"))
    orders = pd.read_csv(os.path.join(DATA_DIR, "olist_orders_dataset.csv"))
    order_items = pd.read_csv(os.path.join(DATA_DIR, "olist_order_items_dataset.csv"))
    products = pd.read_csv(os.path.join(DATA_DIR, "olist_products_dataset.csv"))
    payments = pd.read_csv(os.path.join(DATA_DIR, "olist_order_payments_dataset.csv"))
    return customers, orders, order_items, products, payments

def clean_data(customers, orders, order_items, products, payments):
    orders = orders[orders['order_status'] == 'delivered']
    orders = orders.dropna(subset=['order_purchase_timestamp', 'customer_id'])
    orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])
    order_items = order_items[order_items['price'] > 0]
    order_items['total_price'] = order_items['price'] + order_items['freight_value']
    customers = customers.dropna(subset=['customer_id', 'customer_unique_id'])
    products = products.dropna(subset=['product_id'])
    print(f"Orders after cleaning: {len(orders)}")
    print(f"Order items after cleaning: {len(order_items)}")
    return customers, orders, order_items, products, payments

def create_database(customers, orders, order_items, products, payments):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            customer_id TEXT PRIMARY KEY,
            customer_unique_id TEXT,
            country TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            product_id TEXT PRIMARY KEY,
            category TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            order_id TEXT PRIMARY KEY,
            customer_id TEXT,
            order_date TEXT,
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS order_items (
            order_id TEXT,
            product_id TEXT,
            quantity INTEGER,
            unit_price REAL,
            total_price REAL,
            FOREIGN KEY (order_id) REFERENCES orders(order_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        )
    """)
    customers_data = customers[['customer_id', 'customer_unique_id', 'customer_state']].copy()
    customers_data.columns = ['customer_id', 'customer_unique_id', 'country']
    customers_data.drop_duplicates(subset=['customer_id'], inplace=True)
    customers_data.to_sql('customers', conn, if_exists='replace', index=False)
    products_data = products[['product_id', 'product_category_name']].copy()
    products_data.columns = ['product_id', 'category']
    products_data.drop_duplicates(subset=['product_id'], inplace=True)
    products_data.to_sql('products', conn, if_exists='replace', index=False)
    orders_data = orders[['order_id', 'customer_id', 'order_purchase_timestamp']].copy()
    orders_data.columns = ['order_id', 'customer_id', 'order_date']
    orders_data.drop_duplicates(subset=['order_id'], inplace=True)
    orders_data.to_sql('orders', conn, if_exists='replace', index=False)
    order_items_data = order_items[['order_id', 'product_id', 'price', 'freight_value', 'total_price']].copy()
    order_items_data['quantity'] = 1
    order_items_data = order_items_data[['order_id', 'product_id', 'quantity', 'price', 'total_price']]
    order_items_data.columns = ['order_id', 'product_id', 'quantity', 'unit_price', 'total_price']
    order_items_data.to_sql('order_items', conn, if_exists='replace', index=False)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_orders_customer ON orders(customer_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_orders_date ON orders(order_date)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_order_items_order ON order_items(order_id)")
    
    conn.commit()
    conn.close()
    print("Database created successfully at:", DB_PATH)
    return DB_PATH

def main():
    print("Loading CSVs...")
    customers, orders, order_items, products, payments = load_csvs()
    print("Cleaning data...")
    customers, orders, order_items, products, payments = clean_data(customers, orders, order_items, products, payments)
    print("Creating database...")
    create_database(customers, orders, order_items, products, payments)

if __name__ == "__main__":
    main()