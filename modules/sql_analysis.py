# =========================================================
# SQL ANALYTICS - MAIN ROUTER
# =========================================================

import streamlit as st

from modules.SQL_ANALYTICS.sql_dashboard import show_sql_dashboard

# =========================================================
# MAIN FUNCTION
# =========================================================

def show_sql_analytics():

    show_sql_dashboard()