import os

from project_registry import PROJECT_REGISTRY


def discover_engines(root_dir="."):

    engines = []

    for folder, _, files in os.walk(root_dir):

        if "__pycache__" in folder:
            continue

        for file in files:

            if file.endswith("_engine.py"):

                engine_name = file.replace(
                    ".py",
                    ""
                )

                engines.append(
                    engine_name
                )

    return sorted(engines)


def show_discovered_engines():

    engines = discover_engines()

    print(
        "\n=== LASERSTONE AUTO REGISTRY ===\n"
    )

    for index, engine in enumerate(
        engines,
        start=1
    ):

        print(
            f"{index}. {engine}"
        )

    print("\n----------------------------")

    print(
        f"Total Engines Found: {len(engines)}"
    )


def compare_with_registry():

    discovered_engines = discover_engines()

    registered_engines = list(
        PROJECT_REGISTRY.keys()
    )

    missing_engines = []

    for engine in discovered_engines:

        if engine not in registered_engines:

            missing_engines.append(engine)
            extra_registered = []
            for engine in registered_engines:
                if engine not in discovered_engines:extra_registered.append(engine)

    total_discovered = len(discovered_engines)
    total_registered = len(registered_engines)
    total_missing = len(missing_engines)

    if total_discovered == 0:
        coverage = 0
    else:
        coverage = round(
            (total_registered / total_discovered) * 100,
            2
        )

    print(
        "\n=== REGISTRY COVERAGE REPORT ===\n"
    )

    print(
        f"Discovered Engines: {total_discovered}"
    )

    print(
        f"Registered Engines: {total_registered}"
    )

    print(
        f"Missing Engines: {total_missing}"
    )
    print(
    f"Registered But Not Discovered: {len(extra_registered)}")

    print(
        f"Registry Coverage: {coverage}%"
    )

    print(
        "\n=== MISSING ENGINES ===\n"
    )

    if not missing_engines:

        print("All discovered engines are registered.")

    else:

        for index, engine in enumerate(
            missing_engines,
            start=1
        ):

            print(
                f"{index}. {engine}"
            )

def suggest_missing_registry_entries():

    discovered_engines = discover_engines()
    registered_engines = list(PROJECT_REGISTRY.keys())

    missing_engines = []

    for engine in discovered_engines:

        if engine not in registered_engines:
            missing_engines.append(engine)

    print("\n=== SUGGESTED REGISTRY ENTRIES ===\n")

    for engine in missing_engines:

        print(f'"{engine}": {{')
        print('    "status": "ACTIVE",')
        suggested_category = suggest_category(engine)
        print(
            f'    "category": "{suggested_category}",'
        )
        print('    "standardized": True,')
        print('    "dashboard_visible": True,')
        print('    "inputs": [')
        print('        "plant_data"')
        print('    ],')
        print('    "outputs": [')
        print(f'        "{engine.replace("_engine", "")}_output"')
        print('    ]')
        print('},\n')


def category_report():

    category_counts = {}

    for engine_name, info in PROJECT_REGISTRY.items():

        category = info.get(
            "category",
            "Unclassified"
        )

        if category not in category_counts:
            category_counts[category] = 0

        category_counts[category] += 1

    print("\n=== CATEGORY ANALYSIS REPORT ===\n")

    for category, count in sorted(category_counts.items()):

        print(
            f"{category}: {count}"
        )

    print("\n----------------------------")

    print(
        f"Total Categories: {len(category_counts)}"
    )

    print(
        f"Total Registered Engines: {len(PROJECT_REGISTRY)}"
    )
    
def suggest_category(engine_name):

    engine_name = engine_name.lower()

    if "audit" in engine_name:
        return "System Audit"

    elif "dashboard" in engine_name:
        return "User Interface"

    elif "gui" in engine_name:
        return "User Interface"

    elif "laser" in engine_name:
        return "Laser Engineering"

    elif "prediction" in engine_name:
        return "Scientific Prediction"

    elif "recommendation" in engine_name:
        return "Decision Support"

    elif "health" in engine_name:
        return "System Health"

    elif "runtime" in engine_name:
        return "Runtime Monitoring"

    elif "mission" in engine_name:
        return "Mission Control"

    elif "evolution" in engine_name:
        return "Evolution Analysis"

    elif "control" in engine_name:
        return "System Control"

    elif "beam" in engine_name:
        return "Laser Engineering"
    elif "efficiency" in engine_name:
        return "Performance Analysis"

    elif "dependency" in engine_name:
        return "Infrastructure Intelligence"

    elif "export" in engine_name:
        return "Data Export"

    elif "snapshot" in engine_name:
        return "System Monitoring"

    elif "discovery" in engine_name:
         return "Artificial Intelligence"
    
    else:
        return "Unclassified"

if __name__ == "__main__":

    show_discovered_engines()
    compare_with_registry()
    category_report()
    suggest_missing_registry_entries()