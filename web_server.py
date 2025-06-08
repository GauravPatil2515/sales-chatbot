#!/usr/bin/env python3
"""
Sales Chatbot Web Server
A Flask web server that provides REST API endpoints for the web UI
"""

from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import sqlite3
import os
import json
import time
from datetime import datetime
from tabulate import tabulate

# Import functions from chat_bot module
from chat_bot import execute_query
from llm.llm_interface import get_sql_from_query

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

class SalesChatBot:
    """Class wrapper for the sales chatbot functionality"""
    def __init__(self):
        # Load environment variables from .env file
        import dotenv
        dotenv.load_dotenv()
        
        # Check if API key is available
        if not os.environ.get('GROQ_API_KEY'):
            print("❌ Warning: GROQ_API_KEY not found in environment variables. Please check your .env file.")
    
    def process_query(self, user_input):
        """Process a natural language query and return structured results"""
        start_time = time.time()
        
        try:
            print(f"Processing query: {user_input}")
            
            # Generate SQL query
            sql = get_sql_from_query(user_input)
            print(f"Generated SQL: {sql}")

            # Execute query
            headers, results = execute_query(sql)
            
            execution_time = round(time.time() - start_time, 2)

            if isinstance(results, str):  # It's an error message
                return {
                    'success': False,
                    'error': results,
                    'sql_query': sql,
                    'execution_time': execution_time
                }
            
            # Convert results to list of dictionaries for JSON serialization
            sql_result = []
            if headers and results:
                sql_result = [dict(zip(headers, row)) for row in results]
            
            # Generate natural language response
            response = self._generate_response(user_input, sql_result, headers)
            
            return {
                'success': True,
                'response': response,
                'sql_query': sql,
                'sql_result': sql_result,
                'execution_time': execution_time
            }

        except Exception as e:
            execution_time = round(time.time() - start_time, 2)
            error_msg = f"Error processing query: {str(e)}"
            print(error_msg)
            return {
                'success': False,
                'error': error_msg,
                'execution_time': execution_time
            }
    
    def _generate_response(self, query, results, headers):
        """Generate a natural language response based on query results"""
        if not results:
            return "No results found for your query. The data might not exist or the query needs adjustment."
        
        result_count = len(results)
        
        # Basic response generation based on query patterns
        query_lower = query.lower()
        
        if "total" in query_lower and "revenue" in query_lower:
            if results and 'total_amount' in results[0]:
                total = sum(float(r.get('total_amount', 0)) for r in results)
                return f"The total revenue is ${total:,.2f} based on {result_count} record(s)."
            elif results and len(results[0]) == 1:
                # Single value result
                value = list(results[0].values())[0]
                return f"The total revenue is ${float(value):,.2f}."
        
        elif "count" in query_lower or "how many" in query_lower:
            if result_count == 1 and len(results[0]) == 1:
                count = list(results[0].values())[0]
                return f"Found {count} matching records."
            else:
                return f"Found {result_count} records matching your criteria."
        
        elif "top" in query_lower or "best" in query_lower:
            return f"Here are the top {result_count} results based on your query criteria."
        
        else:
            return f"Query executed successfully and returned {result_count} result(s). The data is displayed in the table above."

# Initialize chatbot (will be set when server starts)
chatbot = None

def initialize_chatbot():
    """Initialize chatbot with proper error handling"""
    global chatbot
    if not chatbot:
        chatbot = SalesChatBot()

def get_db_connection():
    """Get database connection"""
    db_path = os.path.join('data', 'sales.db')
    return sqlite3.connect(db_path)

