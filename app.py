# =========================================================
# ENTERPRISE AI ANALYTICS PLATFORM
# FINAL STABLE VERSION
# =========================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import requests
import io
import re

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak,
    Table,
    TableStyle
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Enterprise AI Analytics Platform",
    layout="wide"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.stApp{
    background-color:#020617;
    color:white;
}

section[data-testid="stSidebar"]{
    background-color:#111827;
}

h1,h2,h3,h4,h5,h6{
    color:white !important;
}

.stButton>button{
    background:linear-gradient(90deg,#2563eb,#9333ea);
    color:white;
    border:none;
    border-radius:10px;
    padding:10px 20px;
    font-weight:bold;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# API KEY
# =========================================================

OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]

# =========================================================
# AI FUNCTION
# =========================================================

@st.cache_data(show_spinner=False)
def ask_ai(prompt):

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    try:

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=120
        )

        result = response.json()

        if "choices" in result:
            return result["choices"][0]["message"]["content"]

        return str(result)

    except Exception as e:
        return str(e)

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("📊 AI Analyst Platform")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Overview",
        "🧹 AI Data Cleaning",
        "📊 Visualizations",
        "🧠 AI Insights",
        "🗄 SQL Generator",
        "📈 Power BI Assistant",
        "🧠 AI Analyst",
        "📄 PDF Reports",
        "📤 Export Center"
    ]
)

# =========================================================
# FILE UPLOAD
# =========================================================

uploaded_files = st.file_uploader(
    "📁 Upload CSV or Excel Files",
    type=["csv", "xlsx"],
    accept_multiple_files=True
)

df = None

if uploaded_files:

    selected_file = st.selectbox(
        "Select Dataset",
        [file.name for file in uploaded_files]
    )

    selected_uploaded_file = None

    for file in uploaded_files:

        if file.name == selected_file:
            selected_uploaded_file = file
            break

    try:

        if selected_uploaded_file.name.endswith(".csv"):

            df = pd.read_csv(selected_uploaded_file)

        else:

            df = pd.read_excel(selected_uploaded_file)

    except Exception as e:

        st.error(f"Error loading file: {e}")

# =========================================================
# OVERVIEW
# =========================================================

if page == "🏠 Overview":

    st.title("Enterprise AI-Powered Analytics Platform")

    if df is not None:

        numeric_cols = df.select_dtypes(include=np.number).columns.tolist()

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Rows", df.shape[0])
        col2.metric("Columns", df.shape[1])
        col3.metric("Missing Values", int(df.isnull().sum().sum()))
        col4.metric("Numeric Columns", len(numeric_cols))

        st.subheader("Dataset Preview")

        st.dataframe(df.head(20), use_container_width=True)

        numeric_summary = df.select_dtypes(include=np.number)

        if not numeric_summary.empty:

            st.subheader("Statistical Summary")

            stats_df = pd.DataFrame({
                "Mean": numeric_summary.mean(),
                "Median": numeric_summary.median(),
                "Minimum": numeric_summary.min(),
                "Maximum": numeric_summary.max(),
                "Std Deviation": numeric_summary.std()
            })

            st.dataframe(
                stats_df,
                use_container_width=True
            )

# =========================================================
# AI DATA CLEANING
# =========================================================

elif page == "🧹 AI Data Cleaning":

    if df is not None:

        st.header("🧹 AI Data Cleaning")

        cleaned_df = df.copy()

        col1, col2, col3 = st.columns(3)

        with col1:

            if st.button("Remove Duplicates"):

                before = cleaned_df.shape[0]

                cleaned_df = cleaned_df.drop_duplicates()

                after = cleaned_df.shape[0]

                st.success(f"Removed {before - after} duplicate rows.")

        with col2:

            if st.button("Handle Missing Values"):

                with st.spinner("Handling Missing Values..."):

                    for col in cleaned_df.columns:

                        if pd.api.types.is_numeric_dtype(cleaned_df[col]):

                            cleaned_df[col] = cleaned_df[col].fillna(
                                cleaned_df[col].mean()
                            )

                        else:

                            cleaned_df[col] = cleaned_df[col].fillna("Unknown")

                st.success("Missing values handled successfully.")

        with col3:

            if st.button("Fix Data Types"):

                with st.spinner("Fixing Data Types..."):

                    for col in cleaned_df.columns:

                        try:

                            cleaned_df[col] = pd.to_numeric(
                                cleaned_df[col],
                                errors="ignore"
                            )

                        except:
                            pass

                st.success("Data types optimized successfully.")

        st.subheader("Dataset Preview")

        st.dataframe(cleaned_df.head(20))

        csv = cleaned_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "⬇ Download Cleaned Dataset",
            data=csv,
            file_name="cleaned_dataset.csv",
            mime="text/csv"
        )

