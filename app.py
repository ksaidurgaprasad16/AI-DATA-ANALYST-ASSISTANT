import streamlit as st

from modules.file_analysis import show_file_analytics
from modules.sql_analysis import show_sql_analytics
from modules.pbix_analysis import show_pbix_analysis as show_pbix_analytics

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Enterprise AI Analytics Platform",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# SESSION STATE
# =========================================================

if "page" not in st.session_state:
    st.session_state.page = "Home"

# Separate PDF sections for each module — Issue #3
if "file_pdf_sections" not in st.session_state:
    st.session_state.file_pdf_sections = []

if "sql_pdf_sections" not in st.session_state:
    st.session_state.sql_pdf_sections = []

if "pbix_pdf_sections" not in st.session_state:
    st.session_state.pbix_pdf_sections = []

# Reset pdf_sections alias based on active page
if st.session_state.page == "File":
    st.session_state.pdf_sections = st.session_state.file_pdf_sections
elif st.session_state.page == "SQL":
    st.session_state.pdf_sections = st.session_state.sql_pdf_sections
elif st.session_state.page == "Power BI":
    st.session_state.pdf_sections = st.session_state.pbix_pdf_sections
else:
    if "pdf_sections" not in st.session_state:
        st.session_state.pdf_sections = []

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.main-title{
    font-size:40px;
    font-weight:900;
    color:white;
    line-height:1.1;
    margin-bottom:10px;
}

.subtitle{
    font-size:18px;
    color:#cbd5e1;
    margin-bottom:30px;
}

.metric-box{
    height:280px;
    border-radius:28px;
    padding:35px 20px;
    text-align:center;
    color:white;
    display:flex;
    flex-direction:column;
    justify-content:center;
    align-items:center;
}

.metric-number{
    font-size:48px;
    font-weight:900;
    line-height:1;
}

.metric-label{
    margin-top:20px;
    font-size:18px;
    font-weight:700;
}

.feature-card{
    background:#06122e;
    border:1px solid rgba(255,255,255,0.08);
    border-radius:28px;
    padding:35px;
    color:white;
    min-height:760px;
}

.feature-card h1{
    font-size:28px;
    font-weight:800;
    margin-bottom:25px;
}

.feature-card h4{
    font-size:17px;
    font-weight:700;
    margin-top:25px;
    margin-bottom:18px;
}

.feature-card ul{
    padding-left:24px;
}

.feature-card li{
    font-size:15px;
    line-height:2;
    margin-bottom:2px;
}

div.element-container:has(div.stButton) {
    width: 100% !important;
    margin-bottom: 10px !important;
}

