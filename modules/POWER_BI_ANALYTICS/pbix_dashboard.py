# =========================================================
# POWER BI ANALYTICS - MAIN DASHBOARD ROUTER
# =========================================================

import streamlit as st
import pandas as pd

from modules.POWER_BI_ANALYTICS.utils import init_pbix_session_state
from modules.POWER_BI_ANALYTICS.metadata_reader import show_metadata_reader
from modules.POWER_BI_ANALYTICS.dax_extractor import show_dax_extractor
from modules.POWER_BI_ANALYTICS.relationship_viewer import show_relationship_viewer
from modules.POWER_BI_ANALYTICS.ai_chat import show_pbix_ai_chat
from modules.POWER_BI_ANALYTICS.pdf_reports import show_pbix_pdf_reports
from modules.POWER_BI_ANALYTICS.export_center import show_pbix_export_center

# =========================================================
# MAIN FUNCTION
# =========================================================

def show_pbix_dashboard():

    init_pbix_session_state()

    st.markdown("""
    <h1 style='font-size:52px;font-weight:800;color:white;'>
    📈 Power BI Intelligence
    </h1>
    """, unsafe_allow_html=True)

    st.caption(
        "Upload datasets • AI metadata • DAX formulas • "
        "Relationship maps • Dashboard recommendations"
    )

    st.write("")

    # =====================================================
    # SIDEBAR
    # =====================================================

    with st.sidebar:

        st.markdown("---")

        st.markdown("""
        <div style="
            padding:15px;
            border-radius:18px;
            background:linear-gradient(135deg,#111827,#1e293b);
            border:1px solid rgba(255,255,255,0.08);
            margin-bottom:18px;
        ">
            <h3 style="margin:0;color:white;">
            📈 Power BI Workspace
            </h3>
        </div>
        """, unsafe_allow_html=True)

        if st.button(
            "🏠 Back To Home",
            use_container_width=True,
            key="pbix_back_home"
        ):
            st.session_state.page = "Home"
            st.rerun()

        st.write("")

        pbix_page = st.radio(
            "Choose Section",
            [
                "📋 Metadata Reader",
                "🧮 DAX Extractor",
                "🔗 Relationship Viewer",
                "🤖 AI Power BI Chat",
                "📄 PDF Reports",
                "📤 Export Center"
            ]
        )

    # =====================================================
    # FILE UPLOADER — CSV / Excel
    # =====================================================

    uploaded_file = st.file_uploader(
        "📁 Upload your dataset (CSV or Excel)",
        type=["csv", "xlsx"],
        key="pbix_file_uploader"
    )

    df = None

    if uploaded_file:

        try:
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)

            # only update session state if new file
            if (
                "pbix_file_name" not in st.session_state
                or st.session_state.pbix_file_name != uploaded_file.name
            ):
                st.session_state.pbix_file_name = uploaded_file.name
                st.session_state.pbix_columns = df.columns.tolist()
                st.session_state.pbix_df_shape = df.shape
                # clear previous AI responses on new file
                st.session_state.pbix_metadata_response = ""
                st.session_state.pbix_dax_response = ""
                st.session_state.pbix_relationship_response = ""
                st.session_state.pbix_chat_history = []

            st.markdown(f"""
            <div style="
                background:linear-gradient(135deg,#064e3b,#065f46);
                padding:14px 20px;
                border-radius:14px;
                border:1px solid rgba(255,255,255,0.08);
                margin-bottom:16px;
            ">
                <p style="color:#6ee7b7;margin:0;font-size:14px;">
                ✅ <b>{uploaded_file.name}</b> loaded —
                {df.shape[0]:,} rows &nbsp;•&nbsp;
                {df.shape[1]} columns &nbsp;•&nbsp;
                Columns: {", ".join(df.columns.tolist()[:5])}
                {"..." if len(df.columns) > 5 else ""}
                </p>
            </div>
            """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Error loading file: {e}")
            return

    else:
        st.info(
            "👆 Upload a CSV or Excel file to begin "
            "Power BI analysis."
        )

    # =====================================================
    # PAGE ROUTING
    # =====================================================

    if pbix_page == "📋 Metadata Reader":
        show_metadata_reader()

    elif pbix_page == "🧮 DAX Extractor":
        show_dax_extractor()

    elif pbix_page == "🔗 Relationship Viewer":
        show_relationship_viewer()

    elif pbix_page == "🤖 AI Power BI Chat":
        show_pbix_ai_chat()

    elif pbix_page == "📄 PDF Reports":
        show_pbix_pdf_reports()

    elif pbix_page == "📤 Export Center":
        show_pbix_export_center()