# =========================================================
# VISUALIZATIONS
# =========================================================

elif page == "📊 Visualizations":

    if df is not None:

        st.header("📊 Advanced Visualizations")

        numeric_cols = df.select_dtypes(include=np.number).columns.tolist()

        categorical_cols = df.select_dtypes(exclude=np.number).columns.tolist()

        viz_type = st.selectbox(
            "Select Visualization Type",
            [
                "Numerical Analysis",
                "Categorical Analysis",
                "Heatmap"
            ]
        )

        # =====================================================
        # NUMERICAL ANALYSIS
        # =====================================================

        if viz_type == "Numerical Analysis":

            if len(numeric_cols) > 0:

                selected_col = st.selectbox(
                    "Select Numeric Column",
                    numeric_cols
                )

                # ===== CHART TYPE OPTION ADDED BACK =====

                chart_type = st.selectbox(
                    "Select Chart Type",
                    [
                        "Histogram",
                        "Box Plot",
                        "Line Chart",
                        "Scatter Plot"
                    ]
                )

                if chart_type == "Histogram":

                    fig = px.histogram(df, x=selected_col)

                elif chart_type == "Box Plot":

                    fig = px.box(df, y=selected_col)

                elif chart_type == "Line Chart":

                    fig = px.line(df, y=selected_col)

                else:

                    fig = px.scatter(df, y=selected_col)

                st.plotly_chart(fig, use_container_width=True)

        # =====================================================
        # CATEGORICAL ANALYSIS
        # =====================================================

        elif viz_type == "Categorical Analysis":

            if len(categorical_cols) > 0:

                selected_col = st.selectbox(
                    "Select Category Column",
                    categorical_cols
                )

                # ===== CHART TYPE OPTION ADDED BACK =====

                chart_type = st.selectbox(
                    "Select Chart Type",
                    [
                        "Bar Chart",
                        "Pie Chart"
                    ]
                )

                value_counts = (
                    df[selected_col]
                    .astype(str)
                    .value_counts()
                    .reset_index()
                )

                value_counts.columns = ["Category", "Count"]

                if chart_type == "Bar Chart":

                    fig = px.bar(
                        value_counts,
                        x="Category",
                        y="Count"
                    )

                else:

                    fig = px.pie(
                        value_counts,
                        names="Category",
                        values="Count"
                    )

                st.plotly_chart(fig, use_container_width=True)

        # =====================================================
        # HEATMAP
        # =====================================================

        else:

            if len(numeric_cols) >= 2:

                corr = df[numeric_cols].corr()

                fig = px.imshow(
                    corr,
                    text_auto=True,
                    aspect="auto"
                )

                st.plotly_chart(fig, use_container_width=True)

# =========================================================
# AI INSIGHTS
# =========================================================

elif page == "🧠 AI Insights":

    if df is not None:

        st.header("🧠 Smart AI Insights")

        if st.button("Generate AI Insights"):

            prompt = f"""
Analyze this dataset deeply.

Generate:
- business insights
- trends
- anomalies
- risks
- opportunities
- recommendations
- predictions

Dataset Columns:
{list(df.columns)}

Dataset Sample:
{df.head(50).to_string()}
"""

            with st.spinner("Generating AI Insights..."):

                response = ask_ai(prompt)

            st.success("Insights Generated Successfully ✅")

            st.write(response)

# =========================================================
# SQL GENERATOR
# =========================================================

elif page == "🗄 SQL Generator":

    if df is not None:

        st.header("🗄 AI SQL Generator")

        sql_query = st.text_area(
            "Describe SQL Query",
            placeholder="Example: Show top 10 products by sales"
        )

        if st.button("Generate SQL Query"):

            prompt = f"""
Generate SQL query only.

Dataset Columns:
{list(df.columns)}

User Request:
{sql_query}
"""

            with st.spinner("Generating SQL Query..."):

                response = ask_ai(prompt)

            st.success("SQL Query Generated ✅")

            st.code(response, language="sql")

# =========================================================
# POWER BI ASSISTANT
# =========================================================

elif page == "📈 Power BI Assistant":

    if df is not None:

        st.header("📈 Power BI Dashboard Assistant")

        dashboard_prompt = f"""
Suggest:
- dashboard pages
- KPIs
- visuals
- slicers
- filters
- business metrics

Dataset Columns:
{list(df.columns)}
"""

        with st.spinner("Generating Power BI Recommendations..."):

            dashboard_response = ask_ai(dashboard_prompt)

        st.success("Power BI Recommendations Ready ✅")

        st.write(dashboard_response)

