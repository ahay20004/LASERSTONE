from constants import (
    THRESHOLDS
)
from project_registry import PROJECT_REGISTRY



def generate_intelligence_summary(plant):

    summary = {}

    summary["material_score"] = (
        plant.get("material_score", 0)
    )

    summary["lri_score"] = (
        plant.get("lri_score", 0)
    )

    summary["experimental_success"] = (
        plant.get(
            "experimental_success_score",
            0
        )
    )

    summary["novelty"] = (
        plant.get(
            "research_novelty_score",
            0
        )
    )

    summary["patent"] = (
        plant.get(
            "patent_potential_score",
            0
        )
    )

    summary["confidence"] = (
        plant.get(
            "scientific_confidence_score",
            0
        )
    )

    summary["integrity"] = (
        plant.get(
            "system_integrity_score",
            0
        )
    )

    intelligence_score = (

        summary["material_score"] * 0.20

        +

        summary["lri_score"] * 0.15

        +

        summary["experimental_success"] * 0.15

        +

        summary["novelty"] * 0.15

        +

        summary["patent"] * 0.10

        +

        summary["confidence"] * 0.15

        +

        summary["integrity"] * 0.10
    )

    summary["intelligence_score"] = round(
        intelligence_score,
        2
    )

    summary["classification"] = (
        classify_intelligence(
            intelligence_score
        )
    )

    return summary


def classify_intelligence(score):

    if score >= THRESHOLDS["elite"]:

        return (
            "Elite Scientific Intelligence"
        )

    elif score >= THRESHOLDS["advanced"]:

        return (
            "Advanced Scientific Intelligence"
        )

    elif score >= THRESHOLDS["promising"]:

        return (
            "Promising Scientific Intelligence"
        )

    else:

        return (
            "Developing Scientific Intelligence"
        )
print("INTELLIGENCE HUB LOADED")

def generate_system_health_report():

    print("\n=== SYSTEM HEALTH REPORT ===\n")
    print("System Health Engine Connected Successfully")

def generate_system_health_report():

    total_engines = len(PROJECT_REGISTRY)

    connected_engines = 0
    isolated_engines = 0
    most_connected_engine = ""
    most_connections = 0

    for engine_name, info in PROJECT_REGISTRY.items():

        connections = (
            len(info.get("inputs", []))
            +
            len(info.get("outputs", []))
        )

        if connections > 0:
            connected_engines += 1
        if connections > most_connections:
            most_connections = connections
            most_connected_engine = engine_name
    else:
            isolated_engines += 1
    print(f"Most Connected Engine: {most_connected_engine}")
    print(f"Connections: {most_connections}")

    coverage = 0

    if total_engines > 0:
        coverage = round(
            (
                connected_engines
                / total_engines
            ) * 100,
            2
        )
    system_status = "STABLE"
    if coverage >= 90:
        system_status = "EXCELLENT"
    elif coverage >= 75:
        system_status = "STABLE"

    elif coverage >= 50:
         system_status = "MODERATE"

    else:
        system_status = "CRITICAL"
    
    total_engines = len(PROJECT_REGISTRY)
    if total_engines < 10:
        platform_class = "BASIC ANALYZER"
    elif total_engines < 20:
        platform_class = "ADVANCED ANALYZER"
    elif total_engines < 30:
        platform_class = "SCIENTIFIC PLATFORM"
    else:
         platform_class = "INTELLIGENT SCIENTIFIC PLATFORM"

    print("\n=== SYSTEM HEALTH REPORT ===\n")
    print(f"Total Engines: {total_engines}" )
    print(f"Connected Engines: {connected_engines}")
    print(f"Isolated Engines: {isolated_engines}" )
    print(f"Connectivity Coverage: {coverage}%"  )
    print(f"System Status: {system_status}")
    print("\nLASERSTONE PLATFORM CLASSIFICATION")
    print("=" * 35)
    print(f"Platform Class : {platform_class}")
    print(f"Registry Engines: {total_engines}")
    print(f"Platform Maturity: {coverage}%")