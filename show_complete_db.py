#!/usr/bin/env python3
"""
Database Viewer
Shows complete database contents for the Sales Chatbot
"""

import sqlite3
from tabulate import tabulate

def show_database_contents():
    """Display all database contents in a formatted way"""
    DB_PATH = "data/sales.db"
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        print("📊 Database Contents")
        print("=" * 60)
        
        # Show customers
        print("\n👥 CUSTOMERS")
        print("-" * 40)
        cursor.execute("SELECT * FROM customers LIMIT 10")
        customers = cursor.fetchall()
        cursor.execute("PRAGMA table_info(customers)")
        columns = [col[1] for col in cursor.fetchall()]
        print(tabulate(customers, headers=columns, tablefmt="grid"))
        
        # Show customer stats
        cursor.execute("SELECT customer_type, COUNT(*) as count FROM customers GROUP BY customer_type")
        stats = cursor.fetchall()
        print(f"\nCustomer Types: {dict(stats)}")
        
        # Show products
        print("\n🛍️  PRODUCTS")
        print("-" * 40)
        cursor.execute("SELECT * FROM products LIMIT 10")
        products = cursor.fetchall()
        cursor.execute("PRAGMA table_info(products)")
        columns = [col[1] for col in cursor.fetchall()]
        print(tabulate(products, headers=columns, tablefmt="grid"))
        
        # Show orders summary
        print("\n📦 ORDERS SUMMARY")
        print("-" * 40)
        cursor.execute("SELECT status, COUNT(*) as count, SUM(price * quantity) as revenue FROM orders GROUP BY status")
        order_stats = cursor.fetchall()
        print(tabulate(order_stats, headers=["Status", "Count", "Revenue"], tablefmt="grid"))
        
        # Show recent orders
        print("\n🕒 RECENT ORDERS (Latest 5)")
        print("-" * 40)
        cursor.execute("""
            SELECT o.order_id, c.name, p.name, o.quantity, o.price, o.order_date, o.status 
            FROM orders o 
            JOIN customers c ON o.customer_id = c.customer_id 
            JOIN products p ON o.product_id = p.product_id 
            ORDER BY o.order_date DESC 
            LIMIT 5
        """)
        recent_orders = cursor.fetchall()
        print(tabulate(recent_orders, 
                      headers=["Order ID", "Customer", "Product", "Qty", "Price", "Date", "Status"], 
                      tablefmt="grid"))
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error viewing database: {str(e)}")

def main():
    """Main entry point for database viewer"""
    show_database_contents()

if __name__ == "__main__":
    main()