# =========================================================
# AI ANALYST
# =========================================================

elif page == "🧠 AI Analyst":

    if df is not None:

        st.header("🧠 AI Data Analyst")

        user_question = st.text_area(
            "Ask anything about your dataset",
            placeholder="Example: Summarize this dataset in 50 points"
        )

        if st.button("Analyze Dataset"):

            number_match = re.search(
                r'(\d+)\s*points?',
                user_question.lower()
            )

            if number_match:

                points_count = number_match.group(1)

            else:

                points_count = "20"

            prompt = f"""
IMPORTANT:
- Give EXACTLY {points_count} points.
- Give detailed professional bullet points.

Dataset Columns:
{list(df.columns)}

Dataset Sample:
{df.head(50).to_string()}

User Question:
{user_question}
"""

            with st.spinner("Analyzing Dataset..."):

                response = ask_ai(prompt)

            st.success("Analysis Complete ✅")

            st.write(response)

# =========================================================
# PDF REPORTS
# =========================================================

elif page == "📄 PDF Reports":

    if df is not None:

        st.header("📄 Enterprise PDF Reports")

        if st.button("Generate PDF Report"):

            with st.spinner("Generating Enterprise PDF Report..."):

                buffer = io.BytesIO()

                doc = SimpleDocTemplate(
                    buffer,
                    pagesize=letter
                )

                styles = getSampleStyleSheet()

                elements = []

                title = Paragraph(
                    "<b>Enterprise AI Analytics Report</b>",
                    styles["Title"]
                )

                elements.append(title)

                elements.append(Spacer(1, 20))

                intro = f"""
Rows: {df.shape[0]}<br/>
Columns: {df.shape[1]}<br/>
Missing Values: {df.isnull().sum().sum()}
"""

                elements.append(
                    Paragraph(
                        intro,
                        styles["BodyText"]
                    )
                )

                elements.append(PageBreak())

                preview_data = [list(df.columns)]

                for row in df.head(15).values.tolist():

                    preview_data.append(
                        [str(x) for x in row]
                    )

                preview_table = Table(preview_data)

                preview_table.setStyle(TableStyle([
                    ('BACKGROUND',(0,0),(-1,0),colors.darkblue),
                    ('TEXTCOLOR',(0,0),(-1,0),colors.white),
                    ('GRID',(0,0),(-1,-1),1,colors.black)
                ]))

                elements.append(preview_table)

                elements.append(PageBreak())

                ai_prompt = f"""
Generate a detailed enterprise analytics report.

Include:
- Executive Summary
- Insights
- Trends
- Risks
- Opportunities
- Recommendations
- Forecasts
- Conclusion

Dataset Columns:
{list(df.columns)}
"""

                ai_content = ask_ai(ai_prompt)

                sections = ai_content.split("\n")

                for section in sections:

                    if section.strip() != "":

                        elements.append(
                            Paragraph(
                                section,
                                styles["BodyText"]
                            )
                        )

                        elements.append(Spacer(1, 10))

                doc.build(elements)

                pdf = buffer.getvalue()

            st.success("PDF Report Generated Successfully ✅")

            st.download_button(
                "⬇ Download PDF Report",
                data=pdf,
                file_name="Enterprise_AI_Analytics_Report.pdf",
                mime="application/pdf"
            )

# =========================================================
# EXPORT CENTER
# =========================================================

elif page == "📤 Export Center":

    if df is not None:

        st.header("📤 Export Center")

        if st.button("Prepare Export Files"):

            with st.spinner("Preparing Export Files..."):

                csv = (
                    df.to_csv(index=False)
                    .encode("utf-8")
                )

                excel_buffer = io.BytesIO()

                with pd.ExcelWriter(
                    excel_buffer,
                    engine='openpyxl'
                ) as writer:

                    df.to_excel(
                        writer,
                        index=False
                    )

                summary_text = f"""
Dataset Rows: {df.shape[0]}
Dataset Columns: {df.shape[1]}
Missing Values: {df.isnull().sum().sum()}

Columns:
{list(df.columns)}
"""

            st.success("Export Files Ready ✅")

            st.download_button(
                "⬇ Download Dataset CSV",
                data=csv,
                file_name="dataset_export.csv",
                mime="text/csv"
            )

            st.download_button(
                "⬇ Download Dataset Excel",
                data=excel_buffer.getvalue(),
                file_name="dataset_export.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

            st.download_button(
                "⬇ Download Dataset Summary",
                data=summary_text,
                file_name="dataset_summary.txt",
                mime="text/plain"
            )