import os
from datetime import datetime

def generate_sweetviz(df, sheet_name, output_dir):
    import sweetviz as sv   # Lazy import (IMPORTANT)

    os.makedirs(output_dir, exist_ok=True)

    file_path = os.path.join(
        output_dir,
        f"sweetviz_{sheet_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    )

    report = sv.analyze(df)
    report.show_html(file_path, open_browser=False)

    return file_path
