#!/usr/bin/env python3
"""
Sales Chatbot - Main Entry Point
A sophisticated sales analysis chatbot powered by AI
"""

import os
import sys

def show_menu():
    """Display the main menu options."""
    print("\n🧠 Sales Chatbot - AI-Powered Sales Analysis")
    print("=" * 55)
    print("Choose an option:")
    print("1. 🚀 Run Interactive Chatbot")
    print("2. 📊 Run Demo (Sample Queries)")
    print("3. 🌐 Start Web Server (Modern UI)")
    print("4. 🗄️  View Database Contents")
    print("5. ⚙️  Setup Project")
    print("6. 🔑 Setup Environment (.env file & API key)")
    print("7. ❌ Exit")
    print("-" * 55)

def main():
    """Main application entry point."""
    while True:
        show_menu()
        choice = input("Enter your choice (1-7): ").strip()
        
        if choice == "1":
            print("\n🚀 Starting interactive chatbot...")
            try:
                from chat_bot import run_chatbot
                run_chatbot()
            except ImportError as e:
                print(f"❌ Error importing chatbot: {e}")
            except Exception as e:
                print(f"❌ Error running chatbot: {e}")
        
        elif choice == "2":
            print("\n📊 Running demo...")
            try:
                from demo import run_demo
                run_demo()
            except ImportError as e:
                print(f"❌ Error importing demo: {e}")
            except Exception as e:
                print(f"❌ Error running demo: {e}")
        
        elif choice == "3":
            print("\n🌐 Starting web server...")
            print("📱 The web UI will be available at: http://localhost:5000")
            print("⚡ Press Ctrl+C to stop the server")
            try:
                from web_server import app
                app.run(debug=False, host='0.0.0.0', port=5000)
            except ImportError as e:
                print(f"❌ Error importing web server: {e}")
            except Exception as e:
                print(f"❌ Error starting web server: {e}")
        
        elif choice == "4":
            print("\n🗄️  Showing database contents...")
            try:
                from show_complete_db import main as show_db
                show_db()
            except ImportError as e:
                print(f"❌ Error importing database viewer: {e}")
            except Exception as e:
                print(f"❌ Error viewing database: {e}")
        
        elif choice == "5":
            print("\n⚙️  Running project setup...")
            try:
                from setup import main as setup_project
                setup_project()
            except ImportError as e:
                print(f"❌ Error importing setup: {e}")
            except Exception as e:
                print(f"❌ Error running setup: {e}")
        
        elif choice == "6":
            print("\n🔑 Setting up environment...")
            try:
                from setup_environment import setup_environment
                setup_environment()
            except ImportError as e:
                print(f"❌ Error importing environment setup: {e}")
            except Exception as e:
                print(f"❌ Error setting up environment: {e}")
        
        elif choice == "7":
            print("\n👋 Goodbye!")
            sys.exit(0)
        
        else:
            print("❌ Invalid choice. Please enter 1-7.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
