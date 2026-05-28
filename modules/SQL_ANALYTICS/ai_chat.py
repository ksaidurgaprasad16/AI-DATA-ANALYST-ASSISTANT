# =========================================================
# SQL ANALYTICS - AI SQL CHAT
# =========================================================

import streamlit as st
import sqlalchemy

from modules.SQL_ANALYTICS.utils import ask_ai

# =========================================================
# MAIN FUNCTION
# =========================================================

def show_ai_sql_chat():

    st.markdown("""
    <h1 style='font-size:42px;font-weight:800;color:white;'>
    💬 AI SQL Chat
    </h1>
    """, unsafe_allow_html=True)

    st.caption("Chat with your database using AI")
    st.write("")

    if st.session_state.sql_engine is None:
        st.warning("⚠️ Please connect to a database first.")
        return

    tables = st.session_state.sql_tables

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
    except:
        schema_info = f"Tables: {tables}"

    # =====================================================
    # SESSION STATE
    # =====================================================

    if "sql_chat_history" not in st.session_state:
        st.session_state.sql_chat_history = []

    if "sql_latest_response" not in st.session_state:
        st.session_state.sql_latest_response = ""

    if "sql_latest_question" not in st.session_state:
        st.session_state.sql_latest_question = ""

    # =====================================================
    # CLEAR CHAT
    # =====================================================

    if st.button("🗑 Clear Chat", key="clear_sql_chat"):
        st.session_state.sql_chat_history = []
        st.session_state.sql_latest_response = ""
        st.session_state.sql_latest_question = ""
        st.rerun()

    st.write("")

    # =====================================================
    # CHAT HISTORY
    # =====================================================

    for chat in st.session_state.sql_chat_history:
        with st.chat_message(chat["role"]):
            st.markdown(chat["content"])

    # =====================================================
    # USER INPUT
    # =====================================================

    user_input = st.chat_input(
        "Ask anything about your database..."
    )

    if user_input:

        st.chat_message("user").markdown(user_input)

        st.session_state.sql_chat_history.append({
            "role": "user",
            "content": user_input
        })

        conversation = ""
        for msg in st.session_state.sql_chat_history:
            conversation += (
                f"{msg['role']}: {msg['content']}\n"
            )

        prompt = f"""
You are an expert SQL database analyst.

Answer the user's question about their database.
If they ask for a query, generate valid SQL.
Keep answers concise and professional.

Database Schema:
{schema_info}

Conversation History:
{conversation}

Current Question:
{user_input}
"""

        with st.spinner("Thinking..."):
            response = ask_ai(
                prompt,
                st.secrets["OPENROUTER_API_KEY"]
            )

        st.session_state.sql_latest_response = response
        st.session_state.sql_latest_question = user_input

        with st.chat_message("assistant"):
            st.markdown(response)

        st.session_state.sql_chat_history.append({
            "role": "assistant",
            "content": response
        })

    st.write("")

    # =====================================================
    # ADD TO PDF — Issue #6 fix
    # Adds FULL conversation history not just last message
    # =====================================================

    if len(st.session_state.sql_chat_history) > 0:

        if st.button(
            "📄 Add Full Chat To PDF",
            use_container_width=True,
            key="sql_chat_pdf_btn"
        ):
            # Build full conversation transcript
            full_transcript = ""

            for msg in st.session_state.sql_chat_history:
                role_label = (
                    "👤 User" if msg["role"] == "user"
                    else "🤖 Assistant"
                )
                full_transcript += (
                    f"{role_label}:\n"
                    f"{msg['content']}\n\n"
                    f"{'─' * 40}\n\n"
                )

            st.session_state.pdf_sections.append({
                "type": "text",
                "title": "AI SQL Chat Conversation",
                "content": full_transcript
            })

            st.success("Full Chat History Added To PDF ✅")