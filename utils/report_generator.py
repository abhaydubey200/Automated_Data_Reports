import pandas as pd
import os
from datetime import datetime
from fpdf import FPDF
import streamlit as st

# -----------------------------
# Load Data
# -----------------------------
@st.cache_data
def load_data(file):
    if file.name.endswith(".csv"):
        return {"Sheet1": pd.read_csv(file)}
    else:
        return pd.read_excel(file, sheet_name=None)

# -----------------------------
# Sweetviz (Lazy Import)
# -----------------------------
@st.cache_resource
def generate_sweetviz(df, sheet_name, report_dir):
    import sweetviz as sv  # IMPORTANT: lazy import

    os.makedirs(report_dir, exist_ok=True)
    path = os.path.join(
        report_dir,
        f"sweetviz_{sheet_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    )

    report = sv.analyze(df)
    report.show_html(path, open_browser=False)
    return path

# -----------------------------
# KPIs
# -----------------------------
def generate_kpis(df):
    numeric_cols = df.select_dtypes(include="number")
    return numeric_cols.describe().T if not numeric_cols.empty else pd.DataFrame()

# -----------------------------
# PDF Report
# -----------------------------
def generate_pdf(kpis, sheet_name, report_dir):
    os.makedirs(report_dir, exist_ok=True)
    pdf_path = os.path.join(report_dir, f"report_{sheet_name}.pdf")

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(190, 10, f"Automated Report - {sheet_name}", ln=True, align="C")

    pdf.set_font("Arial", size=10)
    for idx, row in kpis.iterrows():
        pdf.multi_cell(0, 8, f"{idx}: {row.to_dict()}")

    pdf.output(pdf_path)
    return pdf_path
