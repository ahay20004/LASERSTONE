from project_registry import PROJECT_REGISTRY
from registry_auto_builder import discover_engines


def calculate_system_health(
        total_registered,
        standardized,
        found_engines):

    if found_engines == 0:
        return "CRITICAL"

    if total_registered == 0:
        return "CRITICAL"

    standardization_ratio = standardized / total_registered

    if standardization_ratio >= 0.5:
        return "HEALTHY"

    return "NEEDS REVIEW"


def generate_health_report():

    found_engines = len(
        discover_engines()
    )

    total_registered = len(
        PROJECT_REGISTRY
    )

    coverage = 0

    if found_engines > 0:
        coverage = round(
            (
                total_registered
                / found_engines
            ) * 100,
            2
        )

    standardized = sum(
        1
        for engine in PROJECT_REGISTRY.values()
        if engine.get(
            "standardized",
            False
        )
    )

    dashboard_connected = sum(
        1
        for engine in PROJECT_REGISTRY.values()
        if engine.get(
            "dashboard_visible",
            False
        )
    )

    health = calculate_system_health(
        total_registered,
        standardized,
        found_engines
    )

    print("\n" + "=" * 50)
    print("LASERSTONE PROJECT HEALTH REPORT")
    print("=" * 50)

    print(f"Total Engines Found: {found_engines}")
    print(f"Registered Engines: {total_registered}")
    print(f"Registry Coverage: {coverage}%")
    print(f"Standardized Engines: {standardized}")
    print(f"Dashboard Connected: {dashboard_connected}")
    print(f"System Health: {health}")

    print("=" * 50)


if __name__ == "__main__":

    generate_health_report()