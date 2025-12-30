import pandas as pd
import os
import sweetviz as sv
import plotly.express as px
from fpdf import FPDF
from datetime import datetime
import streamlit as st

# -----------------------------
# Cached Data Loader
# -----------------------------
@st.cache_data
def load_data(file):
    if file.name.endswith(".csv"):
        return {"Sheet1": pd.read_csv(file)}
    else:
        return pd.read_excel(file, sheet_name=None)  # All sheets

# -----------------------------
# Generate Sweetviz Report
# -----------------------------
@st.cache_resource
def generate_sweetviz(df, sheet_name="Sheet1", report_dir="Reports"):
    os.makedirs(report_dir, exist_ok=True)
    file_path = os.path.join(report_dir, f"Sweetviz_Report_{sheet_name}_{datetime.now().strftime('%Y-%m-%d_%H%M%S')}.html")
    report = sv.analyze(df)
    report.show_html(file_path)
    return file_path

# -----------------------------
# Generate KPIs
# -----------------------------
def generate_kpis(df):
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    if numeric_cols:
        return df[numeric_cols].describe().T
    else:
        return pd.DataFrame()

# -----------------------------
# Generate Charts
# -----------------------------
def generate_charts(df, report_dir="Reports"):
    os.makedirs(report_dir, exist_ok=True)
    chart_files = []

    # Numeric charts
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    for col in numeric_cols:
        fig = px.histogram(df, x=col, nbins=20)
        chart_path = os.path.join(report_dir, f"{col}_{datetime.now().strftime('%H%M%S')}.png")
        fig.write_image(chart_path)
        chart_files.append(chart_path)

    # Categorical charts
    categorical_cols = df.select_dtypes(include="object").columns.tolist()
    for col in categorical_cols:
        fig = px.histogram(df, x=col)
        chart_path = os.path.join(report_dir, f"{col}_{datetime.now().strftime('%H%M%S')}.png")
        fig.write_image(chart_path)
        chart_files.append(chart_path)

    return chart_files

# -----------------------------
# Generate PDF Report using FPDF
# -----------------------------
def generate_pdf(df, kpis, charts, sheet_name="Sheet1", report_dir="Reports"):
    os.makedirs(report_dir, exist_ok=True)
    pdf_file = os.path.join(report_dir, f"PDF_Report_{sheet_name}_{datetime.now().strftime('%Y-%m-%d_%H%M%S')}.pdf")
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt=f"Automated Report - {sheet_name}", ln=1, align="C")
    pdf.set_font("Arial", '', 12)
    pdf.cell(200, 10, txt=f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=1)

    # KPIs Table
    pdf.ln(5)
    for i, row in kpis.iterrows():
        pdf.multi_cell(0, 8, txt=f"{i}: {row.to_dict()}")
    
    pdf.output(pdf_file)
    return pdf_file
