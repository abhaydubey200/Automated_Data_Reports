import streamlit as st
from utils import report_generator as rg
import os

st.set_page_config(page_title="Advanced Automated Data Reports", layout="wide")
st.title(" Advanced Automated Data Analytics Dashboard")

uploaded_file = st.file_uploader("Upload CSV or Excel", type=["csv", "xlsx"])

if uploaded_file:
    st.success(" File uploaded successfully!")
    
    # Load data
    df_dict = rg.load_data(uploaded_file)
    report_dir = os.path.join(os.getcwd(), "Reports")
    os.makedirs(report_dir, exist_ok=True)

    for sheet_name, df in df_dict.items():
        st.write(f"## Sheet: {sheet_name}")
        st.dataframe(df.head())

        # Sweetviz
        st.write("### Sweetviz Report")
        sv_file = rg.generate_sweetviz(df, sheet_name=sheet_name, report_dir=report_dir)
        st.markdown(f"[Open Sweetviz Report]({sv_file})")

        # KPIs
        st.write("### Key Metrics / KPIs")
        kpis = rg.generate_kpis(df)
        st.dataframe(kpis)

        # Charts
        st.write("### Automatic Charts")
        charts = rg.generate_charts(df, report_dir=report_dir)
        st.write(f"Generated {len(charts)} charts")

        # PDF
        st.write("### PDF Report")
        pdf_file = rg.generate_pdf(df, kpis, charts, sheet_name=sheet_name, report_dir=report_dir)
        st.markdown(f"[Download PDF Report]({pdf_file})")

    st.success(" All reports generated successfully!")
