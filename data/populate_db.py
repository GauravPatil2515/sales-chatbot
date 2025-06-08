#!/usr/bin/env python3
"""
Basic Database Population Script
Creates and populates the sales database with sample data
"""

import sqlite3
import random
import os
from datetime import datetime, timedelta

def create_and_populate_database():
    """Create database and populate with sample data"""
    print("🔄 Creating sales database...")
    
    # Connect to SQLite database
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sales.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Drop existing tables
    cursor.execute("DROP TABLE IF EXISTS orders;")
    cursor.execute("DROP TABLE IF EXISTS products;")
    cursor.execute("DROP TABLE IF EXISTS customers;")
    
    # Create customers table
    cursor.execute("""
        CREATE TABLE customers (
            customer_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            join_date TEXT NOT NULL,
            customer_type TEXT NOT NULL DEFAULT 'regular'
        );
    """)
    
    # Create products table
    cursor.execute("""
        CREATE TABLE products (
            product_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            base_price REAL NOT NULL,
            stock_level INTEGER NOT NULL DEFAULT 100
        );
    """)
    
    # Create orders table
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
    
    print("✅ Database created successfully!")
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_and_populate_database()