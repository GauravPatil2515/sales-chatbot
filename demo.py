#!/usr/bin/env python3
"""
Sales Chatbot Demo
Simple demo script for the main application
"""

import os
from chat_bot import process_query

def run_demo():
    """Run a simple demo of the chatbot"""
    print("🚀 Sales Chatbot Demo")
    print("=" * 50)
    
    # Check API key
    if not os.getenv('GROQ_API_KEY'):
        print("❌ GROQ_API_KEY not set. Please set your API key first.")
        return
    
    # Demo queries
    queries = [
        "How many customers do we have?",
        "What is our total revenue?",
        "Show top 3 products by sales"
    ]
    
    successful = 0
    for i, query in enumerate(queries, 1):
        print(f"\n{i}. Testing: {query}")
        try:
            success, result = process_query(query)
            if success:
                print("✅ Success")
                successful += 1
            else:
                print(f"❌ Failed: {result}")
        except Exception as e:
            print(f"❌ Error: {str(e)}")
    
    print(f"\n🎯 Demo completed: {successful}/{len(queries)} queries successful")

if __name__ == "__main__":
    run_demo()
