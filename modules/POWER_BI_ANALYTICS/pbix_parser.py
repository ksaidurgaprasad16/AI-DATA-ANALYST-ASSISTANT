# =========================================================
# POWER BI ANALYTICS - PBIX PARSER
# =========================================================

import zipfile
import json
import re
import io

# =========================================================
# MAIN PARSER FUNCTION
# =========================================================

def parse_pbix(uploaded_file):
    """
    Parse a PBIX or PBIT file and extract:
    - Tables and columns
    - Relationships
    - DAX measures
    - Report pages and visuals
    - Power Query M code
    Returns a dict with all extracted data.
    """

    result = {
        "file_name": uploaded_file.name,
        "tables": [],
        "relationships": [],
        "dax_measures": [],
        "report_pages": [],
        "power_query": [],
        "raw_errors": []
    }

    try:
        file_bytes = uploaded_file.read()
        uploaded_file.seek(0)

        with zipfile.ZipFile(io.BytesIO(file_bytes), "r") as z:

            file_list = z.namelist()

            # =====================================================
            # EXTRACT DATA MODEL SCHEMA
            # Tables, Columns, Relationships, DAX Measures
            # =====================================================

            schema_candidates = [
                f for f in file_list
                if "DataModelSchema" in f
                or "datamodel" in f.lower()
                or "schema" in f.lower()
            ]

            for schema_file in schema_candidates:
                try:
                    raw = z.read(schema_file)

                    # try UTF-16 first (common in PBIX)
                    try:
                        content = raw.decode("utf-16-le")
                    except:
                        try:
                            content = raw.decode("utf-8")
                        except:
                            content = raw.decode("latin-1")

                    # remove BOM if present
                    content = content.lstrip("\ufeff")

                    schema = json.loads(content)

                    # =========================================
                    # EXTRACT TABLES AND COLUMNS
                    # =========================================

                    model = schema.get("model", schema)
                    tables_raw = model.get("tables", [])

                    for table in tables_raw:
                        table_name = table.get("name", "Unknown")

                        # skip hidden system tables
                        if table_name.startswith("$") or table_name.startswith("~"):
                            continue

                        columns = []
                        for col in table.get("columns", []):
                            col_name = col.get("name", "")
                            col_type = col.get("dataType", "unknown")
                            col_expr = col.get("expression", "")
                            if col_name and not col_name.startswith("RowNumber"):
                                columns.append({
                                    "name": col_name,
                                    "type": col_type,
                                    "expression": col_expr
                                })

                        # =========================================
                        # EXTRACT DAX MEASURES
                        # =========================================

                        for measure in table.get("measures", []):
                            measure_name = measure.get("name", "")
                            measure_expr = measure.get("expression", "")
                            if measure_name and measure_expr:
                                result["dax_measures"].append({
                                    "table": table_name,
                                    "name": measure_name,
                                    "expression": measure_expr
                                })

                        if columns:
                            result["tables"].append({
                                "name": table_name,
                                "columns": columns
                            })

                    # =========================================
                    # EXTRACT RELATIONSHIPS
                    # =========================================

                    relationships_raw = model.get("relationships", [])

                    for rel in relationships_raw:
                        result["relationships"].append({
                            "from_table": rel.get("fromTable", ""),
                            "from_column": rel.get("fromColumn", ""),
                            "to_table": rel.get("toTable", ""),
                            "to_column": rel.get("toColumn", ""),
                            "cardinality": rel.get("crossFilteringBehavior", ""),
                            "type": rel.get("type", "")
                        })

                except Exception as e:
                    result["raw_errors"].append(
                        f"Schema parse error: {str(e)}"
                    )

            # =====================================================
            # EXTRACT REPORT LAYOUT
            # Pages and Visuals
            # =====================================================

            layout_candidates = [
                f for f in file_list
                if "Layout" in f
                and "Report" in f
            ]

            for layout_file in layout_candidates:
                try:
                    raw = z.read(layout_file)

                    try:
                        content = raw.decode("utf-16-le")
                    except:
                        try:
                            content = raw.decode("utf-8")
                        except:
                            content = raw.decode("latin-1")

                    content = content.lstrip("\ufeff")

                    layout = json.loads(content)

                    sections = layout.get("sections", [])

                    for section in sections:
                        page_name = section.get(
                            "displayName",
                            section.get("name", "Unknown Page")
                        )

                        visuals = []
                        for visual_container in section.get(
                            "visualContainers", []
                        ):
                            try:
                                config_str = visual_container.get(
                                    "config", "{}"
                                )
                                config = json.loads(config_str)
                                visual_type = (
                                    config
                                    .get("singleVisual", {})
                                    .get("visualType", "unknown")
                                )
                                if visual_type and visual_type != "unknown":
                                    visuals.append(visual_type)
                            except:
                                pass

                        result["report_pages"].append({
                            "name": page_name,
                            "visuals": list(set(visuals))
                        })

                except Exception as e:
                    result["raw_errors"].append(
                        f"Layout parse error: {str(e)}"
                    )

            # =====================================================
            # EXTRACT POWER QUERY M CODE
            # =====================================================

            mashup_candidates = [
                f for f in file_list
                if "Mashup" in f
                or "mashup" in f.lower()
                or "DataMashup" in f
            ]

            for mashup_file in mashup_candidates:
                try:
                    raw = z.read(mashup_file)

                    # Mashup is a ZIP inside PBIX
                    try:
                        with zipfile.ZipFile(
                            io.BytesIO(raw), "r"
                        ) as mz:
                            for mf in mz.namelist():
                                if mf.endswith(".m") or "Section" in mf:
                                    try:
                                        m_code = mz.read(mf).decode(
                                            "utf-8", errors="replace"
                                        )
                                        if "let" in m_code.lower():
                                            result["power_query"].append({
                                                "file": mf,
                                                "code": m_code[:2000]
                                            })
                                    except:
                                        pass
                    except:
                        pass

                except Exception as e:
                    result["raw_errors"].append(
                        f"Mashup parse error: {str(e)}"
                    )

    except zipfile.BadZipFile:
        result["raw_errors"].append(
            "File is not a valid PBIX/PBIT file or is corrupted."
        )
    except Exception as e:
        result["raw_errors"].append(f"General parse error: {str(e)}")

    return result


