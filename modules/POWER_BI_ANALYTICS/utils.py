# =========================================================
# POWER BI ANALYTICS - SHARED UTILITIES
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
# SESSION STATE INITIALIZER
# =========================================================

def init_pbix_session_state():

    defaults = {
        "pbix_file_name": None,
        "pbix_columns": [],
        "pbix_metadata_response": "",
        "pbix_dax_response": "",
        "pbix_relationship_response": "",
        "pbix_chat_history": [],
        "pbix_latest_response": "",
        "pbix_latest_question": "",
        "pbix_pdf_sections": [],
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value