# =========================================================
# POWER BI ANALYTICS WRAPPER
# =========================================================

import streamlit as st
from modules.POWER_BI_ANALYTICS.pbix_dashboard import show_pbix_dashboard

def show_pbix_analysis():
    show_pbix_dashboard()