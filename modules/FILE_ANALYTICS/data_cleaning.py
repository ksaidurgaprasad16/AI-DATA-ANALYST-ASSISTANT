# =========================================================
# FILE ANALYTICS - AI DATA CLEANING
# =========================================================

import streamlit as st
import pandas as pd

# =========================================================
# MAIN FUNCTION
# =========================================================

def show_data_cleaning(df, uploaded_file):

    # =====================================================
    # HEADER
    # =====================================================

    st.markdown("""
    <h1 style='
        font-size:52px;
        font-weight:800;
        color:white;
    '>
    🧹 AI Data Cleaning
    </h1>
    """, unsafe_allow_html=True)

    st.caption(
        "Smart dataset cleaning and preprocessing"
    )

    st.write("")

    # =====================================================
    # SESSION STATE
    # =====================================================

    current_file_name = uploaded_file.name

    if (
        "cleaned_df" not in st.session_state
        or "current_cleaning_file" not in st.session_state
        or st.session_state.current_cleaning_file != current_file_name
    ):

        st.session_state.cleaned_df = df.copy()

        st.session_state.current_cleaning_file = current_file_name

    cleaned_df = st.session_state.cleaned_df

    # =====================================================
    # METRICS
    # =====================================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Rows", cleaned_df.shape[0])

    with col2:
        st.metric("Columns", cleaned_df.shape[1])

    with col3:
        st.metric(
            "Missing Values",
            int(cleaned_df.isnull().sum().sum())
        )

    with col4:
        st.metric(
            "Duplicate Rows",
            int(cleaned_df.duplicated().sum())
        )

    st.write("")

    # =====================================================
    # CLEANING ACTIONS
    # =====================================================

    c1, c2, c3 = st.columns(3)

    with c1:

        if st.button(
            "🗑 Remove Duplicates",
            use_container_width=True,
            key="remove_duplicates"
        ):

            before = cleaned_df.shape[0]
            cleaned_df = cleaned_df.drop_duplicates()
            after = cleaned_df.shape[0]
            st.session_state.cleaned_df = cleaned_df
            st.success(f"Removed {before - after} duplicate rows.")

    with c2:

        if st.button(
            "⚡ Handle Missing Values",
            use_container_width=True,
            key="missing_values"
        ):

            with st.spinner("Handling Missing Values..."):

                for col in cleaned_df.columns:

                    if pd.api.types.is_numeric_dtype(cleaned_df[col]):
                        cleaned_df[col] = cleaned_df[col].fillna(
                            cleaned_df[col].mean()
                        )
                    else:
                        cleaned_df[col] = cleaned_df[col].fillna("Unknown")

            st.session_state.cleaned_df = cleaned_df
            st.success("Missing values handled successfully.")

    with c3:

        if st.button(
            "🔧 Fix Data Types",
            use_container_width=True,
            key="fix_data_types"
        ):

            with st.spinner("Fixing Data Types..."):

                for col in cleaned_df.columns:
                    try:
                        cleaned_df[col] = pd.to_numeric(
                            cleaned_df[col],
                            errors="ignore"
                        )
                    except:
                        pass

            st.session_state.cleaned_df = cleaned_df
            st.success("Data types optimized successfully.")

    st.write("")

    # =====================================================
    # CLEANED DATA PREVIEW
    # =====================================================

    st.markdown("""
    <h2 style='color:white; font-weight:700;'>
    📄 Cleaned Dataset Preview
    </h2>
    """, unsafe_allow_html=True)

    st.dataframe(
        st.session_state.cleaned_df.head(25),
        use_container_width=True
    )

    st.write("")

    # =====================================================
    # DATASET INFO - FIXED: headers and tables together
    # =====================================================

    info_col1, info_col2 = st.columns(2)

    with info_col1:

        st.markdown("""
        <h3 style="
            color:white;
            background:#111827;
            padding:15px 20px;
            border-radius:15px 15px 0 0;
            border:1px solid rgba(255,255,255,0.08);
            margin-bottom:0;
        ">
        📊 Column Data Types
        </h3>
        """, unsafe_allow_html=True)

        dtypes_df = pd.DataFrame({
            "Column": cleaned_df.columns,
            "Data Type": cleaned_df.dtypes.astype(str)
        })

        st.dataframe(dtypes_df, use_container_width=True)

    with info_col2:

        st.markdown("""
        <h3 style="
            color:white;
            background:#111827;
            padding:15px 20px;
            border-radius:15px 15px 0 0;
            border:1px solid rgba(255,255,255,0.08);
            margin-bottom:0;
        ">
        ⚠ Missing Values Summary
        </h3>
        """, unsafe_allow_html=True)

        missing_df = pd.DataFrame({
            "Column": cleaned_df.columns,
            "Missing Values": cleaned_df.isnull().sum().values
        })

        st.dataframe(missing_df, use_container_width=True)

    st.write("")

    # =====================================================
    # DOWNLOAD CLEANED DATASET
    # =====================================================

    csv = (
        st.session_state.cleaned_df
        .to_csv(index=False)
        .encode("utf-8")
    )

    st.download_button(
        "⬇ Download Cleaned Dataset",
        data=csv,
        file_name="cleaned_dataset.csv",
        mime="text/csv",
        use_container_width=True
    )

    st.write("")

    # =====================================================
    # ADD TO PDF
    # =====================================================

    if st.button(
        "📄 Add Cleaning Report To PDF",
        use_container_width=True,
        key="cleaning_pdf"
    ):

        cleaning_summary = f"""
Rows: {cleaned_df.shape[0]}
Columns: {cleaned_df.shape[1]}
Missing Values: {cleaned_df.isnull().sum().sum()}
Duplicate Rows: {cleaned_df.duplicated().sum()}
"""

        st.session_state.pdf_sections.append({
            "type": "text",
            "title": "AI Data Cleaning Report",
            "content": cleaning_summary
        })

        st.success("Cleaning Report Added To PDF ✅")