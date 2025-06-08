import requests
import os
import dotenv

# Load environment variables from .env file
dotenv.load_dotenv()

def get_sql_from_query(user_query: str) -> str:
    """
    Uses Groq's DeepSeek model to convert a user question into SQL.
    
    Args:
        user_query (str): Natural language question from the user
        
    Returns:
        str: SQL query string
        
    Raises:
        Exception: If API call fails or API key is missing
    """
    # Check if API key is set
    api_key = os.getenv('GROQ_API_KEY')
    if not api_key:
        raise Exception("GROQ_API_KEY environment variable not set. Please set your Groq API key.")    # Enhanced schema prompt for Llama model with emphasis on complete table results
    prompt = f"""Generate only a SQL query for SQLite. No explanations.

Schema:
customers: customer_id (PK), name, email, join_date, customer_type ('regular', 'premium', 'vip')
products: product_id (PK), name, category, base_price, stock_level
orders: order_id (PK), customer_id (FK), product_id (FK), quantity, price, order_date (YYYY-MM-DD), status ('completed', 'refunded', 'cancelled', 'pending')

Important: When user asks to "show all" or requests complete data, return ALL rows without LIMIT.

Example queries:
- VIP customers: SELECT COUNT(*) FROM customers WHERE customer_type = 'vip'
- All customers: SELECT * FROM customers ORDER BY customer_id
- All products: SELECT * FROM products ORDER BY product_id
- All orders: SELECT * FROM orders ORDER BY order_date DESC
- Show customers: SELECT * FROM customers
- Show products: SELECT * FROM products
- Show orders: SELECT * FROM orders
- Completed orders revenue: SELECT SUM(price * quantity) FROM orders WHERE status = 'completed'
- Customer order info: SELECT c.name, o.* FROM customers c JOIN orders o ON c.customer_id = o.customer_id

Question: {user_query}
SQL:""".strip()

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.1,
        "max_tokens": 100
    }

    try:
        response = requests.post("https://api.groq.com/openai/v1/chat/completions", 
                               headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            sql_query = response.json()['choices'][0]['message']['content'].strip()
            
            # Clean up response - remove markdown and thinking sections
            sql_query = sql_query.replace('```sql', '').replace('```', '').strip()
            
            # Handle DeepSeek thinking format
            if '<think>' in sql_query:
                lines = sql_query.split('\n')
                cleaned_lines = []
                skip = False
                for line in lines:
                    if '<think>' in line:
                        skip = True
                    elif '</think>' in line:
                        skip = False
                    elif not skip and line.strip():
                        cleaned_lines.append(line.strip())
                sql_query = ' '.join(cleaned_lines)
            
            return ' '.join(sql_query.split())
        else:
            raise Exception(f"Groq API error: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        raise Exception(f"Network error: {str(e)}")
    except Exception as e:
        raise Exception(f"API error: {str(e)}")


def test_connection() -> bool:
    """Test if the Groq API connection works."""
    try:
        result = get_sql_from_query("Count products")
        return len(result) > 0 and 'SELECT' in result.upper()
    except:
        return False