@app.route('/')
def index():
    """Serve the main web UI"""
    try:
        with open('web_ui_integrated.html', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        # Fallback to the regular web_ui file
        with open('web_ui.html', 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error loading UI: {str(e)}"

@app.route('/test')
def test_ui():
    """Serve the test UI for debugging"""
    try:
        with open('test_ui.html', 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error loading test UI: {str(e)}"

@app.route('/api/query', methods=['POST'])
def process_query():
    """Process a natural language query"""
    try:
        # Initialize chatbot if not already done
        if not chatbot:
            initialize_chatbot()
            
        data = request.get_json()
        query = data.get('query', '').strip()
        
        if not query:
            return jsonify({
                'success': False,
                'error': 'Query is required',
                'status': 'error'
            }), 400
        
        # Process the query with chatbot
        result = chatbot.process_query(query)
        
        if not result['success']:
            return jsonify({
                'success': False,
                'error': result.get('error', 'Unknown error'),
                'status': 'error',
                'sql_query': result.get('sql_query', ''),
                'execution_time': result.get('execution_time', 0)
            }), 500        # Generate HTML table if SQL result exists
        html_output = ""
        if result.get('sql_result'):
            try:
                html_output = generate_html_table(result['sql_result'], result.get('sql_query', ''))
            except Exception as e:
                html_output = f"<div class='text-red-600'>Error generating table: {str(e)}</div>"
        
        return jsonify({
            'success': True,
            'status': 'success',
            'response': result.get('response', 'Query executed successfully'),
            'sql_query': result.get('sql_query', ''),
            'html_output': html_output,
            'html_table': html_output,  # Keep backward compatibility
            'results': result.get('sql_result', []),
            'execution_time': result.get('execution_time', 0),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get database statistics"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get basic counts
        cursor.execute("SELECT COUNT(*) FROM customers")
        customer_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM products")
        product_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM orders")
        order_count = cursor.fetchone()[0]
          # Get revenue stats
        cursor.execute("SELECT SUM(price * quantity) FROM orders WHERE status = 'completed'")
        total_revenue = cursor.fetchone()[0] or 0
        
        # Get customer type breakdown
        cursor.execute("""
            SELECT customer_type, COUNT(*) as count, 
                   COALESCE(SUM(o.price * o.quantity), 0) as revenue
            FROM customers c
            LEFT JOIN orders o ON c.customer_id = o.customer_id 
            WHERE o.status = 'completed' OR o.status IS NULL
            GROUP BY customer_type
        """)
        customer_breakdown = cursor.fetchall()
        
        conn.close()
        
        return jsonify({
            'status': 'success',
            'stats': {
                'customers': customer_count,
                'products': product_count,
                'orders': order_count,
                'total_revenue': total_revenue,
                'customer_breakdown': [
                    {
                        'type': row[0],
                        'count': row[1],
                        'revenue': row[2]
                    } for row in customer_breakdown
                ]
            }
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/api/examples', methods=['GET'])
def get_examples():
    """Get example queries"""
    examples = [
        "How many VIP customers do we have?",
        "What is the total revenue from completed orders?",
        "Show me the top 3 products by sales",
        "What is the average order value?",
        "How many orders were placed last month?",
        "Which customer type generates the most revenue?",
        "Show all customers",
        "Show all products",
        "Show all orders"
    ]
    
    return jsonify({
        'status': 'success',
        'examples': examples
    })

@app.route('/api/database', methods=['GET'])
def get_database_contents():
    """Get complete database contents"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get customers
        cursor.execute("SELECT * FROM customers ORDER BY customer_id")
        customers = cursor.fetchall()
        cursor.execute("PRAGMA table_info(customers)")
        customer_columns = [col[1] for col in cursor.fetchall()]
        
        # Get products
        cursor.execute("SELECT * FROM products ORDER BY product_id")
        products = cursor.fetchall()
        cursor.execute("PRAGMA table_info(products)")
        product_columns = [col[1] for col in cursor.fetchall()]
        
        # Get orders
        cursor.execute("SELECT * FROM orders ORDER BY order_date DESC")
        orders = cursor.fetchall()
        cursor.execute("PRAGMA table_info(orders)")
        order_columns = [col[1] for col in cursor.fetchall()]
        
        conn.close()
        
        # Convert to dictionaries
        customers_data = [dict(zip(customer_columns, row)) for row in customers]
        products_data = [dict(zip(product_columns, row)) for row in products]
        orders_data = [dict(zip(order_columns, row)) for row in orders]
        
        return jsonify({
            'status': 'success',
            'data': {
                'customers': {
                    'columns': customer_columns,
                    'data': customers_data,
                    'count': len(customers_data)
                },
                'products': {
                    'columns': product_columns,
                    'data': products_data,
                    'count': len(products_data)
                },
                'orders': {
                    'columns': order_columns,
                    'data': orders_data,
                    'count': len(orders_data)
                }
            }
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

def generate_html_table(data, sql_query):
    """Generate HTML table from SQL results"""
    if not data:
        return "<div class='text-gray-500 text-center py-8'>No results found</div>"
    
    # Extract headers and rows
    headers = list(data[0].keys()) if isinstance(data[0], dict) else []
    
    if not headers:
        # Handle tuple/list format
        headers = [f"Column_{i+1}" for i in range(len(data[0]))]
        rows = data
    else:
        # Handle dict format
        rows = [[row[col] for col in headers] for row in data]
    
    # Generate HTML table
    html = '<div class="overflow-x-auto">'
    html += '<table class="min-w-full divide-y divide-gray-200">'
    
    # Headers
    html += '<thead class="bg-gray-50">'
    html += '<tr>'
    for header in headers:
        html += f'<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">{header}</th>'
    html += '</tr>'
    html += '</thead>'
    
    # Body
    html += '<tbody class="bg-white divide-y divide-gray-200">'
    for row in rows:
        html += '<tr>'
        for cell in row:
            # Format cell value
            if isinstance(cell, float):
                if cell > 1000:
                    formatted_cell = f"${cell:,.2f}"
                else:
                    formatted_cell = f"{cell:.2f}"
            elif isinstance(cell, int) and cell > 1000:
                formatted_cell = f"{cell:,}"
            else:
                formatted_cell = str(cell)
            
            html += f'<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{formatted_cell}</td>'
        html += '</tr>'
    html += '</tbody>'
    html += '</table>'
    html += '</div>'
    
    return html

if __name__ == '__main__':
    print("🚀 Starting Sales Chatbot Web Server...")
    print("📱 Web UI will be available at: http://localhost:5000")
    print("🔌 API endpoints available at: http://localhost:5000/api/")
    print("⚡ Press Ctrl+C to stop the server")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
