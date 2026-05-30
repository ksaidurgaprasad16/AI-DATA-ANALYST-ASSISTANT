# =========================================================
# POWER BI ANALYTICS - METADATA READER
# =========================================================

import streamlit as st
import re
from modules.POWER_BI_ANALYTICS.utils import ask_ai

# =========================================================
# MAIN FUNCTION
# =========================================================

def show_metadata_reader():

    st.markdown("""
    <h1 style='font-size:52px;font-weight:800;color:white;'>
    🗂️ Metadata Reader
    </h1>
    """, unsafe_allow_html=True)

    st.caption("AI-generated metadata summary for your dataset")
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
        padding:20px 25px;
        border-radius:18px;
        border:1px solid rgba(255,255,255,0.08);
        margin-bottom:24px;
    ">
        <h3 style="color:white;margin:0 0 8px 0;">
        📁 Dataset Loaded
        </h3>
        <p style="color:#c4b5fd;margin:0;">
        <b>{file_name}</b> &nbsp;•&nbsp;
        {shape[0]:,} rows &nbsp;•&nbsp;
        {shape[1]} columns &nbsp;•&nbsp;
        Columns: {", ".join(columns[:6])}
        {"..." if len(columns) > 6 else ""}
        </p>
    </div>
    """, unsafe_allow_html=True)

    if "pbix_metadata_response" not in st.session_state:
        st.session_state.pbix_metadata_response = ""

    if st.button(
        "🚀 Generate Metadata Summary",
        use_container_width=True,
        key="generate_metadata"
    ):
        prompt = f"""
You are a senior Power BI data architect.

Analyze the dataset columns and generate a professional
Power BI metadata summary report.

Use ONLY this exact format:

## Table Overview
| Property | Details |
(fill: file name, total columns, suggested table name, data category)

## Column Metadata
| Column Name | Suggested Data Type | Category | Description |
(analyze each column — categorize as Dimension/Measure/Date/ID/Text)

## Data Categories Summary
| Category | Columns | Power BI Role |
(group into: Dimensions, Measures, Dates, IDs, Text fields)

## Suggested Table Name
| Original File Name | Suggested Power BI Table Name | Reason |

## Power BI Data Model Notes
| Observation | Recommendation | Priority |

File Name: {file_name}
Total Rows: {shape[0]:,}
Total Columns: {shape[1]}
Columns: {columns}

Be specific — reference actual column names.
Keep recommendations practical for Power BI beginners.
"""

        with st.spinner("Generating Metadata Summary..."):
            response = ask_ai(
                prompt,
                st.secrets["OPENROUTER_API_KEY"]
            )

        st.session_state.pbix_metadata_response = response

    st.write("")

    if st.session_state.pbix_metadata_response != "":

        st.success("Metadata Summary Generated ✅")
        st.write("")

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

            _render_on_screen(
                st.session_state.pbix_metadata_response
            )

            st.markdown("</div>", unsafe_allow_html=True)

        st.write("")

        col1, col2 = st.columns(2)

        with col1:
            if st.button(
                "📄 Add Metadata To PDF",
                use_container_width=True,
                key="metadata_pdf_btn"
            ):
                st.session_state.pbix_pdf_sections.append({
                    "type": "text",
                    "title": "Metadata Summary",
                    "content": st.session_state.pbix_metadata_response
                })
                st.success("Metadata Added To PDF ✅")

        with col2:
            if st.button(
                "🔄 Regenerate",
                use_container_width=True,
                key="regenerate_metadata"
            ):
                st.session_state.pbix_metadata_response = ""
                st.rerun()


# =========================================================
# RENDER ON SCREEN
# =========================================================

def _render_on_screen(content):

    lines = content.split("\n")
    table_buffer = []

    def flush_table(buf):
        if not buf:
            return
        clean_rows = [
            r for r in buf
            if not re.match(r"^\|[-| :]+\|$", r.strip())
        ]
        parsed = []
        for row in clean_rows:
            cols = [
                c.strip().replace("**", "").replace("*", "")
                for c in row.split("|") if c.strip()
            ]
            if cols:
                parsed.append(cols)
        if len(parsed) >= 2:
            import pandas as pd
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
                <h2 style='color:#f9a8d4;font-weight:800;
                font-size:24px;margin-top:24px;
                margin-bottom:10px;'>{text}</h2>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <h3 style='color:#c4b5fd;font-weight:700;
                font-size:18px;margin-top:16px;
                margin-bottom:8px;'>{text}</h3>
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