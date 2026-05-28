# =========================================================
# SQL ANALYTICS - EXPORT CENTER
# =========================================================

import streamlit as st
import pandas as pd
import io

# =========================================================
# MAIN FUNCTION
# =========================================================

def show_sql_export_center():

    st.markdown("""
    <h1 style='font-size:42px;font-weight:800;color:white;'>
    📤 SQL Export Center
    </h1>
    """, unsafe_allow_html=True)

    st.caption("Export your query results")
    st.write("")

    if st.session_state.sql_query_result is None:
        st.info(
            "💡 Run a query first in Query Runner "
            "to export results."
        )
        return

    df = st.session_state.sql_query_result

    # =====================================================
    # RESULT INFO CARD
    # =====================================================

    st.markdown(f"""
    <div style="
        background:linear-gradient(135deg,#111827,#1e293b);
        padding:20px 25px;
        border-radius:18px;
        border:1px solid rgba(255,255,255,0.08);
        margin-bottom:24px;
    ">
        <h3 style="color:white;margin:0 0 6px 0;">
        📊 Current Query Result
        </h3>
        <p style="color:#94a3b8;margin:0;">
        {len(df):,} rows &nbsp;•&nbsp;
        {len(df.columns)} columns &nbsp;•&nbsp;
        Columns: {", ".join(df.columns.tolist()[:5])}
        {"..." if len(df.columns) > 5 else ""}
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    # =====================================================
    # EXPORT CARDS
    # =====================================================

    col1, col2, col3 = st.columns(3)

    # =====================================================
    # CSV
    # =====================================================

    with col1:

        st.markdown("""
        <div style="
            background:#111827;
            padding:25px 25px 15px 25px;
            border-radius:18px 18px 0 0;
            border:1px solid rgba(255,255,255,0.08);
            border-bottom:none;
        ">
        <h2 style="color:white;margin-bottom:8px;">
        📄 CSV Export
        </h2>
        <p style="color:#d1d5db;margin:0;">
        Download results in CSV format.
        </p>
        </div>
        """, unsafe_allow_html=True)

        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "⬇ Download CSV",
            data=csv,
            file_name="sql_results.csv",
            mime="text/csv",
            use_container_width=True,
            key="sql_csv_export"
        )

    # =====================================================
    # EXCEL
    # =====================================================

    with col2:

        st.markdown("""
        <div style="
            background:#111827;
            padding:25px 25px 15px 25px;
            border-radius:18px 18px 0 0;
            border:1px solid rgba(255,255,255,0.08);
            border-bottom:none;
        ">
        <h2 style="color:white;margin-bottom:8px;">
        📊 Excel Export
        </h2>
        <p style="color:#d1d5db;margin:0;">
        Export results as Excel workbook.
        </p>
        </div>
        """, unsafe_allow_html=True)

        excel_buffer = io.BytesIO()

        with pd.ExcelWriter(
            excel_buffer,
            engine="openpyxl"
        ) as writer:
            df.to_excel(writer, index=False)

        st.download_button(
            "⬇ Download Excel",
            data=excel_buffer.getvalue(),
            file_name="sql_results.xlsx",
            mime=(
                "application/vnd.openxmlformats-"
                "officedocument.spreadsheetml.sheet"
            ),
            use_container_width=True,
            key="sql_excel_export"
        )

    # =====================================================
    # JSON
    # =====================================================

    with col3:

        st.markdown("""
        <div style="
            background:#111827;
            padding:25px 25px 15px 25px;
            border-radius:18px 18px 0 0;
            border:1px solid rgba(255,255,255,0.08);
            border-bottom:none;
        ">
        <h2 style="color:white;margin-bottom:8px;">
        🔧 JSON Export
        </h2>
        <p style="color:#d1d5db;margin:0;">
        Export results in JSON format.
        </p>
        </div>
        """, unsafe_allow_html=True)

        json_data = df.to_json(
            orient="records",
            indent=4
        )

        st.download_button(
            "⬇ Download JSON",
            data=json_data,
            file_name="sql_results.json",
            mime="application/json",
            use_container_width=True,
            key="sql_json_export"
        )

    st.write("")
    st.write("")

    # =====================================================
    # SUMMARY EXPORT
    # =====================================================

    st.markdown("""
    <h2 style='color:white;font-weight:700;'>
    🚀 Advanced Export
    </h2>
    """, unsafe_allow_html=True)

    summary_text = f"""
SQL Query Results Summary
=========================
Rows: {len(df)}
Columns: {len(df.columns)}
Column Names: {list(df.columns)}

Sample Data (first 10 rows):
{df.head(10).to_string()}
"""

    st.download_button(
        "⬇ Download Summary TXT",
        data=summary_text,
        file_name="sql_summary.txt",
        mime="text/plain",
        use_container_width=True,
        key="sql_summary_export"
    )