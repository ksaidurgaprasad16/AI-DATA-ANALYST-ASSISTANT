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
import tempfile

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak,
    Table,
    TableStyle,
    Image
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
# PDF SESSION STORAGE
# =========================================================

if "pdf_sections" not in st.session_state:

    st.session_state.pdf_sections = []

# =========================================================
# AI FUNCTION
# =========================================================

def ask_ai(prompt):

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "openrouter/free",
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
            timeout=60
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

        # ==========================================
        # SESSION STATE FOR CLEANED DATA
        # ==========================================

        current_file_name = selected_uploaded_file.name

        if (
            "cleaned_df" not in st.session_state
            or "current_file" not in st.session_state
            or st.session_state.current_file != current_file_name
        ):

            st.session_state.cleaned_df = df.copy()

            st.session_state.current_file = current_file_name

        cleaned_df = st.session_state.cleaned_df

        col1, col2, col3 = st.columns(3)

        # ==========================================
        # REMOVE DUPLICATES
        # ==========================================

        with col1:

            if st.button("Remove Duplicates"):

                before = cleaned_df.shape[0]

                cleaned_df = cleaned_df.drop_duplicates()

                after = cleaned_df.shape[0]

                st.session_state.cleaned_df = cleaned_df

                st.success(f"Removed {before - after} duplicate rows.")

        # ==========================================
        # HANDLE MISSING VALUES
        # ==========================================

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

                st.session_state.cleaned_df = cleaned_df

                st.success("Missing values handled successfully.")

        # ==========================================
        # FIX DATA TYPES
        # ==========================================

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

                st.session_state.cleaned_df = cleaned_df

                st.success("Data types optimized successfully.")

        # ==========================================
        # PREVIEW CLEANED DATA
        # ==========================================

        st.subheader("Cleaned Dataset Preview")

        st.dataframe(
            st.session_state.cleaned_df.head(20),
            use_container_width=True
        )

        # ==========================================
        # DOWNLOAD CLEANED DATASET
        # ==========================================

        csv = (
            st.session_state.cleaned_df
            .to_csv(index=False)
            .encode("utf-8")
        )

        st.download_button(
            "⬇ Download Cleaned Dataset",
            data=csv,
            file_name="cleaned_dataset.csv",
            mime="text/csv"
        )

