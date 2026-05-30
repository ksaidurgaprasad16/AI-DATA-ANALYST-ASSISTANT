# =========================================================
# POWER BI ANALYTICS - EXPORT CENTER
# =========================================================

import streamlit as st

# =========================================================
# MAIN FUNCTION
# =========================================================

def show_pbix_export_center():

    st.markdown("""
    <h1 style='font-size:52px;font-weight:800;color:white;'>
    📤 Export Center
    </h1>
    """, unsafe_allow_html=True)

    st.caption("Export your Power BI analytics summaries")
    st.write("")

    if not st.session_state.get("pbix_columns"):
        st.warning("⚠️ Please upload a file in Dashboard first.")
        return

    columns = st.session_state.pbix_columns
    file_name = st.session_state.get("pbix_file_name", "Dataset")

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
        📁 File Loaded
        </h3>
        <p style="color:#c4b5fd;margin:0;">
        <b>{file_name}</b> &nbsp;•&nbsp;
        {len(columns)} columns
        </p>
    </div>
    """, unsafe_allow_html=True)

    # =====================================================
    # EXPORT CARDS
    # =====================================================

    col1, col2 = st.columns(2)

    # =====================================================
    # METADATA EXPORT
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
        🗂️ Metadata Summary
        </h2>
        <p style="color:#d1d5db;margin:0;">
        Download AI-generated metadata as TXT.
        </p>
        </div>
        """, unsafe_allow_html=True)

        metadata = st.session_state.get(
            "pbix_metadata_response", ""
        )

        if metadata:
            st.download_button(
                "⬇ Download Metadata",
                data=metadata,
                file_name="powerbi_metadata.txt",
                mime="text/plain",
                use_container_width=True,
                key="export_metadata"
            )
        else:
            st.info("Generate Metadata first.")

    # =====================================================
    # DAX EXPORT
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
        ⚡ DAX Measures
        </h2>
        <p style="color:#d1d5db;margin:0;">
        Download AI-generated DAX as TXT.
        </p>
        </div>
        """, unsafe_allow_html=True)

        dax = st.session_state.get("pbix_dax_response", "")

        if dax:
            st.download_button(
                "⬇ Download DAX",
                data=dax,
                file_name="powerbi_dax_measures.txt",
                mime="text/plain",
                use_container_width=True,
                key="export_dax"
            )
        else:
            st.info("Generate DAX Measures first.")

    st.write("")

    col3, col4 = st.columns(2)

    # =====================================================
    # RELATIONSHIP EXPORT
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
        🔗 Relationships
        </h2>
        <p style="color:#d1d5db;margin:0;">
        Download relationship map as TXT.
        </p>
        </div>
        """, unsafe_allow_html=True)

        relationships = st.session_state.get(
            "pbix_relationship_response", ""
        )

        if relationships:
            st.download_button(
                "⬇ Download Relationships",
                data=relationships,
                file_name="powerbi_relationships.txt",
                mime="text/plain",
                use_container_width=True,
                key="export_relationships"
            )
        else:
            st.info("Generate Relationship Map first.")

    # =====================================================
    # FULL SUMMARY EXPORT
    # =====================================================

    with col4:

        st.markdown("""
        <div style="
            background:#111827;
            padding:25px 25px 15px 25px;
            border-radius:18px 18px 0 0;
            border:1px solid rgba(255,255,255,0.08);
            border-bottom:none;
        ">
        <h2 style="color:white;margin-bottom:8px;">
        📋 Full Summary
        </h2>
        <p style="color:#d1d5db;margin:0;">
        Download complete analysis as TXT.
        </p>
        </div>
        """, unsafe_allow_html=True)

        full_summary = f"""
POWER BI ANALYTICS REPORT
==========================
File: {file_name}
Columns: {", ".join(columns)}

METADATA SUMMARY
================
{st.session_state.get("pbix_metadata_response", "Not generated yet.")}

DAX MEASURES
============
{st.session_state.get("pbix_dax_response", "Not generated yet.")}

RELATIONSHIP MAP
================
{st.session_state.get("pbix_relationship_response", "Not generated yet.")}
"""

        st.download_button(
            "⬇ Download Full Summary",
            data=full_summary,
            file_name="powerbi_full_summary.txt",
            mime="text/plain",
            use_container_width=True,
            key="export_full_summary"
        )

    st.write("")
    st.write("")

    # =====================================================
    # ADD TO PDF
    # =====================================================

    if st.button(
        "📄 Add Export Summary To PDF",
        use_container_width=True,
        key="export_summary_pdf"
    ):
        summary = f"""
File: {file_name}
Columns: {len(columns)}
Metadata Generated: {"Yes" if st.session_state.get("pbix_metadata_response") else "No"}
DAX Generated: {"Yes" if st.session_state.get("pbix_dax_response") else "No"}
Relationships Generated: {"Yes" if st.session_state.get("pbix_relationship_response") else "No"}
"""
        st.session_state.pbix_pdf_sections.append({
            "type": "text",
            "title": "Export Summary",
            "content": summary
        })
        st.success("Export Summary Added To PDF ✅")