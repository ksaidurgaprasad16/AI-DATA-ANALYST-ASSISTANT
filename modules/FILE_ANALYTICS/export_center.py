# =========================================================
# FILE ANALYTICS - EXPORT CENTER
# =========================================================

import streamlit as st
import pandas as pd
import io

# =========================================================
# MAIN FUNCTION
# =========================================================

def show_export_center(df):

    # =====================================================
    # HEADER
    # =====================================================

    st.markdown("""
    <h1 style='
        font-size:52px;
        font-weight:800;
        color:white;
    '>
    📤 Export Center
    </h1>
    """, unsafe_allow_html=True)

    st.caption(
        "Export datasets and analytics files"
    )

    st.write("")

    # =====================================================
    # EXPORT CARDS
    # =====================================================

    col1, col2, col3 = st.columns(3)

    # =====================================================
    # CSV EXPORT
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
        <h2 style="color:white; margin-bottom:8px;">
        📄 CSV Export
        </h2>
        <p style="color:#d1d5db; margin:0;">
        Download complete dataset in CSV format.
        </p>
        </div>
        """, unsafe_allow_html=True)

        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "⬇ Download CSV",
            data=csv,
            file_name="dataset_export.csv",
            mime="text/csv",
            use_container_width=True,
            key="csv_export_btn"
        )

    # =====================================================
    # EXCEL EXPORT
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
        <h2 style="color:white; margin-bottom:8px;">
        📊 Excel Export
        </h2>
        <p style="color:#d1d5db; margin:0;">
        Export dataset to Excel workbook format.
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
            file_name="dataset_export.xlsx",
            mime=(
                "application/vnd.openxmlformats-"
                "officedocument.spreadsheetml.sheet"
            ),
            use_container_width=True,
            key="excel_export_btn"
        )

    # =====================================================
    # SUMMARY EXPORT
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
        <h2 style="color:white; margin-bottom:8px;">
        🧠 Summary Export
        </h2>
        <p style="color:#d1d5db; margin:0;">
        Download dataset summary and metadata.
        </p>
        </div>
        """, unsafe_allow_html=True)

        summary_text = f"""
Dataset Rows: {df.shape[0]}
Dataset Columns: {df.shape[1]}
Missing Values: {df.isnull().sum().sum()}

Columns:
{list(df.columns)}
"""

        st.download_button(
            "⬇ Download Summary",
            data=summary_text,
            file_name="dataset_summary.txt",
            mime="text/plain",
            use_container_width=True,
            key="summary_export_btn"
        )

    st.write("")
    st.write("")

    # =====================================================
    # ADVANCED EXPORTS
    # =====================================================

    st.markdown("""
    <h2 style='
        color:white;
        font-weight:700;
    '>
    🚀 Advanced Export Options
    </h2>
    """, unsafe_allow_html=True)

    adv1, adv2 = st.columns(2)

    with adv1:

        json_data = df.to_json(
            orient="records",
            indent=4
        )

        st.download_button(
            "⬇ Download JSON",
            data=json_data,
            file_name="dataset_export.json",
            mime="application/json",
            use_container_width=True,
            key="json_export_btn"
        )

    with adv2:

        parquet_buffer = io.BytesIO()

        df.to_parquet(parquet_buffer, index=False)

        st.download_button(
            "⬇ Download Parquet",
            data=parquet_buffer.getvalue(),
            file_name="dataset_export.parquet",
            mime="application/octet-stream",
            use_container_width=True,
            key="parquet_export_btn"
        )

    st.write("")
    st.write("")

    # =====================================================
    # PDF ADD BUTTON
    # =====================================================

    if st.button(
        "📄 Add Export Summary To PDF",
        use_container_width=True,
        key="export_pdf_btn"
    ):

        export_summary = f"""
CSV Export Ready
Excel Export Ready
JSON Export Ready
Parquet Export Ready

Rows: {df.shape[0]}
Columns: {df.shape[1]}
"""

        st.session_state.pdf_sections.append({
            "type": "text",
            "title": "Export Center Summary",
            "content": export_summary
        })

        st.success("Export Summary Added To PDF ✅")