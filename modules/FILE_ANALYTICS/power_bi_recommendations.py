# =========================================================
# FILE ANALYTICS - POWER BI RECOMMENDATIONS
# =========================================================

import streamlit as st
import requests
import pandas as pd
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
# RENDER POWER BI RECOMMENDATIONS ON WEBSITE
# Issue #1 fix — headings, tables rendered beautifully
# =========================================================

def render_powerbi_on_screen(content):

    lines = content.split("\n")
    table_buffer = []

    def flush_table(table_buffer):
        if not table_buffer:
            return
        clean_rows = [
            r for r in table_buffer
            if not re.match(r"^\|[-| :]+\|$", r.strip())
        ]
        parsed = []
        for row in clean_rows:
            cols = [c.strip() for c in row.split("|") if c.strip()]
            if cols:
                parsed.append(cols)
        if len(parsed) >= 2:
            headers = parsed[0]
            rows = parsed[1:]
            max_cols = max(len(r) for r in [headers] + rows)
            headers += [""] * (max_cols - len(headers))
            norm_rows = [
                r + [""] * (max_cols - len(r)) for r in rows
            ]
            try:
                df_table = pd.DataFrame(norm_rows, columns=headers)
                st.dataframe(df_table, use_container_width=True)
            except:
                for r in parsed:
                    st.write(" | ".join(r))
        elif len(parsed) == 1:
            st.write(" | ".join(parsed[0]))

    for line in lines:
        stripped = line.strip()

        if not stripped:
            flush_table(table_buffer)
            table_buffer = []
            continue

        if re.match(r"^\|[-| :]+\|$", stripped):
            continue

        if stripped.startswith("#"):
            flush_table(table_buffer)
            table_buffer = []
            level = len(stripped) - len(stripped.lstrip("#"))
            text = stripped.lstrip("#").strip()
            if level == 1:
                st.markdown(f"""
                <h2 style='
                    color:#f9a8d4;
                    font-weight:800;
                    font-size:24px;
                    margin-top:24px;
                    margin-bottom:10px;
                    padding-bottom:6px;
                    border-bottom:2px solid rgba(249,168,212,0.3);
                '>
                📈 {text}
                </h2>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <h3 style='
                    color:#c4b5fd;
                    font-weight:700;
                    font-size:18px;
                    margin-top:16px;
                    margin-bottom:8px;
                '>
                {text}
                </h3>
                """, unsafe_allow_html=True)

        elif "|" in stripped:
            table_buffer.append(stripped)

        else:
            flush_table(table_buffer)
            table_buffer = []
            clean = stripped.replace("**", "").replace("*", "")
            st.markdown(
                f"<p style='color:#e2e8f0;line-height:1.8;"
                f"margin:4px 0;'>{clean}</p>",
                unsafe_allow_html=True
            )

    flush_table(table_buffer)

# =========================================================
# CLEAN FOR PDF — Issue #4
# =========================================================

def clean_for_pdf(content):
    content = re.sub(r"\*\*(.+?)\*\*", r"\1", content)
    content = re.sub(r"\*(.+?)\*", r"\1", content)
    content = content.replace("■", "-")
    content = content.replace("•", "-")
    return content

# =========================================================
# MAIN FUNCTION
# =========================================================

def show_power_bi_recommendations(df):

    st.markdown("""
    <h1 style='font-size:52px;font-weight:800;color:white;'>
    📈 Power BI Recommendations
    </h1>
    """, unsafe_allow_html=True)

    st.caption(
        "AI-generated Power BI dashboard suggestions"
    )
    st.write("")

    if "powerbi_rec_response" not in st.session_state:
        st.session_state.powerbi_rec_response = ""

    # =====================================================
    # INFO CARD
    # =====================================================

    st.markdown(f"""
    <div style="
        background:linear-gradient(135deg,#1e1b4b,#312e81);
        padding:20px 25px;
        border-radius:18px;
        border:1px solid rgba(255,255,255,0.08);
        margin-bottom:20px;
    ">
        <h3 style="color:white;margin:0 0 8px 0;">
        📊 Dataset Loaded
        </h3>
        <p style="color:#c4b5fd;margin:0;">
        {df.shape[0]:,} rows &nbsp;•&nbsp;
        {df.shape[1]} columns &nbsp;•&nbsp;
        Columns: {", ".join(df.columns.tolist()[:6])}
        {"..." if len(df.columns) > 6 else ""}
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    if st.button(
        "🚀 Generate Power BI Recommendations",
        use_container_width=True,
        key="generate_powerbi_rec"
    ):

        prompt = f"""
You are a senior Power BI consultant and data analyst.

Analyze the dataset and generate professional
Power BI dashboard recommendations.

Use ONLY this exact format:

# Dashboard Pages
| Page Name | Purpose |

# KPIs to Track
| KPI | Business Value |

# Recommended Visuals
| Visual Type | Column(s) to Use | Insight |

# Slicers & Filters
| Slicer | Column | Why Useful |

# DAX Measures
| Measure Name | DAX Formula |

# Dashboard Layout Map
| Page | KPIs | Main Visual | Slicer |

Dataset Columns:
{list(df.columns)}

Dataset Sample:
{df.head(10).to_string()}
"""

        with st.spinner("Generating Power BI Recommendations..."):
            response = ask_ai(
                prompt,
                st.secrets["OPENROUTER_API_KEY"]
            )

        st.session_state.powerbi_rec_response = response

    st.write("")

    if st.session_state.powerbi_rec_response != "":

        st.success("Power BI Recommendations Ready ✅")
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

            render_powerbi_on_screen(
                st.session_state.powerbi_rec_response
            )

            st.markdown("</div>", unsafe_allow_html=True)

        st.write("")

        col1, col2 = st.columns(2)

        with col1:
            if st.button(
                "📄 Add Recommendations To PDF",
                use_container_width=True,
                key="powerbi_rec_pdf_btn"
            ):
                # clean for PDF — Issue #4
                clean_content = clean_for_pdf(
                    st.session_state.powerbi_rec_response
                )
                st.session_state.pdf_sections.append({
                    "type": "text",
                    "title": "Power BI Recommendations",
                    "content": clean_content
                })
                st.success("Recommendations Added To PDF ✅")

        with col2:
            if st.button(
                "🔄 Regenerate",
                use_container_width=True,
                key="regenerate_powerbi_rec"
            ):
                st.session_state.powerbi_rec_response = ""
                st.rerun()