# =========================================================
# VISUALIZATIONS
# =========================================================

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

                    fig = px.histogram(
                        df,
                        x=selected_col,
                        color_discrete_sequence=["#3b82f6"],
                        title=f"{selected_col} Distribution"
                    )

                elif chart_type == "Box Plot":

                    fig = px.box(
                        df,
                        y=selected_col,
                        color_discrete_sequence=["#ef4444"],
                        title=f"{selected_col} Box Plot"
                    )

                elif chart_type == "Line Chart":

                    fig = px.line(
                        df,
                        y=selected_col,
                        color_discrete_sequence=["#22c55e"],
                        title=f"{selected_col} Trend"
                    )

                else:

                    fig = px.scatter(
                        df,
                        y=selected_col,
                        color_discrete_sequence=["#a855f7"],
                        title=f"{selected_col} Scatter Plot"
                    )

                # =================================================
                # PROFESSIONAL STYLING
                # =================================================

                fig.update_layout(
                    template="plotly_dark",
                    paper_bgcolor="#020617",
                    plot_bgcolor="#020617",
                    font=dict(
                        color="white",
                        size=14
                    ),
                    title_font=dict(
                        size=22
                    ),
                    height=500,
                    margin=dict(
                        l=40,
                        r=40,
                        t=60,
                        b=40
                    )
                )

                st.plotly_chart(fig, use_container_width=True)

                if st.button("Add This Visualization To PDF"):

                    st.session_state.pdf_sections.append({
                        "type": "chart",
                        "title": f"{chart_type} - {selected_col}",
                        "figure": fig
                    })

                    st.success("Visualization Added To PDF ✅")

        # =====================================================
        # CATEGORICAL ANALYSIS
        # =====================================================

        elif viz_type == "Categorical Analysis":

            if len(categorical_cols) > 0:

                selected_col = st.selectbox(
                    "Select Category Column",
                    categorical_cols
                )

                chart_type = st.selectbox(
                    "Select Chart Type",
                    [
                        "Bar Chart",
                        "Pie Chart"
                    ]
                )

                # =================================================
                # LIMIT TOP 10 CATEGORIES
                # =================================================

                value_counts = (
                    df[selected_col]
                    .astype(str)
                    .value_counts()
                    .head(10)
                    .reset_index()
                )

                value_counts.columns = ["Category", "Count"]

                if chart_type == "Bar Chart":

                    fig = px.bar(
                        value_counts,
                        x="Category",
                        y="Count",
                        color="Category",
                        title=f"Top Categories in {selected_col}"
                    )

                else:

                    fig = px.pie(
                        value_counts,
                        names="Category",
                        values="Count",
                        title=f"{selected_col} Distribution"
                    )

                # =================================================
                # PROFESSIONAL STYLING
                # =================================================

                fig.update_layout(
                    template="plotly_dark",
                    paper_bgcolor="#020617",
                    plot_bgcolor="#020617",
                    font=dict(
                        color="white",
                        size=14
                    ),
                    title_font=dict(
                        size=22
                    ),
                    height=500,
                    margin=dict(
                        l=40,
                        r=40,
                        t=60,
                        b=40
                    )
                )

                st.plotly_chart(fig, use_container_width=True)

                if st.button("Add This Visualization To PDF"):

                    st.session_state.pdf_sections.append({
                        "type": "chart",
                        "title": f"{chart_type} - {selected_col}",
                        "figure": fig
                    })

                    st.success("Visualization Added To PDF ✅")

        # =====================================================
        # HEATMAP
        # =====================================================

        else:

            if len(numeric_cols) >= 2:

                corr = df[numeric_cols].corr()

                fig = px.imshow(
                    corr,
                    text_auto=True,
                    aspect="auto",
                    color_continuous_scale="Blues",
                    title="Correlation Heatmap"
                )

                # =================================================
                # PROFESSIONAL STYLING
                # =================================================

                fig.update_layout(
                    template="plotly_dark",
                    paper_bgcolor="#020617",
                    plot_bgcolor="#020617",
                    font=dict(
                        color="white",
                        size=14
                    ),
                    title_font=dict(
                        size=22
                    ),
                    height=600,
                    margin=dict(
                        l=40,
                        r=40,
                        t=60,
                        b=40
                    )
                )

                st.plotly_chart(fig, use_container_width=True)

                if st.button("Add Heatmap To PDF"):

                    st.session_state.pdf_sections.append({
                        "type": "chart",
                        "title": "Correlation Heatmap",
                        "figure": fig
                    })

                    st.success("Heatmap Added To PDF ✅")
# =========================================================
# AI INSIGHTS
# =========================================================

elif page == "🧠 AI Insights":

    if df is not None:

        st.header("🧠 Smart AI Insights")

        if "ai_insights_response" not in st.session_state:
            st.session_state.ai_insights_response = ""

        if st.button("Generate AI Insights"):

            full_prompt = f"""
You are a professional AI Data Analyst.

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
{df.head(25).to_string()}

Give professional, business-level insights.
"""

            with st.spinner("Generating AI Insights..."):

                response = ask_ai(full_prompt)

            st.session_state.ai_insights_response = response

        if st.session_state.ai_insights_response != "":

            st.success("Insights Generated Successfully ✅")

            st.write(st.session_state.ai_insights_response)

            if st.button("Add Insights To PDF"):

                st.session_state.pdf_sections.append({
                    "type": "text",
                    "title": "AI Insights",
                    "content": st.session_state.ai_insights_response
                })

                st.success("AI Insights Added To PDF ✅")

# =========================================================
# POWER BI ASSISTANT
# =========================================================

# =========================================================
# POWER BI ASSISTANT
# =========================================================