# =========================================================
# HELPER — SUMMARIZE PARSED DATA
# =========================================================

def get_parse_summary(parsed):
    """Returns a human-readable summary of parsed PBIX data."""

    tables = parsed.get("tables", [])
    relationships = parsed.get("relationships", [])
    measures = parsed.get("dax_measures", [])
    pages = parsed.get("report_pages", [])
    pq = parsed.get("power_query", [])

    total_cols = sum(len(t["columns"]) for t in tables)

    summary = f"""
File: {parsed.get("file_name", "Unknown")}
Tables: {len(tables)}
Total Columns: {total_cols}
Relationships: {len(relationships)}
DAX Measures: {len(measures)}
Report Pages: {len(pages)}
Power Query Queries: {len(pq)}
"""
    return summary.strip()


# =========================================================
# HELPER — FORMAT FOR AI PROMPT
# =========================================================

def format_for_ai(parsed):
    """Formats parsed PBIX data into a string for AI prompts."""

    lines = []

    lines.append(f"File: {parsed.get('file_name', 'Unknown')}")
    lines.append("")

    # tables and columns
    tables = parsed.get("tables", [])
    if tables:
        lines.append("TABLES AND COLUMNS:")
        for table in tables:
            col_names = [c["name"] for c in table["columns"]]
            lines.append(
                f"  Table: {table['name']} → "
                f"Columns: {', '.join(col_names)}"
            )
        lines.append("")

    # relationships
    relationships = parsed.get("relationships", [])
    if relationships:
        lines.append("RELATIONSHIPS:")
        for rel in relationships:
            lines.append(
                f"  {rel['from_table']}[{rel['from_column']}] → "
                f"{rel['to_table']}[{rel['to_column']}]"
            )
        lines.append("")

    # dax measures
    measures = parsed.get("dax_measures", [])
    if measures:
        lines.append("EXISTING DAX MEASURES:")
        for m in measures[:20]:
            lines.append(
                f"  [{m['table']}] {m['name']} = {m['expression'][:100]}"
            )
        lines.append("")

    # report pages
    pages = parsed.get("report_pages", [])
    if pages:
        lines.append("REPORT PAGES:")
        for page in pages:
            visuals_str = (
                ", ".join(page["visuals"])
                if page["visuals"] else "no visuals detected"
            )
            lines.append(
                f"  Page: {page['name']} → Visuals: {visuals_str}"
            )
        lines.append("")

    return "\n".join(lines)