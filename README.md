# AI Data Analyst

An intelligent data analysis tool powered by Groq AI that converts natural language questions into SQL queries, executes them against your data, and displays results—all with a simple web interface.

## Introduction

AI Data Analyst is a Streamlit-based application that bridges the gap between non-technical users and data analysis. Instead of writing SQL queries manually, simply ask questions in plain English about your dataset, and the AI will generate and execute the appropriate SQL query using the power of Groq's LLM models.

This tool is perfect for:
- Data exploration without SQL knowledge
- Quick analysis of CSV and Excel files
- Business intelligence reporting
- Interactive data investigation

## Features

- **📤 Easy File Upload**: Upload CSV or Excel files (`.csv`, `.xlsx`, `.xls`)
- **📊 Data Preview**: View dataset structure, column information, and sample rows
- **🤖 AI-Powered SQL Generation**: Ask questions in natural language, AI generates SQL automatically
- **⚡ Instant Execution**: Run generated queries against your data with DuckDB
- **💾 Download Results**: Export analysis results as CSV files
- **🔒 API Key Management**: Manage Groq API keys securely in the app sidebar (optional local storage)
- **🔄 Fallback Models**: Automatic fallback to alternative models if primary model unavailable
- **📈 Session State**: Persistent data and UI state during your session

## Prerequisites

Before running the application, ensure you have:
- Python 3.8 or higher
- A Groq API key (get one at [console.groq.com](https://console.groq.com))
- pip or your preferred Python package manager

## Installation

1. **Clone the project**:
   ```bash
   git clone https://github.com/omkargutal/AI-Agent_Data-Analysis
   cd AI-Agent_Data-Analysis
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your Groq API key**:
   - Create a `.env` file in the project root:
     ```
     GROQ_API_KEY=your_api_key_here
     ```
   - Or configure it in the app sidebar when running

## How to Run

1. **Activate your virtual environment** (if you created one):
   ```bash
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Run the Streamlit app**:
   ```bash
   streamlit run ai_data_analyst.py
   ```

3. **Access the app**: Open your browser and navigate to `http://localhost:8501`

## Usage

### Basic Workflow

1. **Upload Your Data**
   - Click "Upload Dataset" and select a CSV or Excel file
   - Wait for confirmation that the file is loaded

2. **Explore Your Data** (Optional)
   - Click "📊 Display Data Sample" to view:
     - Total rows and columns
     - Column names and data types
     - Null value counts
     - Top 10 rows of data

3. **Ask Questions**
   - Type your question in natural language
   - Example questions:
     - "How many records are there?"
     - "What is the average salary by department?"
     - "Show me the top 5 products by sales"
     - "Get all customers from New York"

4. **View & Download Results**
   - Review the generated SQL query
   - See execution results in a table
   - Download results as CSV using the "📥 Download Results as CSV" button

### Advanced Options

- **Get SQL Query Only**: Check this option to see just the generated SQL without executing it. Useful for learning SQL or reviewing queries before execution.

## Configuration

### API Key Management

**Option 1: Using .env file (Persistent)**
- Create a `.env` file in the project root
- Add your key: `GROQ_API_KEY=your_key_here`
- The app will automatically load this on startup

**Option 2: Via Sidebar (Session Only)**
- Paste your API key in the sidebar input field
- Optionally check "Save keys to local .env file" to persist it

### Supported Models

The application uses Groq's optimized models:
- Primary: `openai/gpt-oss-120b`
- Fallback: `meta-llama/llama-4-scout-17b-16e-instruct`

## Project Structure

```
├── ai_data_analyst.py      # Main Streamlit application
├── requirements.txt         # Python dependencies
├── .env                     # API keys (create this locally, don't commit)
└── README.md               # This file
```

## Dependencies

- **streamlit**: Web framework for the UI
- **pandas**: Data manipulation and analysis
- **duckdb**: SQL query execution engine
- **groq**: Groq API client
- **python-dotenv**: Environment variable management
- **watchdog**: File system monitoring (for Streamlit)

## Troubleshooting

### "GROQ_API_KEY not set" Error
- Ensure your API key is set in `.env` or the sidebar
- Check that the key is valid and hasn't expired
- Try setting it in the sidebar with "Apply keys"

### SQL Execution Errors
- Check the generated SQL in the "Generated SQL Query" section
- Ensure column names match exactly (case-sensitive)
- Review the sample data to verify data types
- Check error message for specific SQL syntax issues

### File Upload Issues
- Ensure file is less than Streamlit's upload limit (default 200MB)
- Check that CSV/Excel file is not corrupted
- Try opening the file locally first to verify data integrity

### Slow Query Execution
- Large datasets may take longer to process
- DuckDB is optimized but very large files (100MB+) may impact performance
- Consider filtering data before upload or using queries with LIMIT

## Limitations

- Maximum file upload size: 200MB (Streamlit default)
- SQL queries are executed against in-memory data using DuckDB
- Complex data transformations may need manual SQL refinement

## Tips & Best Practices

1. **Be specific** in your questions for better SQL generation
2. **Check the SQL** before running complex queries
3. **Start with data exploration** to understand your columns and data types
4. **Use "Get SQL Query Only"** to learn and verify generated SQL
5. **Download results** for further analysis in Excel or other tools

## License

This project is open source and available for personal and commercial use.

## Support

If you encounter issues:
1. Check the Troubleshooting section above
2. Verify your Groq API key is valid
3. Ensure all dependencies are installed correctly
4. Check that your data file is properly formatted

---

**Built with Streamlit, Groq AI, and DuckDB** 🚀