elif page == "📈 Power BI Assistant":

    if df is not None:

        st.header("📈 Power BI Dashboard Assistant")

        if "powerbi_response" not in st.session_state:
            st.session_state.powerbi_response = ""

        if st.button("Generate Power BI Recommendations"):

            dashboard_prompt = f"""
You are a senior Power BI consultant.

Generate clean professional dashboard recommendations.

STRICT RULES:
- Create EACH section ONLY ONCE
- Do NOT repeat headings
- Keep spacing compact
- Keep answers concise
- Use markdown tables only
- No HTML
- No extra paragraphs
- No repeated KPI sections

FORMAT EXACTLY:

# Dashboard Pages
| Section | Explanation |

# KPIs
| KPI | Business Use |

# Visuals
| Visual | Purpose |

# Slicers
| Slicer | Why Needed |

# Filters
| Filter | Business Purpose |

# Business Metrics
| Metric | Explanation |

# Dashboard Mapping
| Dashboard Page | KPIs | Visuals | Slicers |

Dashboard Mapping should act like a dashboard mind map.

Dataset Columns:
{list(df.columns)}
"""

            with st.spinner("Generating Power BI Recommendations..."):

                dashboard_response = ask_ai(dashboard_prompt)

            st.session_state.powerbi_response = dashboard_response

        if st.session_state.powerbi_response != "":

            st.success("Power BI Recommendations Ready ✅")

            st.markdown(st.session_state.powerbi_response)

            if st.button("Add Power BI Suggestions To PDF"):

                st.session_state.pdf_sections.append({
                    "type": "text",
                    "title": "Power BI Recommendations",
                    "content": st.session_state.powerbi_response
                })

                st.success(
                    "Power BI Recommendations Added To PDF ✅"
                )


# =========================================================
# SQL GENERATOR
# =========================================================

elif page == "🗄 SQL Generator":

    if df is not None:

        st.header("🗄 AI SQL Generator")

        if "sql_response" not in st.session_state:
            st.session_state.sql_response = ""

        sql_query = st.text_area(
            "Describe SQL Query",
            placeholder="Example: Show top 10 products by sales"
        )

        if st.button("Generate SQL Query"):

            prompt = f"""
You are an expert SQL generator.

Generate ONLY valid SQL query.

Do NOT explain anything.
Do NOT add comments.
Do NOT add markdown.
Do NOT add reasoning.
Do NOT add text before or after query.

Dataset Columns:
{list(df.columns)}

User Request:
{sql_query}
"""

            with st.spinner("Generating SQL Query..."):

                response = ask_ai(prompt)

            st.session_state.sql_response = response

        if st.session_state.sql_response != "":

            st.success("SQL Query Generated ✅")

            st.code(
                st.session_state.sql_response,
                language="sql"
            )

            if st.button("Add SQL To PDF"):

                st.session_state.pdf_sections.append({
                    "type": "text",
                    "title": "SQL Query",
                    "content": st.session_state.sql_response
                })

                st.success("SQL Added To PDF ✅")

# =========================================================
# AI ANALYST
# =========================================================

