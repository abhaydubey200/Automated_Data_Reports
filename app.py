import streamlit as st
from utils import report_generator as rg
import os

st.set_page_config(page_title="Automated Data Reports", layout="wide")
st.title("📊 Automated Data Analysis Platform")

uploaded_file = st.file_uploader(
    "Upload CSV or Excel file",
    type=["csv", "xlsx"]
)

if uploaded_file:
    st.success("File uploaded successfully")

    data = rg.load_data(uploaded_file)
    report_dir = os.path.join(os.getcwd(), "Reports")

    for sheet_name, df in data.items():
        st.header(f"Sheet: {sheet_name}")
        st.dataframe(df.head())

        # KPIs
        st.subheader("Key KPIs")
        kpis = rg.generate_kpis(df)
        st.dataframe(kpis)

        # Sweetviz
        st.subheader("Sweetviz Report")
        with st.spinner("Generating Sweetviz report..."):
            sv_path = rg.generate_sweetviz(df, sheet_name, report_dir)
        st.markdown(f"[Open Sweetviz Report]({sv_path})")

        # PDF
        st.subheader("PDF Report")
        pdf_path = rg.generate_pdf(kpis, sheet_name, report_dir)
        st.markdown(f"[Download PDF]({pdf_path})")

    st.success("All reports generated successfully")
