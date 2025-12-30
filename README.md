# Advanced Automated Data Reports

This project allows you to upload CSV or Excel datasets and automatically generates:
- Sweetviz interactive EDA report
- KPIs summary tables
- Automatic charts for numeric and categorical columns
- PDF reports combining KPIs and charts

## Features
- Multi-sheet Excel support
- Automatic detection of numeric and categorical columns
- Downloadable Sweetviz HTML report
- Downloadable PDF report
- Streamlit dashboard for interactive visualization

## Installation
```bash
git clone <repo-url>
cd Automated_Data_Reports
pip install -r requirements.txt
streamlit run app.py
