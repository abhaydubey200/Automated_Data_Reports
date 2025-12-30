import streamlit as st

from utils.data_loader import load_file
from utils.kpi_generator import generate_kpis
from utils.report_generator import generate_sweetviz

st.set_page_config(page_title="Automated Data Report", layout="wide")

st.title("📊 Automated Data Reporting System")
st.write("Upload CSV or Excel file to auto-generate KPIs & Sweetviz report")

uploaded_file = st.file_uploader(
    "Upload CSV or Excel file",
    type=["csv", "xlsx", "xls"]
)

if uploaded_file:
    try:
        sheets = load_file(uploaded_file)

        for sheet_name, df in sheets.items():
            st.divider()
            st.subheader(f"📄 Sheet: {sheet_name}")

            # KPIs
            kpis = generate_kpis(df)
            cols = st.columns(len(kpis))

            for col, (key, value) in zip(cols, kpis.items()):
                col.metric(key, value)

            # Sweetviz
            st.subheader("📈 Sweetviz Report")

            if st.button(f"Generate Report for {sheet_name}"):
                with st.spinner("Generating Sweetviz Report..."):
                    report_path = generate_sweetviz(
                        df,
                        sheet_name,
                        "Reports/sweetviz"
                    )

                with open(report_path, "r", encoding="utf-8") as f:
                    st.components.v1.html(
                        f.read(),
                        height=800,
                        scrolling=True
                    )

    except Exception as e:
        st.error(f"Error: {e}")
