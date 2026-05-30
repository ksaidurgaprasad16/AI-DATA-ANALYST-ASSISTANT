# =========================================================
# POWER BI ANALYTICS - AI CHAT
# =========================================================

import streamlit as st
from modules.POWER_BI_ANALYTICS.utils import ask_ai

# =========================================================
# MAIN FUNCTION
# =========================================================

def show_pbix_ai_chat():

    st.markdown("""
    <style>
    .stChatMessage{
        background:#111827;
        border-radius:16px;
        padding:14px;
        margin-bottom:10px;
        border:1px solid rgba(255,255,255,0.08);
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <h1 style='font-size:52px;font-weight:800;color:white;'>
    🤖 AI Power BI Assistant
    </h1>
    """, unsafe_allow_html=True)

    st.caption("Chat with AI about your Power BI dashboard")
    st.write("")

    if not st.session_state.get("pbix_columns"):
        st.warning("⚠️ Please upload a file in Dashboard first.")
        return

    columns = st.session_state.pbix_columns
    file_name = st.session_state.get("pbix_file_name", "Dataset")
    shape = st.session_state.get("pbix_df_shape", (0, 0))

    # =====================================================
    # INFO CARD
    # =====================================================

    st.markdown(f"""
    <div style="
        background:linear-gradient(135deg,#1e1b4b,#312e81);
        padding:16px 22px;
        border-radius:14px;
        border:1px solid rgba(255,255,255,0.08);
        margin-bottom:20px;
    ">
        <p style="color:#c4b5fd;margin:0;font-size:14px;">
        💡 Chatting about <b>{file_name}</b> &nbsp;•&nbsp;
        {shape[0]:,} rows &nbsp;•&nbsp;
        {shape[1]} columns
        </p>
    </div>
    """, unsafe_allow_html=True)

    # =====================================================
    # SESSION STATE
    # =====================================================

    if "pbix_chat_history" not in st.session_state:
        st.session_state.pbix_chat_history = []

    if "pbix_latest_response" not in st.session_state:
        st.session_state.pbix_latest_response = ""

    if "pbix_latest_question" not in st.session_state:
        st.session_state.pbix_latest_question = ""

    # =====================================================
    # CLEAR CHAT
    # =====================================================

    if st.button(
        "🗑 Clear Chat",
        key="clear_pbix_chat"
    ):
        st.session_state.pbix_chat_history = []
        st.session_state.pbix_latest_response = ""
        st.session_state.pbix_latest_question = ""
        st.rerun()

    st.write("")

    # =====================================================
    # SUGGESTED QUESTIONS
    # =====================================================

    st.markdown("""
    <h3 style='color:#c4b5fd;font-weight:700;
    font-size:16px;margin-bottom:10px;'>
    💬 Suggested Questions
    </h3>
    """, unsafe_allow_html=True)

    suggested = [
        "What visuals should I use for this dataset?",
        "How do I create a KPI card in Power BI?",
        "What DAX formula calculates month-over-month growth?",
        "How should I structure my dashboard pages?"
    ]

    cols = st.columns(2)
    for i, question in enumerate(suggested):
        with cols[i % 2]:
            if st.button(
                question,
                use_container_width=True,
                key=f"suggested_{i}"
            ):
                st.session_state._pbix_suggested = question
                st.rerun()

    st.write("")

    # =====================================================
    # CHAT HISTORY
    # =====================================================

    for chat in st.session_state.pbix_chat_history:
        with st.chat_message(chat["role"]):
            st.markdown(chat["content"])

    # =====================================================
    # USER INPUT
    # =====================================================

    user_input = st.chat_input(
        "Ask anything about Power BI or your dataset..."
    )

    # handle suggested question click
    if hasattr(st.session_state, "_pbix_suggested"):
        user_input = st.session_state._pbix_suggested
        del st.session_state._pbix_suggested

    if user_input:

        st.chat_message("user").markdown(user_input)

        st.session_state.pbix_chat_history.append({
            "role": "user",
            "content": user_input
        })

        conversation = ""
        for msg in st.session_state.pbix_chat_history:
            conversation += (
                f"{msg['role']}: {msg['content']}\n"
            )

        prompt = f"""
You are an expert Power BI consultant and data analyst.

Answer the user's question about Power BI professionally.

IMPORTANT:
- Give practical, actionable advice
- Reference the dataset columns when relevant
- Explain Power BI concepts clearly
- Suggest specific visuals, DAX, or steps when asked
- Keep continuity with conversation history

File: {file_name}
Rows: {shape[0]:,}
Columns: {columns}

Conversation History:
{conversation}

Current Question:
{user_input}

Give a professional, helpful answer.
"""

        with st.spinner("Thinking..."):
            response = ask_ai(
                prompt,
                st.secrets["OPENROUTER_API_KEY"]
            )

        st.session_state.pbix_latest_response = response
        st.session_state.pbix_latest_question = user_input

        with st.chat_message("assistant"):
            st.markdown(response)

        st.session_state.pbix_chat_history.append({
            "role": "assistant",
            "content": response
        })

    st.write("")

    # =====================================================
    # ADD TO PDF
    # =====================================================

    if len(st.session_state.pbix_chat_history) > 0:

        if st.button(
            "📄 Add Full Chat To PDF",
            use_container_width=True,
            key="pbix_chat_pdf_btn"
        ):
            full_transcript = ""

            for msg in st.session_state.pbix_chat_history:
                role_label = (
                    "User" if msg["role"] == "user"
                    else "Assistant"
                )
                full_transcript += (
                    f"{role_label}:\n"
                    f"{msg['content']}\n\n"
                    f"{'─' * 40}\n\n"
                )

            st.session_state.pbix_pdf_sections.append({
                "type": "text",
                "title": "AI Power BI Chat",
                "content": full_transcript
            })

            st.success("Full Chat Added To PDF ✅")