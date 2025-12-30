import pandas as pd

def load_file(uploaded_file):
    if uploaded_file.name.endswith(".csv"):
        return {"Sheet1": pd.read_csv(uploaded_file)}

    elif uploaded_file.name.endswith((".xls", ".xlsx")):
        excel = pd.ExcelFile(uploaded_file)
        return {sheet: excel.parse(sheet) for sheet in excel.sheet_names}

    else:
        raise ValueError("Unsupported file format")
