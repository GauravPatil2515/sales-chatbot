#!/usr/bin/env python3
"""
Project Setup Script
Sets up the sales chatbot project by installing dependencies and creating the database
"""

import os
import sys
import subprocess

def install_dependencies():
    """Install required Python packages."""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def setup_database():
    """Create and populate the database."""
    print("🗄️  Setting up database...")
    try:
        # Import and run database setup
        sys.path.append(os.path.join(os.path.dirname(__file__), 'data'))
        from setup_database import main as setup_db
        setup_db()
        print("✅ Database created and populated successfully!")
        return True
    except Exception as e:
        print(f"❌ Failed to setup database: {e}")
        return False

def check_api_key():
    """Check if API key is configured."""
    api_key = os.getenv('GROQ_API_KEY')
    if api_key:
        print("✅ GROQ_API_KEY is configured")
        return True
    else:
        print("⚠️  GROQ_API_KEY not found")
        print("   Please set your API key:")
        print("   $env:GROQ_API_KEY='your-api-key-here'")
        return False

def main():
    """Main setup function."""
    print("🚀 Sales Chatbot Project Setup")
    print("=" * 50)
    
    success_count = 0
    
    # Step 1: Install dependencies
    if install_dependencies():
        success_count += 1
    
    # Step 2: Setup database
    if setup_database():
        success_count += 1
    
    # Step 3: Check API key
    if check_api_key():
        success_count += 1
    
    # Summary
    print(f"\n🎯 Setup Summary")
    print("=" * 30)
    print(f"Completed steps: {success_count}/3")
    
    if success_count == 3:
        print("🎉 Project setup complete!")
        print("\nNext steps:")
        print("1. Run 'python demo.py' to see the chatbot in action")
        print("2. Run 'python chat_bot.py' for interactive mode")
    else:
        print("⚠️  Setup incomplete. Please check the errors above.")

if __name__ == "__main__":
    main()
