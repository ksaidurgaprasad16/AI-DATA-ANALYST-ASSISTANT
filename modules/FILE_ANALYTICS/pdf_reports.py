# =========================================================
# FILE ANALYTICS - PDF REPORTS
# =========================================================

import streamlit as st
import pandas as pd
import numpy as np
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
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib.enums import TA_LEFT

PAGE_WIDTH = 532

# =========================================================
# CLEAN TEXT FOR PDF
# =========================================================

def clean_pdf_text(text):
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"\*(.+?)\*", r"\1", text)
    text = text.replace("■", "-")
    text = text.replace("•", "-")
    text = text.replace("─", "-")
    text = text.replace("━", "-")
    text = text.replace("–", "-")
    text = text.replace("—", "-")
    text = text.replace("👤", "")
    text = text.replace("🤖", "")
    text = text.replace("✅", "")
    text = text.replace("⚠", "")
    text = text.replace("💡", "")
    text = text.encode("latin-1", errors="replace").decode("latin-1")
    text = text.replace("<", "&lt;").replace(">", "&gt;")
    return text

# =========================================================
# HELPERS
# =========================================================

def wrap_cell(text, style):
    safe = clean_pdf_text(str(text))
    return Paragraph(safe, style)

def _build_pdf_table(table_data, cell_style):

    if not table_data:
        return None

    max_cols = max(len(row) for row in table_data)

    header_cell_style = ParagraphStyle(
        "header_cell_style",
        fontSize=8,
        leading=12,
        textColor=colors.white,
        alignment=TA_LEFT,
        wordWrap="CJK"
    )

    normalized = []
    for i, row in enumerate(table_data):
        padded = list(row) + [""] * (max_cols - len(row))
        style = header_cell_style if i == 0 else cell_style
        wrapped = [
            wrap_cell(cell, style)
            for cell in padded[:max_cols]
        ]
        normalized.append(wrapped)

    col_width = PAGE_WIDTH / max_cols
    col_widths = [col_width] * max_cols

    pdf_table = Table(
        normalized,
        colWidths=col_widths,
        repeatRows=1
    )

    pdf_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1e293b")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1),
         [colors.whitesmoke, colors.HexColor("#f0f4f8")]),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))

    return pdf_table

# =========================================================
# MAIN FUNCTION
# =========================================================

