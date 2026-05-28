# =========================================================
# FILE ANALYTICS - SQL GENERATOR
# =========================================================

import streamlit as st
import requests

# =========================================================
# DB TYPE SYNTAX RULES — Issue #9
# =========================================================

DB_SYNTAX_RULES = {
    "SQLite": """
- Use LOWER() for case-insensitive comparisons
- Use LIMIT for row limiting
- Use || for string concatenation
- Use datetime('now') for current datetime
""",
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
""",
    "SQL Server": """
- Use TOP instead of LIMIT (e.g. SELECT TOP 10)
- Use UPPER()/LOWER() for case comparisons
- Use + for string concatenation
- Use GETDATE() for current datetime
""",
    "Snowflake": """
- Use ILIKE for case-insensitive comparisons
- Use LIMIT for row limiting
- Use CONCAT() or || for string joining
- Use CURRENT_TIMESTAMP() for datetime
""",
    "BigQuery": """
- Use LOWER() for case-insensitive comparisons
- Use LIMIT for row limiting
- Use CONCAT() for string joining
- Use CURRENT_DATETIME() for datetime
- Use backticks for table references
"""
}

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
# MAIN FUNCTION
# =========================================================

def show_sql_generator(df):

    st.markdown("""
    <h1 style='font-size:52px;font-weight:800;color:white;'>
    🗄 AI SQL Generator
    </h1>
    """, unsafe_allow_html=True)

    st.caption("Generate SQL queries using AI")
    st.write("")

    if "sql_response" not in st.session_state:
        st.session_state.sql_response = ""

    # =====================================================
    # SQL DIALECT SELECTOR — Issue #9
    # =====================================================

    col1, col2 = st.columns([2, 3])

    with col1:
        selected_dialect = st.selectbox(
            "🗄️ Select SQL Dialect",
            [
                "SQLite",
                "MySQL",
                "PostgreSQL",
                "SQL Server",
                "Snowflake",
                "BigQuery"
            ],
            key="file_sql_dialect"
        )

    with col2:
        st.markdown(f"""
        <div style="
            background:linear-gradient(135deg,#064e3b,#065f46);
            padding:12px 18px;
            border-radius:12px;
            border:1px solid rgba(255,255,255,0.08);
            margin-top:28px;
        ">
            <p style="color:#6ee7b7;margin:0;font-size:14px;">
            ✅ Generating
            <b>{selected_dialect}</b> syntax queries
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    # =====================================================
    # USER INPUT
    # =====================================================

    sql_query = st.text_area(
        "Describe SQL Query",
        placeholder=(
            "Example: Show top 10 products by sales\n"
            "Example: Find all rows where age is above 30\n"
            "Example: Get monthly totals grouped by category"
        ),
        height=160
    )

    st.write("")

    # =====================================================
    # GENERATE SQL
    # =====================================================

    if st.button(
        "🚀 Generate SQL Query",
        use_container_width=True,
        key="generate_sql_query"
    ):

        if not sql_query.strip():
            st.warning("Please describe your query first.")
            return

        syntax_rules = DB_SYNTAX_RULES.get(
            selected_dialect,
            DB_SYNTAX_RULES["SQLite"]
        )

        prompt = f"""
You are an expert {selected_dialect} SQL developer.

Generate ONLY a valid {selected_dialect} SQL query.

{selected_dialect} SYNTAX RULES:
{syntax_rules}

STRICT RULES:
- Return ONLY the SQL query
- No explanations
- No markdown backticks
- No comments
- No reasoning text

Dataset Columns (use these as table column names):
{list(df.columns)}

Assume the table name is: dataset

User Request:
{sql_query}
"""

        with st.spinner(
            f"Generating {selected_dialect} SQL Query..."
        ):
            response = ask_ai(
                prompt,
                st.secrets["OPENROUTER_API_KEY"]
            )

        st.session_state.sql_response = response

    st.write("")

    # =====================================================
    # DISPLAY SQL
    # =====================================================

    if st.session_state.sql_response != "":

        st.success("SQL Query Generated Successfully ✅")

        st.code(
            st.session_state.sql_response,
            language="sql"
        )

        st.write("")

        if st.button(
            "📄 Add SQL To PDF",
            use_container_width=True,
            key="sql_pdf_btn"
        ):
            st.session_state.pdf_sections.append({
                "type": "text",
                "title": f"Generated SQL Query ({selected_dialect})",
                "content": st.session_state.sql_response
            })
            st.success("SQL Query Added To PDF ✅")