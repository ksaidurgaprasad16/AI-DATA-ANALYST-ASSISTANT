# =========================================================
# FILE ANALYTICS - OVERVIEW
# =========================================================

import streamlit as st
import pandas as pd
import numpy as np

# =========================================================
# OVERVIEW PAGE
# =========================================================

def show_overview(df):

    st.title("🏠 Dataset Overview")

    st.caption(
        "Complete dataset structure and high-level insights"
    )

    st.write("")

    # =====================================================
    # DATA CALCULATIONS
    # =====================================================

    total_rows = df.shape[0]
    total_columns = df.shape[1]
    missing_values = int(df.isnull().sum().sum())
    numeric_columns = len(df.select_dtypes(include=np.number).columns)
    text_columns = len(df.select_dtypes(exclude=np.number).columns)
    duplicate_rows = int(df.duplicated().sum())

    # =====================================================
    # ROW 1 - inline styles, no CSS classes
    # =====================================================

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(f"""
        <div style="
            background:linear-gradient(135deg,#172554,#1e3a8a);
            padding:28px;
            border-radius:24px;
            text-align:center;
            color:white;
            box-shadow:0 0 25px rgba(0,0,0,0.35);
            margin-bottom:20px;
        ">
            <div style="font-size:42px;font-weight:800;margin-bottom:10px;">
                {total_rows:,}
            </div>
            <div style="font-size:20px;font-weight:600;">
                Total Rows
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div style="
            background:linear-gradient(135deg,#4c1d95,#6d28d9);
            padding:28px;
            border-radius:24px;
            text-align:center;
            color:white;
            box-shadow:0 0 25px rgba(0,0,0,0.35);
            margin-bottom:20px;
        ">
            <div style="font-size:42px;font-weight:800;margin-bottom:10px;">
                {total_columns}
            </div>
            <div style="font-size:20px;font-weight:600;">
                Total Columns
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div style="
            background:linear-gradient(135deg,#115e59,#0f766e);
            padding:28px;
            border-radius:24px;
            text-align:center;
            color:white;
            box-shadow:0 0 25px rgba(0,0,0,0.35);
            margin-bottom:20px;
        ">
            <div style="font-size:42px;font-weight:800;margin-bottom:10px;">
                {missing_values:,}
            </div>
            <div style="font-size:20px;font-weight:600;">
                Missing Values
            </div>
        </div>
        """, unsafe_allow_html=True)

    # =====================================================
    # ROW 2
    # =====================================================

    c4, c5, c6 = st.columns(3)

    with c4:
        st.markdown(f"""
        <div style="
            background:linear-gradient(135deg,#9a3412,#ea580c);
            padding:28px;
            border-radius:24px;
            text-align:center;
            color:white;
            box-shadow:0 0 25px rgba(0,0,0,0.35);
            margin-bottom:20px;
        ">
            <div style="font-size:42px;font-weight:800;margin-bottom:10px;">
                {numeric_columns}
            </div>
            <div style="font-size:20px;font-weight:600;">
                Numeric Columns
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c5:
        st.markdown(f"""
        <div style="
            background:linear-gradient(135deg,#9d174d,#db2777);
            padding:28px;
            border-radius:24px;
            text-align:center;
            color:white;
            box-shadow:0 0 25px rgba(0,0,0,0.35);
            margin-bottom:20px;
        ">
            <div style="font-size:42px;font-weight:800;margin-bottom:10px;">
                {text_columns}
            </div>
            <div style="font-size:20px;font-weight:600;">
                Text Columns
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c6:
        st.markdown(f"""
        <div style="
            background:linear-gradient(135deg,#374151,#6b7280);
            padding:28px;
            border-radius:24px;
            text-align:center;
            color:white;
            box-shadow:0 0 25px rgba(0,0,0,0.35);
            margin-bottom:20px;
        ">
            <div style="font-size:42px;font-weight:800;margin-bottom:10px;">
                {duplicate_rows}
            </div>
            <div style="font-size:20px;font-weight:600;">
                Duplicate Rows
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.write("")

    # =====================================================
    # DATA PREVIEW
    # =====================================================

    st.subheader("📄 Dataset Preview")

    st.dataframe(
        df.head(25),
        use_container_width=True
    )

    # =====================================================
    # COLUMN DETAILS
    # =====================================================

    st.subheader("📌 Column Information")

    column_info = pd.DataFrame({
        "Column": df.columns,
        "Data Type": df.dtypes.astype(str),
        "Missing Values": df.isnull().sum().values
    })

    st.dataframe(
        column_info,
        use_container_width=True
    )

    # =====================================================
    # STATISTICS
    # =====================================================

    numeric_df = df.select_dtypes(include=np.number)

    if not numeric_df.empty:

        st.subheader("📊 Statistical Summary")

        stats_df = pd.DataFrame({
            "Mean": numeric_df.mean(),
            "Median": numeric_df.median(),
            "Minimum": numeric_df.min(),
            "Maximum": numeric_df.max(),
            "Std Dev": numeric_df.std()
        })

        st.dataframe(
            stats_df,
            use_container_width=True
        )