def show_pdf_reports(df):

    st.markdown("""
    <h1 style='font-size:52px;font-weight:800;color:white;'>
    📄 Enterprise PDF Reports
    </h1>
    """, unsafe_allow_html=True)

    st.caption("Generate professional AI analytics reports")
    st.write("")

    if "pdf_sections" not in st.session_state:
        st.session_state.pdf_sections = []

    st.markdown("""
    <h2 style='color:white; font-weight:700;'>
    📚 Current PDF Sections
    </h2>
    """, unsafe_allow_html=True)

    if len(st.session_state.pdf_sections) == 0:
        st.info("No sections added yet.")
    else:
        for idx, item in enumerate(
            st.session_state.pdf_sections, start=1
        ):
            st.markdown(f"""
            <div style="
                background:#111827;
                padding:18px;
                border-radius:14px;
                border:1px solid rgba(255,255,255,0.08);
                margin-bottom:12px;
            ">
            <b style="color:white;">{idx}. {item['title']}</b>
            </div>
            """, unsafe_allow_html=True)

    st.write("")
    st.write("")

    if st.button(
        "🚀 Generate Enterprise PDF Report",
        use_container_width=True,
        key="generate_pdf_report"
    ):

        if df is None and len(st.session_state.pdf_sections) == 0:
            st.warning("No content to generate PDF.")
            return

        with st.spinner("Generating PDF Report..."):

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
            body_style.fontSize = 9
            body_style.leading = 14
            body_style.spaceAfter = 4

            cell_style = ParagraphStyle(
                "cell_style",
                fontSize=8,
                leading=12,
                textColor=colors.black,
                alignment=TA_LEFT,
                wordWrap="CJK"
            )

            elements = []

            elements.append(
                Paragraph(
                    "<b>Enterprise AI Analytics Report</b>",
                    title_style
                )
            )
            elements.append(Spacer(1, 12))

            if df is not None:

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
                    colWidths=[266, 266]
                )

                overview_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0),
                     colors.HexColor("#1e293b")),
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
                    Paragraph("<b>Dataset Overview</b>", heading_style)
                )
                elements.append(overview_table)
                elements.append(Spacer(1, 10))

                columns_text = ", ".join(df.columns.tolist())
                elements.append(
                    Paragraph(
                        f"<b>Dataset Columns:</b> {columns_text}",
                        body_style
                    )
                )
                elements.append(Spacer(1, 8))

            for item in st.session_state.pdf_sections:

                elements.append(PageBreak())

                elements.append(
                    Paragraph(
                        f"<b>{clean_pdf_text(item['title'])}</b>",
                        heading_style
                    )
                )
                elements.append(Spacer(1, 8))

                if item["type"] == "text":

                    content = item["content"]
                    content = re.sub(r"-{3,}", "", content)
                    lines = content.split("\n")
                    table_buffer = []

                    for line in lines:

                        stripped = line.strip()

                        if not stripped:
                            if table_buffer:
                                t = _build_pdf_table(
                                    table_buffer, cell_style
                                )
                                if t:
                                    elements.append(t)
                                    elements.append(Spacer(1, 8))
                                table_buffer = []
                            continue

                        if re.match(r"^\|[-| :]+\|$", stripped):
                            continue

                        if stripped.startswith("#"):
                            if table_buffer:
                                t = _build_pdf_table(
                                    table_buffer, cell_style
                                )
                                if t:
                                    elements.append(t)
                                    elements.append(Spacer(1, 8))
                                table_buffer = []
                            heading_text = re.sub(
                                r"^#+\s*", "", stripped
                            )
                            heading_text = clean_pdf_text(heading_text)
                            elements.append(Spacer(1, 6))
                            elements.append(
                                Paragraph(
                                    f"<b>{heading_text}</b>",
                                    heading_style
                                )
                            )
                            elements.append(Spacer(1, 4))

                        elif "|" in stripped:
                            cols = [
                                c.strip()
                                for c in stripped.split("|")
                                if c.strip() != ""
                            ]
                            if cols:
                                table_buffer.append(cols)

                        else:
                            if table_buffer:
                                t = _build_pdf_table(
                                    table_buffer, cell_style
                                )
                                if t:
                                    elements.append(t)
                                    elements.append(Spacer(1, 8))
                                table_buffer = []

                            clean = clean_pdf_text(stripped)
                            elements.append(
                                Paragraph(clean, body_style)
                            )
                            elements.append(Spacer(1, 3))

                    if table_buffer:
                        t = _build_pdf_table(
                            table_buffer, cell_style
                        )
                        if t:
                            elements.append(t)
                            elements.append(Spacer(1, 8))

                elif item["type"] == "chart":

                    try:
                        with tempfile.NamedTemporaryFile(
                            suffix=".png",
                            delete=False
                        ) as tmpfile:

                            item["figure"].write_image(
                                tmpfile.name,
                                scale=2,
                                width=800,
                                height=450
                            )

                            chart_img = Image(
                                tmpfile.name,
                                width=PAGE_WIDTH,
                                height=int(PAGE_WIDTH * 450 / 800)
                            )

                            elements.append(chart_img)
                            elements.append(Spacer(1, 8))

                    except Exception as e:
                        elements.append(
                            Paragraph(
                                f"[Chart could not be rendered: {e}]",
                                body_style
                            )
                        )

            doc.build(elements)
            pdf = buffer.getvalue()

        st.success("PDF Report Generated Successfully ✅")

        st.download_button(
            "⬇ Download PDF Report",
            data=pdf,
            file_name="Enterprise_AI_Analytics_Report.pdf",
            mime="application/pdf",
            use_container_width=True,
            key="download_pdf_report"
        )

    st.write("")

    if st.button(
        "🗑 Clear PDF Content",
        use_container_width=True,
        key="clear_pdf_content"
    ):
        st.session_state.pdf_sections = []
        st.success("PDF Content Cleared ✅")