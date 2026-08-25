def generate_system_health_summary(
    ranked_plants,
    validation_report,
    optimization_report,
    runtime_report
):

    total_plants = len(ranked_plants)

    pass_count = 0
    warning_count = 0
    review_count = 0

    for plant in ranked_plants:

        status = plant.get("audit_status", "")

        if status == "PASS":
            pass_count += 1

        elif status == "WARNING":
            warning_count += 1

        elif status == "REVIEW REQUIRED":
            review_count += 1

    return {
        "total_plants": total_plants,
        "pass": pass_count,
        "warning": warning_count,
        "review_required": review_count,
        "configuration_valid": validation_report.get(
            "system_valid", False
        ),
        "optimization_status": optimization_report.get(
            "optimization_status", "Unknown"
        ),
        "runtime_status": runtime_report.get(
            "system_status", "Unknown"
        ),
        "platform_status": classify_platform_status(
            validation_report,
            review_count
        )
    }


def classify_platform_status(
    validation_report,
    review_count
):

    if (
        validation_report.get("system_valid", False)
        and review_count == 0
    ):
        return "LASERSTONE Platform Stable"

    elif validation_report.get("system_valid", False):
        return "LASERSTONE Platform Stable with Review Notes"

    else:
        return "LASERSTONE Platform Requires Configuration Review"

from project_registry import PROJECT_REGISTRY


def generate_system_health_report():

    total_engines = len(PROJECT_REGISTRY)

    connected_engines = 0
    isolated_engines = 0
    total_connections = 0

    most_connected_engine = ""
    most_connections = 0

    for engine_name, info in PROJECT_REGISTRY.items():

        inputs_count = len(info.get("inputs", []))
        outputs_count = len(info.get("outputs", []))

        connections = inputs_count + outputs_count
        total_connections += connections

        if connections > 0:
            connected_engines += 1
        else:
            isolated_engines += 1

        if connections > most_connections:
            most_connections = connections
            most_connected_engine = engine_name

    coverage = 0

    if total_engines > 0:
        coverage = round(
            (connected_engines / total_engines) * 100,
            2
        )

    print("\n=== SYSTEM HEALTH REPORT ===\n")
    print(f"Total Engines: {total_engines}")
    print(f"Connected Engines: {connected_engines}")
    print(f"Isolated Engines: {isolated_engines}")
    print(f"Connectivity Coverage: {coverage}%")
    print(f"Total Connections: {total_connections}")
    print(f"Most Connected Engine: {most_connected_engine}")
    print(f"Connection Count: {most_connections}")