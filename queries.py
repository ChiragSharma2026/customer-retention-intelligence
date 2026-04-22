import sqlite3
import pandas as pd
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "retail.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    return conn

def total_revenue():
    conn = get_connection()
    query = """
        SELECT ROUND(SUM(total_price), 2) AS total_revenue
        FROM order_items
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def monthly_revenue():
    conn = get_connection()
    query = """
        SELECT 
            STRFTIME('%Y-%m', o.order_date) AS month,
            ROUND(SUM(oi.total_price), 2) AS revenue
        FROM orders o
        JOIN order_items oi ON o.order_id = oi.order_id
        GROUP BY month
        ORDER BY month
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def repeat_vs_new_customers():
    conn = get_connection()
    query = """
        WITH customer_orders AS (
            SELECT c.customer_unique_id, COUNT(*) AS order_count
            FROM orders o
            JOIN customers c ON o.customer_id = c.customer_id
            GROUP BY c.customer_unique_id
        )
        SELECT
            COUNT(CASE WHEN order_count = 1 THEN 1 END) AS one_time_customers,
            COUNT(CASE WHEN order_count > 1 THEN 1 END) AS repeat_customers
        FROM customer_orders
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def customer_lifetime_value():
    conn = get_connection()
    query = """
        SELECT
            c.customer_unique_id AS customer_id,
            ROUND(SUM(oi.total_price), 2) AS lifetime_value
        FROM orders o
        JOIN customers c ON o.customer_id = c.customer_id
        JOIN order_items oi ON o.order_id = oi.order_id
        GROUP BY c.customer_unique_id
        ORDER BY lifetime_value DESC
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def top_customer_contribution():
    conn = get_connection()
    query = """
        SELECT
            c.customer_unique_id AS customer_id,
            ROUND(SUM(oi.total_price), 2) AS revenue,
            ROUND(SUM(SUM(oi.total_price)) OVER(), 2) AS total_revenue
        FROM orders o
        JOIN customers c ON o.customer_id = c.customer_id
        JOIN order_items oi ON o.order_id = oi.order_id
        GROUP BY c.customer_unique_id
        ORDER BY revenue DESC
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def cohort_analysis():
    conn = get_connection()
    query = """
        WITH first_purchase AS (
            SELECT c.customer_unique_id, MIN(o.order_date) AS first_order
            FROM orders o
            JOIN customers c ON o.customer_id = c.customer_id
            GROUP BY c.customer_unique_id
        ),
        cohort_data AS (
            SELECT
                c.customer_unique_id,
                STRFTIME('%Y-%m', fp.first_order) AS cohort_month,
                STRFTIME('%Y-%m', o.order_date) AS order_month
            FROM orders o
            JOIN customers c ON o.customer_id = c.customer_id
            JOIN first_purchase fp ON c.customer_unique_id = fp.customer_unique_id
        )
        SELECT
            cohort_month,
            order_month,
            COUNT(DISTINCT customer_unique_id) AS users
        FROM cohort_data
        GROUP BY cohort_month, order_month
        ORDER BY cohort_month, order_month
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def product_performance():
    conn = get_connection()
    query = """
        SELECT
            p.category,
            SUM(oi.quantity) AS total_sold,
            ROUND(SUM(oi.total_price), 2) AS revenue
        FROM order_items oi
        JOIN products p ON oi.product_id = p.product_id
        GROUP BY p.category
        ORDER BY revenue DESC
        LIMIT 15
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    category_map = {
        'beleza_saude': 'Health & Beauty',
        'relogios_presentes': 'Watches & Gifts',
        'cama_mesa_banho': 'Bed & Bath',
        'esporte_lazer': 'Sports & Leisure',
        'informatica_acessorios': 'Computers & Accessories',
        'moveis_decoracao': 'Furniture & Decor',
        'utilidades_domesticas': 'Home Utilities',
        'cool_stuff': 'Cool Stuff',
        'automotivo': 'Automotive',
        'ferramentas_jardim': 'Tools & Garden',
        'brinquedos': 'Toys',
        'bebes': 'Baby Products',
        'perfumaria': 'Perfumery',
        'telefonia': 'Telephony',
        'moveis_escritorio': 'Office Furniture'
    }    
    df['category'] = df['category'].map(category_map).fillna(df['category'])
    return df

if __name__ == "__main__":
    print("Total Revenue:")
    print(total_revenue())
    print("\nMonthly Revenue (first 5 rows):")
    print(monthly_revenue().head())
    print("\nRepeat vs New Customers:")
    print(repeat_vs_new_customers())
    print("\nTop 5 Customers by CLV:")
    print(customer_lifetime_value().head())
    print("\nProduct Performance (Top 5):")
    print(product_performance().head())
    print("\nCohort Analysis (first 5 rows):")
    print(cohort_analysis().head())