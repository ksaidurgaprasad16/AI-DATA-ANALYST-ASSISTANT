# =========================================================
# SQL ANALYTICS - SHARED UTILITIES
# =========================================================

import requests
import streamlit as st

# =========================================================
# AI FUNCTION
# =========================================================

def ask_ai(prompt, api_key):

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "openrouter/free",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    try:

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=60
        )

        result = response.json()

        if "choices" in result:
            return result["choices"][0]["message"]["content"]

        return str(result)

    except Exception as e:
        return str(e)

# =========================================================
# DB CONNECTION STRING HELPER
# =========================================================

def get_connection_string(
    db_type, host, port, user, password, database
):

    if db_type == "MySQL":
        return (
            f"mysql+pymysql://{user}:{password}"
            f"@{host}:{port}/{database}"
        )

    elif db_type == "PostgreSQL":
        return (
            f"postgresql+psycopg2://{user}:{password}"
            f"@{host}:{port}/{database}"
        )

    elif db_type == "SQL Server":
        return (
            f"mssql+pyodbc://{user}:{password}"
            f"@{host}:{port}/{database}"
            f"?driver=ODBC+Driver+17+for+SQL+Server"
        )

    elif db_type == "SQLite":
        return f"sqlite:///{database}"

    elif db_type == "Snowflake":
        return f"snowflake://{user}:{password}@{host}/{database}"

    elif db_type == "BigQuery":
        return f"bigquery://{database}"

    return None

# =========================================================
# SESSION STATE INITIALIZER
# =========================================================

def init_sql_session_state():

    defaults = {
        "sql_engine": None,
        "sql_tables": [],
        "sql_query_result": None,
        "sql_ai_response": "",
        "sql_chat_history": [],
        "sql_generated_query": "",
        "pdf_sections": []
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value