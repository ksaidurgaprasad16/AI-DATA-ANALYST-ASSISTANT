# =========================================================
# SQL ANALYTICS - DATABASE CONNECTION
# =========================================================

import streamlit as st
import sqlalchemy

from modules.SQL_ANALYTICS.utils import get_connection_string

# =========================================================
# MAIN FUNCTION
# =========================================================

def show_db_connection():

    st.markdown("""
    <h1 style='font-size:42px;font-weight:800;color:white;'>
    🔌 Database Connection
    </h1>
    """, unsafe_allow_html=True)

    st.caption("Connect to your database to begin analysis")
    st.write("")

    # =====================================================
    # DB TYPE SELECTOR — at the top, always visible
    # Issue #1 fix — shown before connection
    # =====================================================

    st.markdown("""
    <h2 style='color:white;font-weight:700;margin-bottom:8px;'>
    🗄️ Select Database Type
    </h2>
    """, unsafe_allow_html=True)

    db_type = st.selectbox(
        "Choose your database type",
        [
            "MySQL", "PostgreSQL", "SQL Server",
            "SQLite", "Snowflake", "BigQuery"
        ],
        key="db_type_selector"
    )

    # Always save to session state immediately on selection
    st.session_state.sql_db_type = db_type

    st.markdown(f"""
    <div style="
        background:linear-gradient(135deg,#064e3b,#065f46);
        padding:12px 18px;
        border-radius:12px;
        border:1px solid rgba(255,255,255,0.08);
        margin-bottom:24px;
    ">
        <p style="color:#6ee7b7;margin:0;font-size:14px;">
        ✅ AI SQL Generator and Chat will use
        <b>{db_type}</b> syntax
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    # =====================================================
    # SQLITE UPLOAD
    # =====================================================

    st.markdown("""
    <div style="
        background:linear-gradient(135deg,#1e1b4b,#312e81);
        padding:20px 25px;
        border-radius:18px;
        border:1px solid rgba(255,255,255,0.08);
        margin-bottom:24px;
    ">
        <h3 style="color:white;margin:0 0 8px 0;">
        💡 Quick Start — Upload SQLite DB
        </h3>
        <p style="color:#c4b5fd;margin:0;">
        Upload a .db or .sqlite file to get started
        instantly without any server credentials.
        </p>
    </div>
    """, unsafe_allow_html=True)

    sqlite_file = st.file_uploader(
        "Upload SQLite Database",
        type=["db", "sqlite", "sqlite3"],
        key="sqlite_upload"
    )

    if sqlite_file:

        import tempfile

        with tempfile.NamedTemporaryFile(
            delete=False, suffix=".db"
        ) as tmp:
            tmp.write(sqlite_file.read())
            tmp_path = tmp.name

        try:
            engine = sqlalchemy.create_engine(
                f"sqlite:///{tmp_path}"
            )
            st.session_state.sql_engine = engine
            st.session_state.sql_tables = (
                sqlalchemy.inspect(engine).get_table_names()
            )
            st.session_state.sql_db_type = "SQLite"

            st.success(
                f"✅ Connected! Found "
                f"{len(st.session_state.sql_tables)} tables."
            )

        except Exception as e:
            st.error(f"Connection failed: {e}")

    st.write("")

    # =====================================================
    # MANUAL SERVER CONNECTION
    # =====================================================

    st.markdown("""
    <h2 style='color:white;font-weight:700;'>
    🖥️ Connect to Database Server
    </h2>
    """, unsafe_allow_html=True)

    st.write("")

    col1, col2 = st.columns(2)

    with col1:
        database = st.text_input("Database Name")

    with col2:
        host = st.text_input("Host", value="localhost")

    col3, col4 = st.columns(2)

    with col3:
        port = st.text_input(
            "Port",
            value=(
                "3306" if db_type == "MySQL" else
                "5432" if db_type == "PostgreSQL" else
                "1433" if db_type == "SQL Server" else ""
            )
        )

    with col4:
        user = st.text_input("Username")

    password = st.text_input("Password", type="password")

    st.write("")

    if st.button(
        "🔌 Connect to Database",
        use_container_width=True,
        key="connect_db_btn"
    ):

        if not database:
            st.warning("Please enter a database name.")
            return

        with st.spinner("Connecting..."):

            try:
                conn_str = get_connection_string(
                    db_type, host, port,
                    user, password, database
                )

                engine = sqlalchemy.create_engine(conn_str)

                with engine.connect() as conn:
                    pass

                st.session_state.sql_engine = engine
                st.session_state.sql_tables = (
                    sqlalchemy.inspect(engine).get_table_names()
                )
                st.session_state.sql_db_type = db_type

                st.success(
                    f"✅ Connected to {db_type}! "
                    f"Found "
                    f"{len(st.session_state.sql_tables)} "
                    f"tables."
                )

            except Exception as e:
                st.error(f"Connection failed: {e}")

    # =====================================================
    # CONNECTION STATUS
    # =====================================================

    if st.session_state.sql_engine is not None:

        st.write("")

        current_db = st.session_state.get(
            "sql_db_type", "Unknown"
        )

        st.markdown(f"""
        <div style="
            background:linear-gradient(135deg,#064e3b,#065f46);
            padding:18px 24px;
            border-radius:14px;
            border:1px solid rgba(255,255,255,0.08);
        ">
            <h3 style="color:white;margin:0 0 6px 0;">
            ✅ {current_db} Database Connected
            </h3>
            <p style="color:#6ee7b7;margin:0;">
            {len(st.session_state.sql_tables)} tables:
            {", ".join(st.session_state.sql_tables[:8])}
            {"..." if len(st.session_state.sql_tables) > 8 else ""}
            </p>
        </div>
        """, unsafe_allow_html=True)