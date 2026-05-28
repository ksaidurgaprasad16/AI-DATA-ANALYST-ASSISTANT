# =========================================================
# SQL ANALYTICS - VISUALIZATIONS
# =========================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import copy

# =========================================================
# COLOR SEQUENCE
# =========================================================

COLORS = [
    "#3b82f6", "#ef4444", "#22c55e", "#a855f7",
    "#f59e0b", "#06b6d4", "#ec4899", "#84cc16",
    "#f97316", "#6366f1"
]

# =========================================================
# HELPERS
# =========================================================

def apply_dark_layout(fig, height=500):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#020617",
        plot_bgcolor="#020617",
        font=dict(color="white", size=14),
        title_font=dict(size=22),
        height=height,
        margin=dict(l=40, r=40, t=60, b=40)
    )
    return fig

def make_pdf_figure(fig):
    pdf_fig = copy.deepcopy(fig)
    pdf_fig.update_layout(
        template="plotly_white",
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(color="black", size=14),
        title_font=dict(size=22, color="black"),
        legend=dict(font=dict(color="black"))
    )
    pdf_fig.update_traces(
        marker=dict(line=dict(width=0.5, color="black"))
    )
    return pdf_fig

# =========================================================
# MAIN FUNCTION
# =========================================================

def show_sql_visualizations():

    st.markdown("""
    <h1 style='font-size:42px;font-weight:800;color:white;'>
    📊 SQL Visualizations
    </h1>
    """, unsafe_allow_html=True)

    st.caption("Visualize your query results")
    st.write("")

    if st.session_state.sql_engine is None:
        st.warning("⚠️ Please connect to a database first.")
        return

    if st.session_state.sql_query_result is None:
        st.info(
            "💡 Run a query first in "
            "Query Runner to visualize results."
        )
        return

    df = st.session_state.sql_query_result

    if df.empty:
        st.warning("Query result is empty. Run a different query.")
        return

    numeric_cols = df.select_dtypes(
        include=np.number
    ).columns.tolist()

    categorical_cols = df.select_dtypes(
        exclude=np.number
    ).columns.tolist()

    # =====================================================
    # CHART TYPE SELECTOR
    # =====================================================

    chart_type = st.selectbox(
        "Select Chart Type",
        [
            "Bar Chart",
            "Line Chart",
            "Pie Chart",
            "Scatter Plot",
            "Histogram"
        ]
    )

    st.write("")

    fig = None

    try:

        # =====================================================
        # BAR CHART
        # =====================================================

        if chart_type == "Bar Chart":

            if categorical_cols and numeric_cols:

                c1, c2 = st.columns(2)

                with c1:
                    x_col = st.selectbox(
                        "X Axis (Category)",
                        categorical_cols,
                        key="bar_x"
                    )

                with c2:
                    y_col = st.selectbox(
                        "Y Axis (Numeric)",
                        numeric_cols,
                        key="bar_y"
                    )

                fig = px.bar(
                    df, x=x_col, y=y_col,
                    color=x_col,
                    color_discrete_sequence=COLORS,
                    title=f"{y_col} by {x_col}"
                )

            else:
                st.warning(
                    "Bar chart needs at least 1 category "
                    "and 1 numeric column."
                )
                return

        # =====================================================
        # LINE CHART
        # =====================================================

        elif chart_type == "Line Chart":

            if numeric_cols:

                c1, c2 = st.columns(2)

                with c1:
                    y_col = st.selectbox(
                        "Y Axis (Numeric)",
                        numeric_cols,
                        key="line_y"
                    )

                with c2:
                    x_col_options = (
                        categorical_cols + numeric_cols
                    )
                    x_col = st.selectbox(
                        "X Axis (optional)",
                        ["Index"] + x_col_options,
                        key="line_x"
                    )

                if x_col == "Index":
                    fig = px.line(
                        df, y=y_col,
                        color_discrete_sequence=["#3b82f6"],
                        title=f"{y_col} Trend"
                    )
                else:
                    fig = px.line(
                        df, x=x_col, y=y_col,
                        color_discrete_sequence=["#3b82f6"],
                        title=f"{y_col} over {x_col}"
                    )

            else:
                st.warning(
                    "Line chart needs at least 1 numeric column."
                )
                return

        # =====================================================
        # PIE CHART
        # =====================================================

        elif chart_type == "Pie Chart":

            if categorical_cols and numeric_cols:

                c1, c2 = st.columns(2)

                with c1:
                    name_col = st.selectbox(
                        "Category Column",
                        categorical_cols,
                        key="pie_name"
                    )

                with c2:
                    val_col = st.selectbox(
                        "Value Column",
                        numeric_cols,
                        key="pie_val"
                    )

                fig = px.pie(
                    df, names=name_col, values=val_col,
                    color_discrete_sequence=COLORS,
                    title=f"{val_col} by {name_col}"
                )

            else:
                st.warning(
                    "Pie chart needs 1 category "
                    "and 1 numeric column."
                )
                return

        # =====================================================
        # SCATTER PLOT
        # =====================================================

        elif chart_type == "Scatter Plot":

            if len(numeric_cols) >= 2:

                c1, c2 = st.columns(2)

                with c1:
                    x_col = st.selectbox(
                        "X Axis",
                        numeric_cols,
                        key="scatter_x"
                    )

                with c2:
                    y_col = st.selectbox(
                        "Y Axis",
                        numeric_cols,
                        key="scatter_y"
                    )

                fig = px.scatter(
                    df, x=x_col, y=y_col,
                    color_discrete_sequence=["#a855f7"],
                    title=f"{x_col} vs {y_col}"
                )

            else:
                st.warning(
                    "Scatter plot needs at least "
                    "2 numeric columns."
                )
                return

        # =====================================================
        # HISTOGRAM
        # =====================================================

        elif chart_type == "Histogram":

            if numeric_cols:

                col = st.selectbox(
                    "Select Column",
                    numeric_cols,
                    key="hist_col"
                )

                fig = px.histogram(
                    df, x=col,
                    color_discrete_sequence=["#3b82f6"],
                    title=f"{col} Distribution"
                )

            else:
                st.warning(
                    "Histogram needs at least "
                    "1 numeric column."
                )
                return

        # =====================================================
        # RENDER CHART
        # =====================================================

        if fig:

            apply_dark_layout(fig)
            st.plotly_chart(fig, use_container_width=True)

            st.write("")

            if st.button(
                "📄 Add Chart To PDF",
                use_container_width=True,
                key="sql_chart_pdf"
            ):
                st.session_state.pdf_sections.append({
                    "type": "chart",
                    "title": f"SQL Chart - {chart_type}",
                    "figure": make_pdf_figure(fig)
                })
                st.success("Chart Added To PDF ✅")

    except Exception as e:
        st.error(f"Chart error: {e}")