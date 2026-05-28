# =========================================================
# SQL ANALYTICS - MAIN DASHBOARD ROUTER
# =========================================================

import streamlit as st

from modules.SQL_ANALYTICS.utils import init_sql_session_state
from modules.SQL_ANALYTICS.db_connection import show_db_connection
from modules.SQL_ANALYTICS.schema_analysis import show_schema_analysis
from modules.SQL_ANALYTICS.sql_generator import show_ai_sql_generator
from modules.SQL_ANALYTICS.optimization import show_query_runner
from modules.SQL_ANALYTICS.visualizations import show_sql_visualizations
from modules.SQL_ANALYTICS.ai_chat import show_ai_sql_chat
from modules.SQL_ANALYTICS.pdf_reports import show_sql_pdf_reports
from modules.SQL_ANALYTICS.export_center import show_sql_export_center

# =========================================================
# MAIN FUNCTION
# =========================================================

def show_sql_dashboard():

    # =====================================================
    # INITIALIZE SESSION STATE
    # =====================================================

    init_sql_session_state()

    # =====================================================
    # HEADER
    # =====================================================

    st.markdown("""
    <h1 style='font-size:52px;font-weight:800;color:white;'>
    🗄️ SQL Analytics
    </h1>
    """, unsafe_allow_html=True)

    st.caption(
        "Connect databases • Run queries • "
        "AI-powered SQL insights"
    )

    st.write("")

    # =====================================================
    # SIDEBAR NAVIGATION
    # =====================================================

    with st.sidebar:

        st.markdown("---")

        st.markdown("""
        <div style="
            padding:15px;
            border-radius:18px;
            background:linear-gradient(
                135deg,#111827,#1e293b
            );
            border:1px solid rgba(255,255,255,0.08);
            margin-bottom:18px;
        ">
            <h3 style="margin:0;color:white;">
            🗄️ SQL Workspace
            </h3>
        </div>
        """, unsafe_allow_html=True)

        if st.button(
            "🏠 Back To Home",
            use_container_width=True,
            key="sql_back_home"
        ):
            st.session_state.page = "Home"
            st.rerun()

        st.write("")

        sql_page = st.radio(
            "Choose Section",
            [
                "🔌 Database Connection",
                "📋 Schema Analysis",
                "🤖 AI SQL Generator",
                "▶️ Query Runner",
                "📊 SQL Visualizations",
                "💬 AI SQL Chat",
                "📄 PDF Reports",
                "📤 Export Center"
            ]
        )

    # =====================================================
    # PAGE ROUTING
    # =====================================================

    if sql_page == "🔌 Database Connection":
        show_db_connection()

    elif sql_page == "📋 Schema Analysis":
        show_schema_analysis()

    elif sql_page == "🤖 AI SQL Generator":
        show_ai_sql_generator()

    elif sql_page == "▶️ Query Runner":
        show_query_runner()

    elif sql_page == "📊 SQL Visualizations":
        show_sql_visualizations()

    elif sql_page == "💬 AI SQL Chat":
        show_ai_sql_chat()

    elif sql_page == "📄 PDF Reports":
        show_sql_pdf_reports()

    elif sql_page == "📤 Export Center":
        show_sql_export_center()