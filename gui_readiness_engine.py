def evaluate_gui_readiness(
    visualization_data,
    chart_recommendations,
    dashboard_layout,
    runtime_report,
    health_summary
):

    readiness_score = 0
    notes = []

    if len(visualization_data) > 0:
        readiness_score += 25
        notes.append("Visualization data is ready.")

    if len(chart_recommendations) > 0:
        readiness_score += 20
        notes.append("Chart recommendations are available.")

    if len(dashboard_layout) > 0:
        readiness_score += 25
        notes.append("Dashboard layout is prepared.")

    if runtime_report.get("runtime_seconds", 999) < 10:
        readiness_score += 15
        notes.append("Runtime performance is acceptable.")

    if "Stable" in health_summary.get("platform_status", ""):
        readiness_score += 15
        notes.append("Platform health is stable.")

    return {
        "score": readiness_score,
        "class": classify_gui_readiness(readiness_score),
        "notes": notes
    }


def classify_gui_readiness(score):

    if score >= 90:
        return "GUI Development Ready"

    elif score >= 75:
        return "Nearly Ready for GUI"

    elif score >= 60:
        return "GUI Preparation in Progress"

    else:
        return "Not Ready for GUI"