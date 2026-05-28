# =========================================================
# FILE ANALYTICS - AI INSIGHTS
# =========================================================

import streamlit as st
import requests
import re

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
# RENDER MARKDOWN NICELY ON WEBSITE
# Issue #1 fix - renders headings, tables, bold properly
# =========================================================

def render_insights_on_screen(content):
    """
    Renders AI insights beautifully on the website
    by processing line by line — headings bold & blue,
    tables as st.table, normal text as styled paragraphs.
    """

    lines = content.split("\n")
    table_buffer = []

    def flush_table(table_buffer):
        if not table_buffer:
            return
        # skip separator rows
        clean_rows = [
            r for r in table_buffer
            if not re.match(r"^\|[-| :]+\|$", r.strip())
        ]
        parsed = []
        for row in clean_rows:
            cols = [c.strip().replace("**", "").replace("*", "") for c in row.split("|") if c.strip()]
            if cols:
                parsed.append(cols)
        if len(parsed) >= 2:
            import pandas as pd
            headers = parsed[0]
            rows = parsed[1:]
            # normalize column count
            max_cols = max(len(r) for r in [headers] + rows)
            headers += [""] * (max_cols - len(headers))
            norm_rows = [r + [""] * (max_cols - len(r)) for r in rows]
            try:
                df_table = pd.DataFrame(norm_rows, columns=headers)
                st.dataframe(df_table, use_container_width=True)
            except:
                for r in parsed:
                    st.write(" | ".join(r))

    for line in lines:
        stripped = line.strip()

        if not stripped:
            flush_table(table_buffer)
            table_buffer = []
            st.write("")
            continue

        # separator row — skip
        if re.match(r"^\|[-| :]+\|$", stripped):
            continue

        # heading
        if stripped.startswith("#"):
            flush_table(table_buffer)
            table_buffer = []
            level = len(stripped) - len(stripped.lstrip("#"))
            text = stripped.lstrip("#").strip()
            if level == 1:
                st.markdown(
                    f"<h2 style='color:#60a5fa;font-weight:800;"
                    f"margin-top:20px;margin-bottom:8px;'>"
                    f"{text}</h2>",
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f"<h3 style='color:#93c5fd;font-weight:700;"
                    f"margin-top:14px;margin-bottom:6px;'>"
                    f"{text}</h3>",
                    unsafe_allow_html=True
                )

        # table row
        elif "|" in stripped:
            table_buffer.append(stripped)

        # normal text
        else:
            flush_table(table_buffer)
            table_buffer = []
            # clean markdown bold/italic for display
            clean = stripped.replace("**", "").replace("*", "")
            st.markdown(
                f"<p style='color:#e2e8f0;line-height:1.8;"
                f"margin:4px 0;'>{clean}</p>",
                unsafe_allow_html=True
            )

    flush_table(table_buffer)

# =========================================================
# CLEAN CONTENT FOR PDF (remove black dots)
# Issue #4 fix
# =========================================================

def clean_for_pdf(content):
    """Remove markdown symbols that cause black dots in PDF."""
    content = re.sub(r"\*\*(.+?)\*\*", r"\1", content)
    content = re.sub(r"\*(.+?)\*", r"\1", content)
    content = content.replace("■", "-")
    content = content.replace("•", "-")
    return content

# =========================================================
# MAIN FUNCTION
# =========================================================

def show_ai_insights(df):

    st.markdown("""
    <h1 style='font-size:52px;font-weight:800;color:white;'>
    🧠 Smart AI Insights
    </h1>
    """, unsafe_allow_html=True)

    st.caption("Business intelligence powered by AI")
    st.write("")

    if "ai_insights_response" not in st.session_state:
        st.session_state.ai_insights_response = ""

    if st.button(
        "🚀 Generate AI Insights",
        use_container_width=True,
        key="generate_ai_insights"
    ):

        full_prompt = f"""
You are a professional AI Data Analyst.

Analyze this dataset and generate concise insights.

Use markdown formatting:
- Use ## for section headings
- Use | tables | for structured data
- Use **bold** for key terms
- Keep sections: Key Business Insights, Trends,
  Anomalies, Risks, Opportunities, Recommendations

Dataset Columns:
{list(df.columns)}

Dataset Sample:
{df.head(15).to_string()}

Keep response focused and professional.
"""

        with st.spinner("Generating AI Insights..."):
            response = ask_ai(
                full_prompt,
                st.secrets["OPENROUTER_API_KEY"]
            )

        response = re.sub(r"^```(?:markdown)?\s*\n?", "", response.strip())
        response = response.rstrip("```").strip()
        st.session_state.ai_insights_response = response

    st.write("")

    if st.session_state.ai_insights_response != "":

        st.success("AI Insights Generated Successfully ✅")
        st.write("")

        # =====================================================
        # Render beautifully on website — Issue #1
        # =====================================================

        with st.container():
            st.markdown("""
            <div style="
                background:#0f172a;
                padding:25px;
                border-radius:18px;
                border:1px solid rgba(255,255,255,0.08);
                margin-bottom:16px;
            ">
            """, unsafe_allow_html=True)

            render_insights_on_screen(
                st.session_state.ai_insights_response
            )

            st.markdown("</div>", unsafe_allow_html=True)

        st.write("")

        if st.button(
            "📄 Add Insights To PDF",
            use_container_width=True,
            key="add_ai_insights_pdf"
        ):
            # clean content before adding to PDF — Issue #4
            clean_content = clean_for_pdf(
                st.session_state.ai_insights_response
            )
            st.session_state.pdf_sections.append({
                "type": "text",
                "title": "AI Insights",
                "content": clean_content
            })
            st.success("AI Insights Added To PDF ✅")