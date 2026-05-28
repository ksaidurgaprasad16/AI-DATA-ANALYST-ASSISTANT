# =========================================================
# SQL ANALYTICS - PDF REPORTS
# =========================================================

import streamlit as st
import io
import re
import tempfile

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak,
    Image
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter

PAGE_WIDTH = 532

# =========================================================
# CLEAN TEXT FOR PDF — removes all black dot causes
# =========================================================

def clean_pdf_text(text):
    """Remove all characters that cause black dots in PDF."""
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"\*(.+?)\*", r"\1", text)
    text = text.replace("■", "-")
    text = text.replace("•", "-")
    text = text.replace("─", "-")
    text = text.replace("━", "-")
    text = text.replace("–", "-")
    text = text.replace("—", "-")
    text = text.replace("👤", "User")
    text = text.replace("🤖", "Assistant")
    text = text.replace("✅", "")
    text = text.replace("⚠", "")
    text = text.replace("💡", "")
    text = text.encode("latin-1", errors="replace").decode("latin-1")
    return text

# =========================================================
# MAIN FUNCTION
# =========================================================

def show_sql_pdf_reports():

    st.markdown("""
    <h1 style='font-size:42px;font-weight:800;color:white;'>
    📄 SQL PDF Reports
    </h1>
    """, unsafe_allow_html=True)

    st.caption("Generate PDF reports from your SQL analytics")
    st.write("")

    if "pdf_sections" not in st.session_state:
        st.session_state.pdf_sections = []

    st.markdown("""
    <h2 style='color:white;font-weight:700;'>
    📚 Current Report Sections
    </h2>
    """, unsafe_allow_html=True)

    if len(st.session_state.pdf_sections) == 0:
        st.info(
            "No sections added yet. "
            "Add content from Query Runner, "
            "AI SQL Generator, SQL Visualizations "
            "or AI SQL Chat."
        )
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
            <b style="color:white;">
            {idx}. {item['title']}
            </b>
            </div>
            """, unsafe_allow_html=True)

    st.write("")
    st.write("")

    if st.button(
        "🚀 Generate SQL PDF Report",
        use_container_width=True,
        key="generate_sql_pdf"
    ):

        if len(st.session_state.pdf_sections) == 0:
            st.warning("No sections added yet.")
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

            elements = []

            elements.append(
                Paragraph(
                    "<b>Enterprise SQL Analytics Report</b>",
                    title_style
                )
            )
            elements.append(Spacer(1, 12))

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
                    # clean all problematic chars
                    content = clean_pdf_text(content)
                    content = re.sub(r"-{3,}", "----------", content)
                    content = re.sub(r"#+\s*", "", content)

                    # split into lines for better rendering
                    lines = content.split("\n")
                    for line in lines:
                        stripped = line.strip()
                        if stripped:
                            elements.append(
                                Paragraph(stripped, body_style)
                            )
                            elements.append(Spacer(1, 3))
                        else:
                            elements.append(Spacer(1, 6))

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
                                f"[Chart error: {e}]",
                                body_style
                            )
                        )

            doc.build(elements)
            pdf = buffer.getvalue()

        st.success("SQL PDF Report Generated ✅")

        st.download_button(
            "⬇ Download SQL PDF Report",
            data=pdf,
            file_name="SQL_Analytics_Report.pdf",
            mime="application/pdf",
            use_container_width=True,
            key="download_sql_pdf"
        )

    st.write("")

    if st.button(
        "🗑 Clear PDF Content",
        use_container_width=True,
        key="clear_sql_pdf"
    ):
        st.session_state.pdf_sections = []
        st.success("PDF Content Cleared ✅")