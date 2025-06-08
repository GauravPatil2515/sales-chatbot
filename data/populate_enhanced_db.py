# Enhanced Database Population Script
# Implements all suggested improvements for more realistic data

import sqlite3
from faker import Faker
import random
import os
from datetime import datetime, timedelta

# Initialize Faker
fake = Faker()

# Connect to SQLite database (creates file if not exists)
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sales.db")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Drop existing tables to recreate with new schema
cursor.execute("DROP TABLE IF EXISTS orders;")
cursor.execute("DROP TABLE IF EXISTS products;")
cursor.execute("DROP TABLE IF EXISTS customers;")

print("🔄 Creating enhanced database schema...")

# Create customers table (NEW!)
cursor.execute("""
    CREATE TABLE customers (
        customer_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        join_date TEXT NOT NULL,
        customer_type TEXT NOT NULL DEFAULT 'regular'
    );
""")

# Create enhanced products table
cursor.execute("""
    CREATE TABLE products (
        product_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        base_price REAL NOT NULL,
        stock_level INTEGER NOT NULL DEFAULT 100
    );
""")

# Create enhanced orders table with customer_id and status
cursor.execute("""
    CREATE TABLE orders (
        order_id INTEGER PRIMARY KEY,
        customer_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        price REAL NOT NULL,
        order_date TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'completed',
        FOREIGN KEY(customer_id) REFERENCES customers(customer_id),
        FOREIGN KEY(product_id) REFERENCES products(product_id)
    );
""")

print("📊 Generating realistic customer data...")

# Insert 50 customers with realistic data
customers = []
customer_types = ['regular', 'premium', 'vip']
for i in range(1, 51):
    name = fake.name()
    email = fake.email()
    join_date = fake.date_between(start_date='-2y', end_date='-30d')
    customer_type = random.choices(customer_types, weights=[70, 25, 5])[0]
    customers.append((i, name, email, join_date.strftime('%Y-%m-%d'), customer_type))

cursor.executemany("INSERT INTO customers VALUES (?, ?, ?, ?, ?);", customers)

print("🛍️ Creating diverse product catalog...")

# Enhanced products with more realistic variety
categories = ["Electronics", "Clothing", "Books", "Home & Garden", "Sports", "Beauty", "Toys", "Food"]
product_data = [
    # Electronics (higher prices)
    ("Gaming Laptop", "Electronics", 1299.99),
    ("Wireless Headphones", "Electronics", 199.99),
    ("Smartphone", "Electronics", 899.99),
    
    # Clothing (moderate prices)
    ("Designer Jeans", "Clothing", 89.99),
    ("Cotton T-Shirt", "Clothing", 24.99),
    ("Winter Jacket", "Clothing", 149.99),
    
    # Books (low prices)
    ("Python Programming Guide", "Books", 39.99),
    ("Mystery Novel", "Books", 14.99),
    
    # Home & Garden
    ("Coffee Maker", "Home & Garden", 79.99),
    ("Garden Tools Set", "Home & Garden", 45.99),
    
    # Sports
    ("Running Shoes", "Sports", 129.99),
    ("Yoga Mat", "Sports", 34.99),
    
    # Beauty
    ("Skincare Set", "Beauty", 89.99),
    ("Perfume", "Beauty", 65.99),
    
    # Toys
    ("LEGO Building Set", "Toys", 59.99),
    
    # Food
    ("Gourmet Coffee Beans", "Food", 29.99),
    ("Organic Honey", "Food", 18.99),
    
    # Edge cases for testing
    ("Clearance Item", "Clothing", 0.99),  # Very low price
    ("Luxury Watch", "Electronics", 2999.99),  # Very high price
    ("Free Sample", "Beauty", 0.00),  # Zero price for testing
]

products = []
for i, (name, category, base_price) in enumerate(product_data, 1):
    stock = random.randint(10, 200) if base_price > 0 else 5  # Limited stock for free items
    products.append((i, name, category, base_price, stock))

cursor.executemany("INSERT INTO products VALUES (?, ?, ?, ?, ?);", products)

print("🛒 Generating realistic order history...")

# Enhanced order generation with seasonal bias and realistic patterns
order_statuses = ['completed', 'refunded', 'cancelled', 'pending']
status_weights = [85, 8, 5, 2]  # Most orders completed, some refunds/cancellations

