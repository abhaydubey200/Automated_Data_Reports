def generate_sweetviz(df, sheet_name, report_dir):
    import sweetviz as sv
    import os
    from datetime import datetime

    os.makedirs(report_dir, exist_ok=True)

    file_path = os.path.join(
        report_dir,
        f"sweetviz_{sheet_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    )

    report = sv.analyze(df)
    report.show_html(file_path, open_browser=False)

    return file_path