div.stButton > button {
    width: 100% !important;
    height: 52px !important;
    min-height: 52px !important;
    max-height: 52px !important;
    background: linear-gradient(90deg,#2563eb,#3b82f6) !important;
    color: white !important;
    border: none !important;
    border-radius: 18px !important;
    padding: 0px 18px !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    margin-bottom: 0px !important;
    text-align: left !important;
    overflow: hidden !important;
    white-space: nowrap !important;
    transition: 0.3s !important;
}

div.stButton > button:hover {
    background: linear-gradient(90deg,#3b82f6,#60a5fa) !important;
    transform: scale(1.01);
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("""
    <h1 style='
        color:white;
        font-size:38px;
        font-weight:900;
        line-height:1.15;
        margin-bottom:40px;
    '>
    📊 Data Analytics
    </h1>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='section-card'>
    <h2 style='color:white;'>🚀 Platform Modules</h2>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🏠 Home"):
        st.session_state.page = "Home"
        st.rerun()

    if st.button("📁 File Analytics"):
        st.session_state.page = "File"
        st.session_state.pdf_sections = st.session_state.file_pdf_sections
        st.rerun()

    if st.button("🗄️ SQL Analytics"):
        st.session_state.page = "SQL"
        st.session_state.pdf_sections = st.session_state.sql_pdf_sections
        st.rerun()

    if st.button("📈 Power BI Analytics"):
        st.session_state.page = "Power BI"
        st.session_state.pdf_sections = st.session_state.pbix_pdf_sections
        st.rerun()

# =========================================================
# HOME PAGE
# =========================================================

if st.session_state.page == "Home":

    st.markdown("""
    <div class='main-title'>
    🚀 Enterprise AI Analytics Platform
    </div>

    <div class='subtitle'>
    Upload files • Connect databases • Analyze dashboards • Generate AI insights
    </div>
    """, unsafe_allow_html=True)

    st.write("")
    st.write("")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
        <div class='metric-box' style='background:linear-gradient(135deg,#2563eb,#1e3a8a);'>
            <div class='metric-number'>15+</div>
            <div class='metric-label'>Supported Files</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class='metric-box' style='background:linear-gradient(135deg,#9333ea,#5b21b6);'>
            <div class='metric-number'>AI</div>
            <div class='metric-label'>Powered Insights</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class='metric-box' style='background:linear-gradient(135deg,#0f766e,#115e59);'>
            <div class='metric-number'>SQL</div>
            <div class='metric-label'>Database Analytics</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div class='metric-box' style='background:linear-gradient(135deg,#db2777,#be185d);'>
            <div class='metric-number'>PBIX</div>
            <div class='metric-label'>Power BI Intelligence</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.write("")

    col1, col2, col3 = st.columns(3)

    # =====================================================
    # FILE ANALYTICS CARD — Issue #10 fixed
    # =====================================================

    with col1:
        st.markdown("""
        <div class="feature-card">

        <h1>📁 File Analytics</h1>

        <h4 style="color:#93c5fd;">Supported Files</h4>

        <ul>
            <li>CSV</li>
            <li>Excel</li>
            <li>JSON</li>
            <li>XML</li>
            <li>Parquet</li>
            <li>Feather</li>
        </ul>

        <h4 style="color:#93c5fd;">Features</h4>

        <ul>
            <li>Dataset Overview</li>
            <li>AI Data Cleaning</li>
            <li>Advanced Visualizations</li>
            <li>AI Insights</li>
            <li>SQL Generator</li>
            <li>AI Chatbot</li>
            <li>Power BI Recommendations</li>
            <li>PDF Reports</li>
            <li>Export Center</li>
        </ul>

        </div>
        """, unsafe_allow_html=True)

    # =====================================================
    # SQL ANALYTICS CARD — Issue #10 fixed
    # =====================================================

    with col2:
        st.markdown("""
        <div class="feature-card">

        <h1>🗄️ SQL Analytics</h1>

        <h4 style="color:#c4b5fd;">Supported Databases</h4>

        <ul>
            <li>MySQL</li>
            <li>PostgreSQL</li>
            <li>SQL Server</li>
            <li>SQLite</li>
            <li>Snowflake</li>
            <li>BigQuery</li>
        </ul>

        <h4 style="color:#c4b5fd;">Features</h4>

        <ul>
            <li>Database Connection</li>
            <li>Schema Analysis</li>
            <li>AI SQL Generator</li>
            <li>Query Runner</li>
            <li>SQL Visualizations</li>
            <li>AI SQL Chat</li>
            <li>PDF Reports</li>
            <li>Export Center</li>
        </ul>

        </div>
        """, unsafe_allow_html=True)

    # =====================================================
    # POWER BI CARD — Issue #10 fixed
    # =====================================================

    with col3:
        st.markdown("""
        <div class="feature-card">

        <h1>📈 Power BI Intelligence</h1>

        <h4 style="color:#f9a8d4;">Supported Files</h4>

        <ul>
            <li>CSV</li>
            <li>Excel</li>
        </ul>

        <h4 style="color:#f9a8d4;">Features</h4>

        <ul>
            <li>Metadata Extraction</li>
            <li>DAX Extraction</li>
            <li>Relationship Viewer</li>
            <li>Dashboard Recreation</li>
            <li>AI Power BI Assistant</li>
            <li>PDF Reports</li>
            <li>Export Center</li>
        </ul>

        </div>
        """, unsafe_allow_html=True)

    # =====================================================
    # DEVELOPER CREDIT — Issue #11
    # =====================================================

    st.write("")
    st.write("")

    st.markdown("""
    <div style="
        text-align:center;
        padding: 20px;
        margin-top: 20px;
        border-top: 1px solid rgba(255,255,255,0.08);
    ">
        <p style="
            color:#64748b;
            font-size:15px;
            font-weight:500;
            letter-spacing:1px;
        ">
        Designed & Developed by
        </p>
        <p style="
            color:#93c5fd;
            font-size:20px;
            font-weight:800;
            letter-spacing:2px;
            margin-top:4px;
        ">
        ✨ K SAI DURGA PRASAD ✨
        </p>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# FILE ANALYTICS PAGE
# =========================================================

elif st.session_state.page == "File":
    st.session_state.pdf_sections = st.session_state.file_pdf_sections
    show_file_analytics()

# =========================================================
# SQL PAGE
# =========================================================

elif st.session_state.page == "SQL":
    st.session_state.pdf_sections = st.session_state.sql_pdf_sections
    show_sql_analytics()

# =========================================================
# POWER BI PAGE
# =========================================================

elif st.session_state.page == "Power BI":
    st.session_state.pdf_sections = st.session_state.pbix_pdf_sections
    show_pbix_analytics()