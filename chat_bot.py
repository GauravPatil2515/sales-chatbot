# Sales Chatbot - Phase 3: Complete Interactive Chatbot
# Integrates database + LLM for natural language sales queries

import sqlite3
import os
from tabulate import tabulate
from llm.llm_interface import get_sql_from_query

DB_PATH = "data/sales.db"

def execute_query(sql: str):
    """Execute SQL query on the sales database and return formatted results."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        headers = [desc[0] for desc in cursor.description] if cursor.description else []
        conn.close()
        return headers, rows
    except Exception as e:
        return [], f"❌ SQL Error: {e}"

def display_welcome():
    """Display welcome message and available sample questions."""
    print("🧠 Sales Analysis Assistant")
    print("=" * 50)
    print("Ask me anything about your sales data!")
    print("\n💡 Try these sample questions:")
    print("• What is the total revenue in May?")
    print("• Top 3 products by quantity sold?")
    print("• How many orders were placed last month?")
    print("• Which product had the highest revenue?")
    print("• Show me all Electronics products")
    print("• What's the average order value?")
    print("\n📝 Type 'exit' or 'quit' to stop")
    print("=" * 50)

def process_query(user_input: str):
    """Process a single user query and return the result."""
    try:
        # Use the API key from environment variable
        api_key = os.getenv('GROQ_API_KEY')
        if not api_key:
            return False, "❌ Error: GROQ_API_KEY not set. Please set your API key first."
        
        print(f"Processing query: {user_input}")
        
        try:
            print("💡 Generating SQL query...")
            sql = get_sql_from_query(user_input)
            print(f"📄 Generated SQL: {sql}")
        except Exception as e:
            error_msg = f"❌ LLM Error: {str(e)}"
            print(error_msg)
            return False, error_msg

        print("📊 Executing query...")
        headers, results = execute_query(sql)

        if isinstance(results, str):  # It's an error message
            print(f"❌ Error: {results}")
            return False, results
        elif results:
            print(f"\n✅ Found {len(results)} result(s):")
            print(tabulate(results, headers=headers, tablefmt="grid"))
            return True, {"headers": headers, "results": results}
        else:
            print("✅ Query executed successfully, but returned no results.")
            return True, {"headers": headers, "results": []}

    except Exception as e:
        error_msg = f"❌ Error: {e}"
        print(error_msg)
        return False, error_msg

def run_chatbot():
    """Main chatbot loop."""
    # Load API key from .env file
    from dotenv import load_dotenv
    load_dotenv()
    
    # Check if API key is available
    if not os.getenv('GROQ_API_KEY'):
        print("❌ Error: GROQ_API_KEY not set in .env file. Please check your environment setup.")
        return
    
    display_welcome()
    
    while True:
        try:
            user_input = input("\n🤖 > ").strip()

            if user_input.lower() in ['exit', 'quit', 'bye']:
                print("👋 Goodbye! Thanks for using Sales Analysis Assistant!")
                break
            
            if not user_input:
                print("Please enter a question about your sales data.")
                continue

            print("💡 Generating SQL query...")
            sql = get_sql_from_query(user_input)
            print(f"📄 Generated SQL: {sql}")

            print("📊 Executing query...")
            headers, results = execute_query(sql)

            if isinstance(results, str):  # It's an error message
                print(results)
                print("💡 Tip: Try rephrasing your question or check if the data exists.")
            elif results:
                print(f"\n✅ Found {len(results)} result(s):")
                print(tabulate(results, headers=headers, tablefmt="grid"))
            else:
                print("✅ Query executed successfully, but returned no results.")
                print("💡 This might mean the data doesn't exist or the query needs adjustment.")

        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            print("💡 Try asking a different question or check your internet connection.")

if __name__ == "__main__":
    run_chatbot()
