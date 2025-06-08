# AI-Powered Sales Chatbot

An intelligent sales chatbot that uses natural language processing to query a sales database. The system leverages Groq's LLM API to convert natural language queries into SQL and execute them against a SQLite database containing customers, products, and orders data.

## 🚀 Features

- **Natural Language Queries**: Ask questions in plain English about sales data
- **AI-Powered SQL Generation**: Converts natural language to SQL using Groq's LLM
- **Dual Interface**: Command-line interface and web-based UI
- **Real-time Database Queries**: Instant responses with actual data
- **Comprehensive Sales Data**: 50+ customers, 20+ products, 700+ orders
- **RESTful API**: Web server with API endpoints for integration

## 🛠️ Technology Stack

- **Backend**: Python 3.8+
- **AI/LLM**: Groq API with Llama models
- **Database**: SQLite with realistic sales data
- **Web Framework**: Flask
- **Frontend**: HTML/CSS/JavaScript
- **Environment Management**: python-dotenv

## 📋 Prerequisites

- Python 3.8 or higher
- Groq API key (free tier available)
- Internet connection for LLM API calls

## 🔧 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/GauravPatil2515/sales-chatbot.git
   cd sales-chatbot
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   - Copy `.env.example` to `.env` (if provided) or create a new `.env` file
   - Add your Groq API key:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```

5. **Initialize the database** (if needed)
   ```bash
   python data/setup_database.py
   ```

## 🚀 Quick Start

### Command Line Interface

Run the main chatbot:
```bash
python main.py
```

### Web Interface

1. Start the web server:
   ```bash
   python web_server.py
   ```

2. Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

### Demo Script

Run the comprehensive demo to see 7 example queries:
```bash
python comprehensive_demo.py
```

This demo will show:
- "Which product had the highest revenue last week?"
- "Show me the top 5 customers by total spending"
- "What are the total sales for each product category?"
- "How many orders were placed in the last 30 days?"
- "Which customers from California have made purchases?"
- "Show me products with stock less than 10 units"
- "What's the average order value for each month?"

## 💬 Example Queries

Try asking these natural language questions:

- "Show me all customers from New York"
- "What are the top 5 best-selling products?"
- "How many orders were placed in 2024?"
- "Which customer has spent the most money?"
- "Show me products with price above $500"
- "What's the total revenue for this month?"

## 📊 Database Schema

The system includes a comprehensive sales database with:

### Tables:
- **Customers**: Customer information (ID, name, email, city, state)
- **Products**: Product catalog (ID, name, category, price, stock)
- **Orders**: Order records (ID, customer, product, quantity, date, total)

### Sample Data:
- 50+ customers across multiple states
- 20+ products in various categories
- 700+ orders with realistic transaction data

## 🌐 API Endpoints

When running the web server, the following endpoints are available:

- `GET /` - Web UI interface
- `GET /api/stats` - Database statistics
- `GET /api/database` - Database contents
- `POST /api/query` - Natural language query processing

## 🔍 Project Structure

```
sales-chatbot/
├── data/
│   ├── sales.db              # SQLite database
│   └── setup_database.py     # Database initialization
├── llm/
│   ├── __init__.py
│   └── llm_interface.py      # LLM integration
├── chat_bot.py               # Main chatbot logic
├── demo.py                   # Demo script
├── main.py                   # CLI entry point
├── web_server.py             # Flask web server
├── web_ui_integrated.html    # Web interface
├── setup.py                  # Project setup
├── setup_environment.py     # Environment setup
├── requirements.txt          # Dependencies
├── .env                      # Environment variables
├── .gitignore               # Git ignore rules
└── README.md                # This file
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_groq_api_key_here
DATABASE_PATH=data/sales.db
HOST=0.0.0.0
PORT=5000
DEBUG=True
```

### API Configuration

The system uses Groq's LLM API. You can get a free API key from [Groq Console](https://console.groq.com/).

## 🧪 Testing

### Validate Installation

Run the validation script to ensure everything is set up correctly:
```bash
python final_validation.py
```

### View Database Contents

Explore the database structure and data:
```bash
python show_complete_db.py
```

## 🐛 Troubleshooting

### Common Issues

1. **API Key Error**: Ensure your Groq API key is correctly set in the `.env` file
2. **Database Not Found**: Run `python data/setup_database.py` to initialize the database
3. **Port Already in Use**: Change the port in `web_server.py` or kill the process using port 5000
4. **Import Errors**: Ensure all dependencies are installed with `pip install -r requirements.txt`

### Debug Mode

Enable debug mode by setting `DEBUG=True` in your `.env` file for detailed error messages.

## 📈 Future Enhancements

- [ ] User authentication and session management
- [ ] Query history and favorites
- [ ] Export results to CSV/PDF
- [ ] Real-time dashboard with charts
- [ ] Integration with external CRM systems
- [ ] Voice interface support
- [ ] Mobile-responsive design improvements

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Gaurav Patil** - *Initial work* - [GauravPatil2515](https://github.com/GauravPatil2515)

## 🙏 Acknowledgments

- [Groq](https://groq.com/) for providing the LLM API
- [Flask](https://flask.palletsprojects.com/) for the web framework
- [SQLite](https://www.sqlite.org/) for the database engine

## 📞 Support

If you have any questions or run into issues, please:

1. Check the [Issues](https://github.com/GauravPatil2515/sales-chatbot/issues) page
2. Create a new issue with detailed information
3. Contact: [GauravPatil2515](https://github.com/GauravPatil2515)

---

⭐ **Star this repository if you found it helpful!**