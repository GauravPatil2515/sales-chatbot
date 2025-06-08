#!/usr/bin/env python3
"""
Setup Environment - For Sales Chatbot
Checks and sets up the environment for the Sales Chatbot application
"""

import os
import sys
import sqlite3
from pathlib import Path
import dotenv

def setup_environment():
    """Set up the environment for the Sales Chatbot."""
    print("\n🔧 Setting up environment for Sales Chatbot...")
    print("=" * 55)
    
    # Check if .env file exists
    env_file = Path('.env')
    if not env_file.exists():
        print("⚠️  No .env file found. Creating one...")
        api_key = input("Enter your Groq API key (or press Enter to skip): ").strip()
        
        with open('.env', 'w') as f:
            f.write(f"GROQ_API_KEY={api_key}")
        
        print("✅ Created .env file.")
    else:
        print("✅ .env file found.")
        
        # Load .env file to check for API key
        dotenv.load_dotenv()
        if not os.getenv('GROQ_API_KEY'):
            print("⚠️  No GROQ_API_KEY found in .env file.")
            api_key = input("Enter your Groq API key (or press Enter to skip): ").strip()
            
            if api_key:
                # Update existing .env file
                with open('.env', 'w') as f:
                    f.write(f"GROQ_API_KEY={api_key}")
                print("✅ Updated API key in .env file.")
        else:
            print("✅ API key found in .env file.")

    # Check database
    db_path = Path('data/sales.db')
    if not db_path.exists():
        print("⚠️  Database not found. Setting up database...")
        try:
            from data.setup_database import setup_database
            setup_database()
            print("✅ Database setup complete.")
        except Exception as e:
            print(f"❌ Error setting up database: {e}")
    else:
        print("✅ Database found.")

    print("\n✅ Environment setup complete!")
    print("=" * 55)

if __name__ == "__main__":
    setup_environment()
