# =========================================================
# SQL ANALYTICS - AI SQL GENERATOR
# =========================================================

import streamlit as st
import pandas as pd
import sqlalchemy

from modules.SQL_ANALYTICS.utils import ask_ai

# =========================================================
# DB TYPE SYNTAX RULES
# =========================================================

DB_SYNTAX_RULES = {
    "MySQL": """
- Use LOWER() for case-insensitive comparisons
- Use LIMIT for row limiting
- Use CONCAT() for string joining
- Use NOW() for current datetime
- Backtick column names if needed
""",
    "PostgreSQL": """
- Use ILIKE for case-insensitive comparisons
- Use LIMIT for row limiting
- Use || for string concatenation
- Use NOW() or CURRENT_TIMESTAMP for datetime
- Use COALESCE() for null handling
""",
    "SQL Server": """
- Use TOP instead of LIMIT (e.g. SELECT TOP 10)
- Use UPPER()/LOWER() for case comparisons
- Use + for string concatenation
- Use GETDATE() for current datetime
- Use ISNULL() for null handling
""",
    "SQLite": """
- Use LOWER() for case-insensitive comparisons
- Use LIMIT for row limiting
- Use || for string concatenation
- Use datetime('now') for current datetime
- No stored procedures supported
""",
    "Snowflake": """
- Use ILIKE for case-insensitive comparisons
- Use LIMIT for row limiting
- Use CONCAT() or || for string joining
- Use CURRENT_TIMESTAMP() for datetime
- Use QUALIFY for window function filtering
""",
    "BigQuery": """
- Use LOWER() for case-insensitive comparisons
- Use LIMIT for row limiting
- Use CONCAT() for string joining
- Use CURRENT_DATETIME() for datetime
- Use backticks for project.dataset.table references
"""
}

# =========================================================
# MAIN FUNCTION
# =========================================================

def show_ai_sql_generator():

    st.markdown("""
    <h1 style='font-size:42px;font-weight:800;color:white;'>
    🤖 AI SQL Generator
    </h1>
    """, unsafe_allow_html=True)

    st.caption("Describe what you want in plain English")
    st.write("")

    if st.session_state.sql_engine is None:
        st.warning("⚠️ Please connect to a database first.")
        return

    tables = st.session_state.sql_tables

    # =====================================================
    # DB TYPE — from session state set in db_connection
    # Issue #5 fix
    # =====================================================

    # get the db type that was selected during connection
    db_options = [
        "MySQL", "PostgreSQL", "SQL Server",
        "SQLite", "Snowflake", "BigQuery"
    ]
    default_idx = db_options.index(
        st.session_state.get("sql_db_type", "SQLite")
    )
    current_db_type = st.selectbox(
        "🗄️ Select SQL Dialect",
        db_options,
        index=default_idx,
        key="sql_analytics_dialect"
    )

    st.markdown(f"""
    <div style="
        background:linear-gradient(135deg,#064e3b,#065f46);
        padding:12px 18px;
        border-radius:12px;
        border:1px solid rgba(255,255,255,0.08);
        margin-bottom:16px;
        display:inline-block;
    ">
        <p style="color:#6ee7b7;margin:0;font-size:14px;">
        🗄️ Generating queries for:
        <b>{current_db_type}</b> syntax
        </p>
    </div>
    """, unsafe_allow_html=True)

    # =====================================================
    # BUILD SCHEMA CONTEXT
    # =====================================================

    schema_info = ""

    try:
        inspector = sqlalchemy.inspect(st.session_state.sql_engine)
        for table in tables[:10]:
            cols = inspector.get_columns(table)
            col_names = [c["name"] for c in cols]
            schema_info += (
                f"Table: {table}\n"
                f"Columns: {col_names}\n\n"
            )
    except Exception as e:
        schema_info = f"Tables: {tables}"

    # get syntax rules for selected db type
    syntax_rules = DB_SYNTAX_RULES.get(
        current_db_type,
        DB_SYNTAX_RULES["SQLite"]
    )

    # =====================================================
    # USER INPUT
    # =====================================================

    user_request = st.text_area(
        "Describe your SQL query",
        placeholder=(
            "Example: Show top 10 customers by total orders\n"
            "Example: Find all products with price above 100\n"
            "Example: Get monthly sales summary for 2023"
        ),
        height=150
    )

    st.write("")

    if st.button(
        "🚀 Generate SQL Query",
        use_container_width=True,
        key="ai_gen_sql_btn"
    ):

        if not user_request.strip():
            st.warning("Please describe your query first.")
            return

        prompt = f"""
You are an expert {current_db_type} SQL developer.

Generate ONLY a valid {current_db_type} SQL query.

{current_db_type} SYNTAX RULES:
{syntax_rules}

STRICT RULES:
- Return ONLY the SQL query
- No explanations
- No markdown backticks
- No comments
- No reasoning text

Database Schema:
{schema_info}

User Request:
{user_request}
"""

        with st.spinner(
            f"Generating {current_db_type} SQL..."
        ):
            response = ask_ai(
                prompt,
                st.secrets["OPENROUTER_API_KEY"]
            )

        st.session_state.sql_generated_query = response

    # =====================================================
    # DISPLAY GENERATED SQL
    # =====================================================

    if st.session_state.sql_generated_query != "":

        st.success("SQL Query Generated ✅")

        st.code(
            st.session_state.sql_generated_query,
            language="sql"
        )

        st.write("")

        col1, col2 = st.columns(2)

        with col1:
            if st.button(
                "▶️ Run This Query",
                use_container_width=True,
                key="run_generated_sql"
            ):
                try:
                    with st.session_state.sql_engine.connect() as conn:
                        result_df = pd.read_sql(
                            st.session_state.sql_generated_query,
                            conn
                        )
                    st.session_state.sql_query_result = result_df
                    st.success(
                        f"Query executed! "
                        f"{len(result_df)} rows returned."
                    )
                    st.dataframe(
                        result_df,
                        use_container_width=True
                    )
                except Exception as e:
                    st.error(f"Query error: {e}")

        with col2:
            if st.button(
                "📄 Add SQL To PDF",
                use_container_width=True,
                key="gen_sql_pdf_btn"
            ):
                st.session_state.pdf_sections.append({
                    "type": "text",
                    "title": f"AI Generated SQL Query ({current_db_type})",
                    "content": st.session_state.sql_generated_query
                })
                st.success("SQL Added To PDF ✅")