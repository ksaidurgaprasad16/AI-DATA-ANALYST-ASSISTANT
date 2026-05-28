# =========================================================
# FILE ANALYTICS - VISUALIZATIONS
# =========================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import copy

# =========================================================
# HELPER - WHITE VERSION FOR PDF
# =========================================================

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
    # Fix: keep marker colors visible on white background
    try:
        pdf_fig.update_traces(marker=dict(line=dict(width=0.5, color="black")))
    except Exception:
        pass
    return pdf_fig

# =========================================================
# HELPER - DARK LAYOUT FOR SCREEN
# =========================================================

def apply_dark_layout(fig, height=550):
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

# =========================================================
# MAIN FUNCTION
# =========================================================

def show_visualizations(df):

    st.markdown("""
    <h1 style='font-size:52px;font-weight:800;color:white;'>
    📊 Advanced Visualizations
    </h1>
    """, unsafe_allow_html=True)

    st.caption("Interactive charts and visual analytics")
    st.write("")

    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    categorical_cols = df.select_dtypes(exclude=np.number).columns.tolist()

    viz_type = st.selectbox(
        "Select Visualization Type",
        ["Numerical Analysis", "Categorical Analysis", "Heatmap"]
    )

    st.write("")

    # =====================================================
    # NUMERICAL ANALYSIS
    # =====================================================

    if viz_type == "Numerical Analysis":

        if len(numeric_cols) > 0:

            c1, c2 = st.columns(2)

            with c1:
                selected_col = st.selectbox("Select Numeric Column", numeric_cols)

            with c2:
                chart_type = st.selectbox(
                    "Select Chart Type",
                    ["Histogram", "Box Plot", "Line Chart", "Scatter Plot"]
                )

            st.write("")

            if chart_type == "Histogram":
                fig = px.histogram(
                    df, x=selected_col,
                    color_discrete_sequence=["#3b82f6"],
                    title=f"{selected_col} Distribution"
                )

            elif chart_type == "Box Plot":
                fig = px.box(
                    df, y=selected_col,
                    color_discrete_sequence=["#ef4444"],
                    title=f"{selected_col} Box Plot"
                )

            elif chart_type == "Line Chart":
                fig = px.line(
                    df, y=selected_col,
                    color_discrete_sequence=["#22c55e"],
                    title=f"{selected_col} Trend"
                )

            else:
                second_col = st.selectbox(
                    "Select Second Numeric Column",
                    numeric_cols,
                    key="scatter_column"
                )
                fig = px.scatter(
                    df, x=selected_col, y=second_col,
                    color_discrete_sequence=["#a855f7"],
                    title=f"{selected_col} vs {second_col}"
                )

            apply_dark_layout(fig, height=550)
            st.plotly_chart(fig, use_container_width=True)

            if st.button(
                "📄 Add This Visualization To PDF",
                use_container_width=True,
                key="num_viz_pdf"
            ):
                st.session_state.pdf_sections.append({
                    "type": "chart",
                    "title": f"{chart_type} - {selected_col}",
                    "figure": make_pdf_figure(fig)
                })
                st.success("Visualization Added To PDF ✅")

        else:
            st.warning("No numeric columns found.")

    # =====================================================
    # CATEGORICAL ANALYSIS
    # =====================================================

    elif viz_type == "Categorical Analysis":

        if len(categorical_cols) > 0:

            c1, c2 = st.columns(2)

            with c1:
                selected_col = st.selectbox("Select Category Column", categorical_cols)

            with c2:
                chart_type = st.selectbox(
                    "Select Chart Type",
                    ["Bar Chart", "Pie Chart"]
                )

            value_counts = (
                df[selected_col]
                .astype(str)
                .value_counts()
                .head(10)
                .reset_index()
            )
            value_counts.columns = ["Category", "Count"]

            st.write("")

            # use explicit color sequence for bar charts
            COLORS = [
                "#3b82f6","#ef4444","#22c55e","#a855f7",
                "#f59e0b","#06b6d4","#ec4899","#84cc16",
                "#f97316","#6366f1"
            ]

            if chart_type == "Bar Chart":
                fig = px.bar(
                    value_counts, x="Category", y="Count",
                    color="Category",
                    color_discrete_sequence=COLORS,
                    title=f"Top Categories in {selected_col}"
                )
            else:
                fig = px.pie(
                    value_counts, names="Category", values="Count",
                    color_discrete_sequence=COLORS,
                    title=f"{selected_col} Distribution"
                )

            apply_dark_layout(fig, height=550)
            st.plotly_chart(fig, use_container_width=True)

            if st.button(
                "📄 Add Category Visualization To PDF",
                use_container_width=True,
                key="cat_viz_pdf"
            ):
                st.session_state.pdf_sections.append({
                    "type": "chart",
                    "title": f"{chart_type} - {selected_col}",
                    "figure": make_pdf_figure(fig)
                })
                st.success("Visualization Added To PDF ✅")

        else:
            st.warning("No categorical columns found.")

    # =====================================================
    # HEATMAP
    # =====================================================

    else:

        if len(numeric_cols) >= 2:

            correlation = df[numeric_cols].corr()

            fig = px.imshow(
                correlation,
                text_auto=True,
                aspect="auto",
                color_continuous_scale="Blues",
                title="Correlation Heatmap"
            )

            apply_dark_layout(fig, height=700)
            st.plotly_chart(fig, use_container_width=True)

            if st.button(
                "📄 Add Heatmap To PDF",
                use_container_width=True,
                key="heatmap_pdf"
            ):
                st.session_state.pdf_sections.append({
                    "type": "chart",
                    "title": "Correlation Heatmap",
                    "figure": make_pdf_figure(fig)
                })
                st.success("Heatmap Added To PDF ✅")

        else:
            st.warning("At least 2 numeric columns required.")