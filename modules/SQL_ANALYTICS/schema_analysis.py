# =========================================================
# SQL ANALYTICS - SCHEMA ANALYSIS
# =========================================================

import streamlit as st
import pandas as pd
import sqlalchemy

# =========================================================
# MAIN FUNCTION
# =========================================================

def show_schema_analysis():

    st.markdown("""
    <h1 style='font-size:42px;font-weight:800;color:white;'>
    📋 Schema Analysis
    </h1>
    """, unsafe_allow_html=True)

    st.caption("Explore your database structure")
    st.write("")

    if st.session_state.sql_engine is None:
        st.warning("⚠️ Please connect to a database first.")
        return

    engine = st.session_state.sql_engine
    tables = st.session_state.sql_tables

    if not tables:
        st.info("No tables found in this database.")
        return

    # =====================================================
    # TABLE SELECTOR
    # =====================================================

    selected_table = st.selectbox(
        "Select Table to Inspect",
        tables
    )

    st.write("")

    try:

        inspector = sqlalchemy.inspect(engine)
        columns = inspector.get_columns(selected_table)

        col_df = pd.DataFrame([{
            "Column": col["name"],
            "Type": str(col["type"]),
            "Nullable": col.get("nullable", True)
        } for col in columns])

        # =====================================================
        # ROW COUNT
        # =====================================================

        with engine.connect() as conn:
            row_count = conn.execute(
                sqlalchemy.text(
                    f"SELECT COUNT(*) FROM {selected_table}"
                )
            ).scalar()

        # =====================================================
        # METRIC CARDS
        # =====================================================

        c1, c2, c3 = st.columns(3)

        with c1:
            st.markdown(f"""
            <div style="
                background:linear-gradient(135deg,#172554,#1e3a8a);
                padding:24px;border-radius:18px;
                text-align:center;color:white;
            ">
                <div style="font-size:36px;font-weight:800;">
                {row_count:,}
                </div>
                <div style="font-size:16px;font-weight:600;
                margin-top:8px;">Total Rows</div>
            </div>
            """, unsafe_allow_html=True)

        with c2:
            st.markdown(f"""
            <div style="
                background:linear-gradient(135deg,#4c1d95,#6d28d9);
                padding:24px;border-radius:18px;
                text-align:center;color:white;
            ">
                <div style="font-size:36px;font-weight:800;">
                {len(columns)}
                </div>
                <div style="font-size:16px;font-weight:600;
                margin-top:8px;">Total Columns</div>
            </div>
            """, unsafe_allow_html=True)

        with c3:
            st.markdown(f"""
            <div style="
                background:linear-gradient(135deg,#115e59,#0f766e);
                padding:24px;border-radius:18px;
                text-align:center;color:white;
            ">
                <div style="font-size:36px;font-weight:800;">
                {len(tables)}
                </div>
                <div style="font-size:16px;font-weight:600;
                margin-top:8px;">Total Tables</div>
            </div>
            """, unsafe_allow_html=True)

        st.write("")
        st.write("")

        # =====================================================
        # ALL TABLES LIST
        # =====================================================

        st.markdown("""
        <h2 style='color:white;font-weight:700;'>
        🗂️ All Tables
        </h2>
        """, unsafe_allow_html=True)

        tables_df = pd.DataFrame({
            "Table Name": tables,
            "Index": range(1, len(tables) + 1)
        })

        st.dataframe(tables_df, use_container_width=True)

        st.write("")

        # =====================================================
        # COLUMN INFORMATION
        # =====================================================

        st.markdown("""
        <h2 style='color:white;font-weight:700;'>
        📌 Column Information
        </h2>
        """, unsafe_allow_html=True)

        st.dataframe(col_df, use_container_width=True)

        st.write("")

        # =====================================================
        # DATA PREVIEW
        # =====================================================

        st.markdown("""
        <h2 style='color:white;font-weight:700;'>
        📄 Data Preview
        </h2>
        """, unsafe_allow_html=True)

        with engine.connect() as conn:
            preview_df = pd.read_sql(
                f"SELECT * FROM {selected_table} LIMIT 25",
                conn
            )

        st.dataframe(preview_df, use_container_width=True)

        st.write("")

        # =====================================================
        # FOREIGN KEYS
        # =====================================================

        fks = inspector.get_foreign_keys(selected_table)

        if fks:

            st.markdown("""
            <h2 style='color:white;font-weight:700;'>
            🔗 Foreign Keys
            </h2>
            """, unsafe_allow_html=True)

            fk_df = pd.DataFrame([{
                "Column": str(fk["constrained_columns"]),
                "References Table": fk["referred_table"],
                "References Column": str(fk["referred_columns"])
            } for fk in fks])

            st.dataframe(fk_df, use_container_width=True)

        # =====================================================
        # ADD TO PDF
        # =====================================================

        st.write("")

        if st.button(
            "📄 Add Schema To PDF",
            use_container_width=True,
            key="schema_pdf_btn"
        ):

            schema_summary = f"""
Table: {selected_table}
Total Rows: {row_count:,}
Total Columns: {len(columns)}

Columns:
{col_df.to_string(index=False)}
"""

            st.session_state.pdf_sections.append({
                "type": "text",
                "title": f"Schema Analysis - {selected_table}",
                "content": schema_summary
            })

            st.success("Schema Added To PDF ✅")

    except Exception as e:
        st.error(f"Error loading schema: {e}")