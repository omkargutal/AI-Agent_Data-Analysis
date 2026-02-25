
import os
from pathlib import Path
import pandas as pd
import duckdb
import streamlit as st
from dotenv import load_dotenv
from groq import Groq
import io

# load .env in project root (do not override already-set environment variables)
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path, override=False)

def _get_env_key(name: str):
    """Return the value for `name` from session state (if present) or the environment.

    This lets the user paste a key into the left sidebar for the current session
    without persisting it to disk. Use `.env` or shell exports for permanent usage.
    """
    val = None
    try:
        val = st.session_state.get(name)
    except Exception:
        val = None
    return val or os.getenv(name)


# --- Left sidebar: allow manual entry of API keys ---
with st.sidebar:
    st.header("API Keys")
    groq_input = st.text_input("GROQ API Key", value=os.getenv("GROQ_API_KEY") or "", type="password")
    save_env = st.checkbox("Save keys to local .env file (overwrites existing)")
    if st.button("Apply keys"):
        if groq_input:
            st.session_state["GROQ_API_KEY"] = groq_input
            os.environ["GROQ_API_KEY"] = groq_input

        if save_env:
            try:
                # Read existing env values (if any) and update
                env_values = {}
                if env_path.exists():
                    for line in env_path.read_text().splitlines():
                        if "=" in line:
                            k, v = line.split("=", 1)
                            env_values[k] = v

                if groq_input:
                    env_values["GROQ_API_KEY"] = groq_input

                # Write back
                env_path.write_text("\n".join(f"{k}={v}" for k, v in env_values.items()))
                st.success("Saved keys to .env (local file)")
            except Exception as e:
                st.error(f"Failed to write .env: {e}")

    st.markdown("---")


GROQ_API_KEY = _get_env_key("GROQ_API_KEY")
if not GROQ_API_KEY:
    st.error(
        "GROQ_API_KEY not set. Add it to a local .env (ignored) or export it in your environment. See .env.example"
    )
    st.stop()

client = Groq(api_key=GROQ_API_KEY)


def call_groq_model(system, user_msg, model= "openai/gpt-oss-120b"):
    """Call Groq API with specified model"""
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": user_msg},
    ]
    try:
        resp = client.chat.completions.create(model=model, messages=messages)
        return resp.choices[0].message.content
    except Exception as e:
        # Fallback to alternative model if primary fails
        if "mixtral" in model.lower():
            try:
                resp = client.chat.completions.create(model="meta-llama/llama-4-scout-17b-16e-instruct", messages=messages)
                return resp.choices[0].message.content
            except:
                pass
        raise e


# Initialize session state
if "df" not in st.session_state:
    st.session_state.df = None
if "file_name" not in st.session_state:
    st.session_state.file_name = None
if "show_data_sample" not in st.session_state:
    st.session_state.show_data_sample = False

st.set_page_config(page_title="AI Data Analyst", layout="wide")
st.title("AI Data Analyst (Groq)")

# File upload section
st.subheader("Upload Dataset")
uploaded = st.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx", "xls"])

if uploaded:
    # Store file info
    st.session_state.file_name = uploaded.name
    
    # Read file based on type
    if uploaded.name.endswith('.csv'):
        st.session_state.df = pd.read_csv(uploaded)
    else:
        st.session_state.df = pd.read_excel(uploaded)
    
    st.success(f"✓ File loaded: {uploaded.name}")
    
    # Display data sample button
    if st.session_state.df is not None:
        def toggle_sample():
            st.session_state.show_data_sample = not st.session_state.show_data_sample
        
        st.button("📊 Display Data Sample", on_click=toggle_sample)
        
        # Show sample if toggle is active
        if st.session_state.show_data_sample:
            st.divider()
            st.subheader("Data Overview")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Rows", st.session_state.df.shape[0])
            with col2:
                st.metric("Total Columns", st.session_state.df.shape[1])
            with col3:
                st.metric("File Name", st.session_state.file_name)
            
            # Column info
            st.subheader("Column Information")
            col_info = pd.DataFrame({
                "Column Name": st.session_state.df.columns,
                "Data Type": st.session_state.df.dtypes.astype(str),
                "Non-Null Count": st.session_state.df.count(),
                "Null Count": st.session_state.df.isnull().sum()
            })
            st.dataframe(col_info, use_container_width=True)
            
            # Top 10 rows
            st.subheader("Top 10 Rows")
            st.dataframe(st.session_state.df.head(10), use_container_width=True)
            st.divider()

