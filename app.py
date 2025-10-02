import streamlit as st
import sqlite3
import pandas as pd
import os
from dotenv import load_dotenv
import google.generativeai as genai
import tempfile

# ===Load environment variables ===
load_dotenv()

# === Configure Gemini API ===
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("models/gemini-2.5-pro")

# === Streamlit UI setup ===
st.set_page_config(page_title="🧠 Gemini NL → SQL", layout="centered")
st.title("🧠 Natural Language to SQL using Gemini")
st.markdown("Ask a question to query your **Orders**, **Customers**, **Claims** data or from your own file!")

# === File Upload ===
uploaded_file = st.file_uploader("📂 Upload a CSV or Excel file to query", type=["csv", "xlsx"])
uploaded_df = None
conn = None
temp_table_name = "uploaded_data"

# === Table selection ===
table_choice = st.selectbox("📋 Select a table to query", ["All", "orders", "customers", "claim", "Uploaded File" if uploaded_file else None])

# === Schema for Gemini context ===
# You can extend this to dynamically include uploaded schema later
schema_description = """
We have the following tables:

1. orders(order_id, customer_name, region, product, quantity, price)
2. customers(customer_id, customer_name, city, state, email)
3. claim(Facility_Name, Facility_ID, State, Period, Claim_Type,
AvgSpndgPerEP_Hospital, AvgSpndgPerEP_State, AvgSpndgPerEP_National,
PercentofSpndg_Hospital, PercentofSpndg_State, PercentofSpndg_National,
Start_Date, End_Date)

For 'orders', `price` is the total cost (already includes quantity).
"""

# === Load uploaded file into in-memory SQLite if present ===
if uploaded_file:
    try:
        file_ext = uploaded_file.name.split(".")[-1]
        if file_ext == "csv":
            uploaded_df = pd.read_csv(uploaded_file)
        elif file_ext == "xlsx":
            uploaded_df = pd.read_excel(uploaded_file)

        if uploaded_df is not None:
            # Create temp SQLite DB in memory
            conn = sqlite3.connect(":memory:")
            uploaded_df.to_sql(temp_table_name, conn, index=False, if_exists="replace")

            # Add schema description for Gemini
            schema_description += f"\n4. {temp_table_name}({', '.join(uploaded_df.columns)})"
            st.success(" Uploaded file processed and loaded into memory.")
    except Exception as e:
        st.error(f" Error loading file: {e}")

# === Get user question ===
user_question = st.text_input("🔍 Enter your question:")

# === Generate SQL query from user question ===
def generate_sql_from_question(question):
    prompt = f"""
You are a helpful assistant that writes SQL queries for a SQLite database.

{schema_description}

Translate the following natural language question into an SQLite SQL query:

Question: "{question}"
SQL Query:
    """
    response = model.generate_content(prompt)
    raw_sql = response.text.strip()

    # Clean up formatting
    if raw_sql.startswith("```"):
        raw_sql = raw_sql.strip("`")
        lines = raw_sql.splitlines()
        raw_sql = "\n".join(line for line in lines if not line.strip().lower().startswith("sql"))

    return raw_sql.strip()

# === Generate natural language answer from SQL result ===
def generate_answer_from_result(question, df):
    result_str = df.to_string(index=False)
    prompt = f"""
You are a data assistant. Based on the user's question and the SQL result, provide a short natural language answer.

Question: "{question}"

SQL Result:
{result_str}

Answer:
"""
    response = model.generate_content(prompt)
    return response.text.strip()

# ===  Process input and display output ===
if user_question:
    try:
        sql = generate_sql_from_question(user_question)
        st.subheader("🔧 Generated SQL Query")
        st.code(sql, language="sql")

        # Decide which DB to query: uploaded file or main DB
        if table_choice == "Uploaded File" and uploaded_file and conn:
            df = pd.read_sql_query(sql, conn)
        else:
            conn = sqlite3.connect("app.db")
            df = pd.read_sql_query(sql, conn)

        conn.close()

        st.success("✅ Query executed successfully!")
        st.subheader("📊 SQL Query Result")
        st.dataframe(df)

        if not df.empty:
            answer = generate_answer_from_result(user_question, df)
            st.subheader("🗣️ Answer in Natural Language")
            st.write(answer)
        else:
            st.warning("⚠️ No data returned by the query.")

    except Exception as e:
        st.error(f"❌ Error: {e}")
