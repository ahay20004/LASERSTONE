import os


def save_text_report(report, plant_name):
    project_dir = os.path.dirname(os.path.abspath(__file__))

    reports_dir = os.path.join(project_dir, "reports")

    os.makedirs(reports_dir, exist_ok=True)

    file_name = plant_name.lower().replace(" ", "_")
    report_path = os.path.join(reports_dir, f"{file_name}_report.txt")

    with open(report_path, "w", encoding="utf-8") as file:
        file.write(report)

    return report_path