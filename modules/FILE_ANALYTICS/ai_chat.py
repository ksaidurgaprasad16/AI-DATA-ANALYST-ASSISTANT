# =========================================================
# FILE ANALYTICS - AI CHATBOT
# =========================================================

import streamlit as st
import requests

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
            timeout=120
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

def show_ai_chat(df, uploaded_file):

    st.markdown("""
    <style>
    .stChatMessage{
        background:#111827;
        border-radius:16px;
        padding:14px;
        margin-bottom:10px;
        border:1px solid rgba(255,255,255,0.08);
    }
    .stChatInput input{
        background:#0f172a !important;
        color:white !important;
        border-radius:14px !important;
        border:1px solid rgba(255,255,255,0.1) !important;
        padding:14px !important;
        font-size:16px !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <h1 style='font-size:52px;font-weight:800;color:white;'>
    🤖 AI Chatbot
    </h1>
    """, unsafe_allow_html=True)

    st.caption("Chat continuously with your dataset")
    st.write("")

    # =====================================================
    # SESSION STATES
    # =====================================================

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if "latest_ai_response" not in st.session_state:
        st.session_state.latest_ai_response = ""

    if "latest_user_question" not in st.session_state:
        st.session_state.latest_user_question = ""

    # =====================================================
    # RESET CHAT ON NEW FILE
    # =====================================================

    current_file_name = uploaded_file.name

    if (
        "chat_file" not in st.session_state
        or st.session_state.chat_file != current_file_name
    ):
        st.session_state.chat_history = []
        st.session_state.chat_file = current_file_name

    # =====================================================
    # CLEAR CHAT
    # =====================================================

    c1, c2 = st.columns([1, 4])

    with c1:
        if st.button(
            "🗑 Clear Chat",
            use_container_width=True,
            key="clear_ai_chat"
        ):
            st.session_state.chat_history = []
            st.session_state.latest_ai_response = ""
            st.session_state.latest_user_question = ""
            st.rerun()

    st.write("")

    # =====================================================
    # DISPLAY CHAT HISTORY
    # =====================================================

    for chat in st.session_state.chat_history:
        with st.chat_message(chat["role"]):
            st.markdown(chat["content"])

    # =====================================================
    # USER INPUT
    # =====================================================

    user_question = st.chat_input(
        "Ask anything about your dataset..."
    )

    if user_question:

        st.chat_message("user").markdown(user_question)

        st.session_state.chat_history.append({
            "role": "user",
            "content": user_question
        })

        conversation_history = ""
        for msg in st.session_state.chat_history:
            conversation_history += (
                f"{msg['role']}: {msg['content']}\n"
            )

        prompt = f"""
You are an expert AI Data Analyst.

Continue the conversation naturally.

IMPORTANT:
- Answer professionally
- Use business language
- Use dataset context
- Explain insights clearly
- Keep continuity in conversation

Dataset Columns:
{list(df.columns)}

Dataset Sample:
{df.head(15).to_string()}

Conversation History:
{conversation_history}

Current User Question:
{user_question}

Give detailed professional answers.
"""

        with st.spinner("Analyzing Dataset..."):
            response = ask_ai(
                prompt,
                st.secrets["OPENROUTER_API_KEY"]
            )

        st.session_state.latest_ai_response = response
        st.session_state.latest_user_question = user_question

        with st.chat_message("assistant"):
            st.markdown(response)

        st.session_state.chat_history.append({
            "role": "assistant",
            "content": response
        })

    st.write("")

    # =====================================================
    # ADD TO PDF — Issue #6 fix
    # Adds FULL conversation history, not just last message
    # =====================================================

    if len(st.session_state.chat_history) > 0:

        if st.button(
            "📄 Add Full Chat To PDF",
            use_container_width=True,
            key="chat_pdf_btn"
        ):
            # Build full conversation transcript
            full_transcript = ""

            for msg in st.session_state.chat_history:
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
                "title": "AI Chatbot Conversation",
                "content": full_transcript
            })

            st.success("Full Chat History Added To PDF ✅")