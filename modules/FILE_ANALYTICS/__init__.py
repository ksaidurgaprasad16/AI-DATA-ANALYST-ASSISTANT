# =========================================================
# FILE ANALYTICS MODULE
# =========================================================

import streamlit as st
import pandas as pd

from modules.FILE_ANALYTICS.overview import show_overview
from modules.FILE_ANALYTICS.visualizations import show_visualizations
from modules.FILE_ANALYTICS.data_cleaning import show_data_cleaning
from modules.FILE_ANALYTICS.ai_insights import show_ai_insights
from modules.FILE_ANALYTICS.sql_generator import show_sql_generator
from modules.FILE_ANALYTICS.ai_chat import show_ai_chat
from modules.FILE_ANALYTICS.export_center import show_export_center
from modules.FILE_ANALYTICS.pdf_reports import show_pdf_reports
from modules.FILE_ANALYTICS.power_bi_recommendations import (
    show_power_bi_recommendations
)

# =========================================================
# MAIN ROUTER
# =========================================================

def show_file_analytics():

    st.title("📁 Enterprise File Analytics")
    st.caption("Upload • Analyze • Visualize • AI Insights")
    st.write("")

    # =====================================================
    # SIDEBAR — shown always, even before upload
    # Issue #2 fix
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
            🚀 Analytics Workspace
            </h3>
        </div>
        """, unsafe_allow_html=True)

        if st.button(
            "🏠 Back To Home",
            use_container_width=True,
            key="back_home_btn"
        ):
            st.session_state.page = "Home"
            st.rerun()

        st.write("")

        page = st.radio(
            "Choose Section",
            [
                "🏠 Overview",
                "🧹 AI Data Cleaning",
                "📊 Visualizations",
                "🧠 AI Insights",
                "🗄 SQL Generator",
                "🤖 AI Chatbot",
                "📈 Power BI Recommendations",
                "📄 PDF Reports",
                "📤 Export Center"
            ]
        )

    # =====================================================
    # FILE UPLOADER
    # =====================================================

    uploaded_files = st.file_uploader(
        "📁 Upload CSV or Excel Files",
        type=["csv", "xlsx"],
        accept_multiple_files=True
    )

    if not uploaded_files:

        st.info("👆 Upload datasets to begin analysis.")

        # =====================================================
        # Show PDF Reports even without upload
        # =====================================================

        if page == "📄 PDF Reports":
            show_pdf_reports(None)

        return

    # =====================================================
    # SELECT FILE
    # =====================================================

    selected_file = st.selectbox(
        "Select Dataset",
        [file.name for file in uploaded_files]
    )

    selected_uploaded_file = None

    for file in uploaded_files:
        if file.name == selected_file:
            selected_uploaded_file = file
            break

    # =====================================================
    # LOAD DATAFRAME
    # =====================================================

    try:
        if selected_uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(selected_uploaded_file)
        else:
            df = pd.read_excel(selected_uploaded_file)

    except Exception as e:
        st.error(f"Error loading file: {e}")
        return

    # =====================================================
    # PAGE ROUTING
    # =====================================================

    if page == "🏠 Overview":
        show_overview(df)

    elif page == "🧹 AI Data Cleaning":
        show_data_cleaning(df, selected_uploaded_file)

    elif page == "📊 Visualizations":
        show_visualizations(df)

    elif page == "🧠 AI Insights":
        show_ai_insights(df)

    elif page == "🗄 SQL Generator":
        show_sql_generator(df)

    elif page == "🤖 AI Chatbot":
        show_ai_chat(df, selected_uploaded_file)

    elif page == "📈 Power BI Recommendations":
        show_power_bi_recommendations(df)

    elif page == "📄 PDF Reports":
        show_pdf_reports(df)

    elif page == "📤 Export Center":
        show_export_center(df)