# Question section - only show if data is loaded
if st.session_state.df is not None:
    st.subheader("Ask Questions About Your Data")
    
    query = st.text_input(
        "Ask a question",
        placeholder="E.g., 'How many records are there?', 'Show me the average salary by department', 'Get the top 5 products by sales'"
    )
    
    col1, col2 = st.columns([3, 1])
    with col1:
        sql_only = st.checkbox("Get SQL Query Only", value=False)
    with col2:
        run = st.button("▶ Run Analysis", type="primary")
    
    if query and run:
        df = st.session_state.df
        duckdb.register("data_df", df)
        
        # Prompt for SQL generation
        system = (
            "You are an expert SQL analyst. Your task is to generate SQL queries for data analysis.\n"
            "Rules:\n"
            "1) Always return a valid SQL query enclosed in ```sql``` fences\n"
            "2) The table name is 'data_df'\n"
            "3) If the question cannot be answered with SQL, provide an EXPLANATION: prefix instead\n"
            "4) Never include markdown formatting in SQL blocks, just the pure SQL\n"
            "5) Optimize for clarity and correctness\n"
        )
        
        # Include schema info
        sample = df.head(10).to_csv(index=False)
        user_msg = (
            f"Dataset Info:\n"
            f"Columns: {', '.join(df.columns.tolist())}\n"
            f"Data Types: {', '.join([f'{col}({dtype})' for col, dtype in zip(df.columns, df.dtypes)])}\n\n"
            f"Sample Data:\n{sample}\n\n"
            f"User Question: {query}\n\n"
            f"Generate a SQL query or provide an explanation. Return in ```sql``` fences or start with EXPLANATION:"
        )
        
        try:
            with st.spinner("Generating SQL query..."):
                reply = call_groq_model(system, user_msg)
            
            # Display SQL
            st.subheader("Generated SQL Query")
            
            # Extract SQL
            sql = None
            if "```sql" in reply:
                start = reply.find("```sql") + len("```sql")
                end = reply.find("```", start)
                sql = reply[start:end].strip() if end != -1 else reply[start:].strip()
            elif "```SQL" in reply:
                start = reply.find("```SQL") + len("```SQL")
                end = reply.find("```", start)
                sql = reply[start:end].strip() if end != -1 else reply[start:].strip()
            elif reply.strip().startswith("SELECT"):
                sql = reply.strip()
            
            if reply.strip().startswith("EXPLANATION:"):
                st.info(reply)
            elif sql:
                st.code(sql, language="sql")
                
                if not sql_only:
                    # Execute SQL
                    try:
                        with st.spinner("Executing query..."):
                            res = duckdb.sql(sql).fetchdf()
                        st.subheader("Query Results")
                        st.dataframe(res, use_container_width=True)
                        
                        # Download option
                        csv_data = res.to_csv(index=False)
                        st.download_button(
                            label="📥 Download Results as CSV",
                            data=csv_data,
                            file_name="query_results.csv",
                            mime="text/csv"
                        )
                    except Exception as e:
                        st.error(f"❌ SQL Execution Error: {str(e)}")
                        st.info("**Raw Response from AI:**")
                        st.code(reply)
            else:
                st.warning("Could not extract SQL from response")
                st.info("**AI Response:**")
                st.code(reply)
        
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            st.info("Make sure your GROQ_API_KEY is valid and the model is available.")

else:
    st.info("👆 Please upload a CSV or Excel file to get started!")