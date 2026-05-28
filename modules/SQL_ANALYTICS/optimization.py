# =========================================================
# SQL ANALYTICS - QUERY RUNNER
# =========================================================

import streamlit as st
import pandas as pd
import numpy as np
import sqlalchemy

# =========================================================
# MAIN FUNCTION
# =========================================================

def show_query_runner():

    st.markdown("""
    <h1 style='font-size:42px;font-weight:800;color:white;'>
    ▶️ Query Runner
    </h1>
    """, unsafe_allow_html=True)

    st.caption("Write and execute SQL queries directly")
    st.write("")

    if st.session_state.sql_engine is None:
        st.warning("⚠️ Please connect to a database first.")
        return

    # =====================================================
    # QUERY INPUT
    # pre-fill with AI generated query if available
    # =====================================================

    query = st.text_area(
        "Write SQL Query",
        value=(
            st.session_state.sql_generated_query
            if st.session_state.sql_generated_query
            else ""
        ),
        placeholder="SELECT * FROM table_name LIMIT 100",
        height=200
    )

    st.write("")

    col1, col2 = st.columns([3, 1])

    with col1:

        if st.button(
            "▶️ Execute Query",
            use_container_width=True,
            key="execute_query_btn"
        ):

            if not query.strip():
                st.warning("Please write a query first.")
                return

            with st.spinner("Executing query..."):

                try:
                    with st.session_state.sql_engine.connect() as conn:
                        result_df = pd.read_sql(
                            sqlalchemy.text(query),
                            conn
                        )

                    st.session_state.sql_query_result = result_df

                    st.success(
                        f"✅ Query executed! "
                        f"{len(result_df)} rows returned."
                    )

                except Exception as e:
                    st.error(f"Query error: {e}")

    with col2:

        if st.button(
            "🗑 Clear",
            use_container_width=True,
            key="clear_query_btn"
        ):
            st.session_state.sql_query_result = None
            st.session_state.sql_generated_query = ""
            st.rerun()

    # =====================================================
    # RESULTS
    # =====================================================

    if st.session_state.sql_query_result is not None:

        result_df = st.session_state.sql_query_result

        st.write("")

        # =====================================================
        # RESULT METRICS
        # =====================================================

        r1, r2, r3 = st.columns(3)

        with r1:
            st.markdown(f"""
            <div style="
                background:linear-gradient(135deg,#172554,#1e3a8a);
                padding:20px;border-radius:16px;
                text-align:center;color:white;
            ">
                <div style="font-size:32px;font-weight:800;">
                {len(result_df):,}
                </div>
                <div style="font-size:14px;font-weight:600;
                margin-top:6px;">Rows Returned</div>
            </div>
            """, unsafe_allow_html=True)

        with r2:
            st.markdown(f"""
            <div style="
                background:linear-gradient(135deg,#4c1d95,#6d28d9);
                padding:20px;border-radius:16px;
                text-align:center;color:white;
            ">
                <div style="font-size:32px;font-weight:800;">
                {len(result_df.columns)}
                </div>
                <div style="font-size:14px;font-weight:600;
                margin-top:6px;">Columns</div>
            </div>
            """, unsafe_allow_html=True)

        with r3:
            numeric_count = len(
                result_df.select_dtypes(
                    include=np.number
                ).columns
            )
            st.markdown(f"""
            <div style="
                background:linear-gradient(135deg,#115e59,#0f766e);
                padding:20px;border-radius:16px;
                text-align:center;color:white;
            ">
                <div style="font-size:32px;font-weight:800;">
                {numeric_count}
                </div>
                <div style="font-size:14px;font-weight:600;
                margin-top:6px;">Numeric Columns</div>
            </div>
            """, unsafe_allow_html=True)

        st.write("")
        st.write("")

        # =====================================================
        # RESULTS TABLE
        # =====================================================

        st.markdown("""
        <h2 style='color:white;font-weight:700;'>
        📄 Query Results
        </h2>
        """, unsafe_allow_html=True)

        st.dataframe(result_df, use_container_width=True)

        st.write("")

        # =====================================================
        # ADD TO PDF
        # =====================================================

        if st.button(
            "📄 Add Results To PDF",
            use_container_width=True,
            key="query_results_pdf"
        ):

            summary = f"""
Query Results Summary:
Rows: {len(result_df)}
Columns: {list(result_df.columns)}

Sample Data:
{result_df.head(10).to_string()}
"""
            st.session_state.pdf_sections.append({
                "type": "text",
                "title": "SQL Query Results",
                "content": summary
            })

            st.success("Results Added To PDF ✅")