orders = []
order_id = 1

# Generate orders with seasonal bias (more recent orders)
for month_offset in range(6):  # Last 6 months
    # More orders in recent months
    orders_this_month = random.randint(150 - month_offset * 20, 200 - month_offset * 30)
    
    for _ in range(orders_this_month):
        # Customer selection (VIP customers order more frequently)
        customer_id = random.randint(1, 50)
        customer_type = customers[customer_id - 1][4]
        
        # Product selection influenced by customer type
        if customer_type == 'vip':
            # VIP customers prefer higher-end products
            product_id = random.choices(range(1, len(products) + 1), 
                                      weights=[p[3] for p in products])[0]  # Weight by price
        else:
            product_id = random.randint(1, len(products))
        
        # Quantity based on product price and customer type
        base_price = products[product_id - 1][3]
        if base_price > 500:  # Expensive items
            quantity = random.choices([1, 2], weights=[80, 20])[0]
        elif base_price == 0:  # Free items
            quantity = random.randint(1, 3)
        else:
            quantity = random.randint(1, 5)
        
        # Price variation (discounts, markups)
        price_variation = random.uniform(0.8, 1.2)  # ±20% variation
        if customer_type == 'vip':
            price_variation *= 0.9  # VIP discount
        price = round(base_price * price_variation, 2)
        
        # Date generation with bias toward recent months
        start_date = datetime.now() - timedelta(days=30 * (month_offset + 1))
        end_date = datetime.now() - timedelta(days=30 * month_offset)
        order_date = fake.date_between(start_date=start_date, end_date=end_date)
        
        # Status selection
        status = random.choices(order_statuses, weights=status_weights)[0]
        
        # Edge case: refunded orders have 0 effective price in some systems
        if status == 'refunded' and random.random() < 0.3:
            price = 0.00
        
        orders.append((order_id, customer_id, product_id, quantity, price, 
                      order_date.strftime('%Y-%m-%d'), status))
        order_id += 1

# Add some edge cases for testing
edge_cases = [
    # Large bulk order
    (order_id, 1, 1, 100, 1199.99, '2024-12-01', 'completed'),
    (order_id + 1, 2, len(products), 0, 0.00, '2024-11-15', 'cancelled'),  # Zero quantity
    (order_id + 2, 3, 5, 1, -10.00, '2024-10-20', 'refunded'),  # Negative price (refund)
]

orders.extend(edge_cases)

cursor.executemany("INSERT INTO orders VALUES (?, ?, ?, ?, ?, ?, ?);", orders)

print("📈 Generating summary statistics...")

# Generate summary
cursor.execute("SELECT COUNT(*) FROM customers")
customer_count = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM products")
product_count = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM orders")
order_count = cursor.fetchone()[0]

cursor.execute("SELECT SUM(quantity * price) FROM orders WHERE status = 'completed'")
total_revenue = cursor.fetchone()[0] or 0

cursor.execute("SELECT COUNT(DISTINCT customer_id) FROM orders")
active_customers = cursor.fetchone()[0]

# Commit and close
conn.commit()
conn.close()

print("\n✅ Enhanced database created successfully!")
print(f"📊 Database Statistics:")
print(f"   • {customer_count} customers")
print(f"   • {product_count} products across {len(set(p[2] for p in product_data))} categories")
print(f"   • {order_count} orders")
print(f"   • ${total_revenue:,.2f} total revenue")
print(f"   • {active_customers} active customers")
print(f"\n🎯 Enhanced Features Added:")
print(f"   ✅ Customer table with customer types (regular, premium, VIP)")
print(f"   ✅ Seasonal bias (more recent orders)")
print(f"   ✅ High price variance (${min(p[3] for p in product_data):.2f} - ${max(p[3] for p in product_data):.2f})")
print(f"   ✅ Edge cases (zero prices, large quantities, refunds)")
print(f"   ✅ Order status tracking (completed, refunded, cancelled)")
print(f"   ✅ Realistic customer behavior patterns")

print(f"\n🚀 Ready for advanced queries like:")
print(f"   • 'Who are our top 5 customers by revenue?'")
print(f"   • 'What's the refund rate by product category?'")
print(f"   • 'Show seasonal sales trends'")
print(f"   • 'Which VIP customers haven't ordered recently?'")