elif page == "🧠 AI Analyst":

    if df is not None:

        st.header("🧠 AI Data Analyst")

        # ==========================================
        # SESSION STATES
        # ==========================================

        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        if "latest_ai_response" not in st.session_state:
            st.session_state.latest_ai_response = ""

        if "latest_user_question" not in st.session_state:
            st.session_state.latest_user_question = ""

        # ==========================================
        # RESET CHAT WHEN NEW FILE IS UPLOADED
        # ==========================================

        current_file_name = selected_uploaded_file.name

        if (
            "chat_file" not in st.session_state
            or st.session_state.chat_file != current_file_name
        ):

            st.session_state.chat_history = []

            st.session_state.chat_file = current_file_name

        # ==========================================
        # CLEAR CHAT BUTTON
        # ==========================================

        if st.button("Clear Chat"):

            st.session_state.chat_history = []

            st.session_state.latest_ai_response = ""

            st.session_state.latest_user_question = ""

            st.rerun()

        # ==========================================
        # DISPLAY CHAT HISTORY
        # ==========================================

        for chat in st.session_state.chat_history:

            with st.chat_message(chat["role"]):

                st.markdown(chat["content"])

        # ==========================================
        # USER INPUT
        # ==========================================

        user_question = st.chat_input(
            "Ask anything about your dataset..."
        )

        if user_question:

            # ==========================================
            # SHOW USER MESSAGE
            # ==========================================

            st.chat_message("user").markdown(user_question)

            st.session_state.chat_history.append({
                "role": "user",
                "content": user_question
            })

            # ==========================================
            # CREATE CONVERSATION MEMORY
            # ==========================================

            conversation_history = ""

            for msg in st.session_state.chat_history:

                conversation_history += (
                    f"{msg['role']}: {msg['content']}\n"
                )

            # ==========================================
            # AI PROMPT
            # ==========================================

            prompt = f"""
You are an expert AI Data Analyst.

Continue the conversation naturally.

Answer ONLY based on the user's question.
Do not unnecessarily analyze the dataset
unless the question is dataset-related.

Dataset Columns:
{list(df.columns)}

Dataset Sample:
{df.head(25).to_string()}

Conversation History:
{conversation_history}

Current User Question:
{user_question}

Give detailed, professional, accurate answers.
"""

            # ==========================================
            # AI RESPONSE
            # ==========================================

            with st.spinner("Analyzing Dataset..."):

                response = ask_ai(prompt)

            # ==========================================
            # STORE LATEST RESPONSE
            # ==========================================

            st.session_state.latest_ai_response = response

            st.session_state.latest_user_question = user_question

            # ==========================================
            # SHOW AI RESPONSE
            # ==========================================

            with st.chat_message("assistant"):

                st.markdown(response)

            st.session_state.chat_history.append({
                "role": "assistant",
                "content": response
            })

        # ==========================================
        # ADD TO PDF BUTTON
        # ==========================================

        if st.session_state.latest_ai_response != "":

            if st.button("Add This Chat To PDF"):

                st.session_state.pdf_sections.append({
                    "type": "text",
                    "title": (
                        f"AI Analyst Question: "
                        f"{st.session_state.latest_user_question}"
                    ),
                    "content": st.session_state.latest_ai_response
                })

                st.success("AI Analyst Response Added To PDF ✅")


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
                    pagesize=letter,
                    rightMargin=40,
                    leftMargin=40,
                    topMargin=35,
                    bottomMargin=25
                )

                styles = getSampleStyleSheet()

                # =================================================
                # PROFESSIONAL PDF STYLES
                # =================================================

                title_style = styles["Title"]
                title_style.fontSize = 24
                title_style.leading = 28
                title_style.textColor = colors.HexColor("#0f172a")
                title_style.spaceAfter = 10

                heading_style = styles["Heading2"]
                heading_style.fontSize = 17
                heading_style.leading = 20
                heading_style.spaceAfter = 8
                heading_style.spaceBefore = 6
                heading_style.textColor = colors.HexColor("#1d4ed8")

                body_style = styles["BodyText"]
                body_style.fontSize = 10
                body_style.leading = 15
                body_style.spaceAfter = 4

                elements = []

                # =====================================================
                # TITLE
                # =====================================================

                title = Paragraph(
                    "<b>Enterprise AI Analytics Report</b>",
                    title_style
                )

                elements.append(title)

                elements.append(Spacer(1, 12))

                # =====================================================
                # DATASET OVERVIEW
                # =====================================================

                numeric_cols = df.select_dtypes(include=np.number)

                overview_data = [
                    ["Metric", "Value"],
                    ["Rows", str(df.shape[0])],
                    ["Columns", str(df.shape[1])],
                    ["Missing Values", str(df.isnull().sum().sum())],
                    ["Numeric Columns", str(len(numeric_cols.columns))]
                ]

                overview_table = Table(
                    overview_data,
                    colWidths=[200, 220]
                )

                overview_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1e293b")),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 10),

                    ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                    ('TOPPADDING', (0, 0), (-1, -1), 6),
                    ('BOTTOMPADDING', (0, 1), (-1, -1), 6),

                    ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
                    ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),

                    ('GRID', (0, 0), (-1, -1), 0.7, colors.grey),

                    ('ROWBACKGROUNDS', (0, 1), (-1, -1),
                     [colors.whitesmoke, colors.beige])
                ]))

                elements.append(
                    Paragraph(
                        "<b>Dataset Overview</b>",
                        heading_style
                    )
                )

                elements.append(overview_table)

                elements.append(Spacer(1, 10))

                # =====================================================
                # DATASET COLUMNS
                # =====================================================

                columns_text = ", ".join(df.columns.tolist())

                elements.append(
                    Paragraph(
                        f"<b>Dataset Columns:</b> {columns_text}",
                        body_style
                    )
                )

                elements.append(Spacer(1, 8))

                # =====================================================
                # USER SELECTED PDF CONTENT
                # =====================================================

                for item in st.session_state.pdf_sections:

                    elements.append(PageBreak())

                    section_title = Paragraph(
                        f"<b>{item['title']}</b>",
                        heading_style
                    )

                    elements.append(section_title)

                    elements.append(Spacer(1, 8))

                    # =================================================
                    # TEXT CONTENT
                    # =================================================

                    if item["type"] == "text":

                        clean_content = item["content"]

                        clean_content = re.sub(
                            r"#+",
                            "",
                            clean_content
                        )

                        clean_content = re.sub(
                            r"-{3,}",
                            "",
                            clean_content
                        )

                        clean_content = clean_content.replace(
                            "<br>",
                            "\n"
                        )

                        clean_content = clean_content.replace(
                            "<br/>",
                            "\n"
                        )

                        # =============================================
                        # TABLE FORMATTING
                        # =============================================

                        if "|" in clean_content:

                            sections = clean_content.split("\n\n")

                            for sec in sections:

                                lines = sec.split("\n")

                                table_data = []

                                for line in lines:

                                    if "|" in line:

                                        cols = [
                                            c.strip()
                                            for c in line.split("|")
                                            if c.strip() != ""
                                        ]

                                        if len(cols) >= 2:

                                            table_data.append(cols[:2])

                                if len(table_data) > 1:

                                    pdf_table = Table(
                                        table_data,
                                        colWidths=[180, 260]
                                    )

                                    pdf_table.setStyle(TableStyle([
                                        ('BACKGROUND', (0, 0), (-1, 0),
                                         colors.HexColor("#1e293b")),

                                        ('TEXTCOLOR', (0, 0), (-1, 0),
                                         colors.white),

                                        ('FONTNAME', (0, 0), (-1, 0),
                                         'Helvetica-Bold'),

                                        ('FONTSIZE', (0, 0), (-1, -1), 9),

                                        ('TOPPADDING', (0, 0), (-1, -1), 5),
                                        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),

                                        ('BACKGROUND', (0, 1), (0, -1),
                                         colors.whitesmoke),

                                        ('TEXTCOLOR', (0, 1), (0, -1),
                                         colors.black),

                                        ('TEXTCOLOR', (1, 1), (1, -1),
                                         colors.HexColor("#16a34a")),

                                        ('GRID', (0, 0), (-1, -1),
                                         0.7, colors.grey),

                                        ('ROWBACKGROUNDS', (0, 1), (-1, -1),
                                         [colors.whitesmoke, colors.beige])
                                    ]))

                                    elements.append(pdf_table)

                                    elements.append(Spacer(1, 8))

                        else:

                            clean_content = clean_content.replace(
                                "\n",
                                "<br/>"
                            )

                            elements.append(
                                Paragraph(
                                    clean_content,
                                    body_style
                                )
                            )

                    # =================================================
                    # CHART CONTENT
                    # =================================================

                    elif item["type"] == "chart":

                        with tempfile.NamedTemporaryFile(
                            suffix=".png",
                            delete=False
                        ) as tmpfile:

                            item["figure"].write_image(
                                tmpfile.name,
                                scale=2
                            )

                            chart_img = Image(
                                tmpfile.name,
                                width=500,
                                height=300
                            )

                            elements.append(chart_img)

                            elements.append(Spacer(1, 8))

                # =====================================================
                # BUILD PDF
                # =====================================================

                doc.build(elements)

                pdf = buffer.getvalue()

            st.success("PDF Report Generated Successfully ✅")

            st.download_button(
                "⬇ Download PDF Report",
                data=pdf,
                file_name="Enterprise_AI_Analytics_Report.pdf",
                mime="application/pdf"
            )

        # =====================================================
        # CLEAR PDF CONTENT
        # =====================================================

        if st.button("Clear PDF Content"):

            st.session_state.pdf_sections = []

            st.success("PDF Content Cleared ✅")

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
st.markdown("""
<hr style='margin-top:50px; margin-bottom:10px;'>

<div style='text-align:left; color:gray; font-size:14px;'>
Developed by <b>K Sai Durga Prasad</b>
</div>
""", unsafe_allow_html=True)