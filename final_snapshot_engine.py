def generate_final_snapshot(
    ranked_plants,
    runtime_report,
    health_summary,
    platform_evolution
):

    if len(ranked_plants) == 0:

        return {
            "status":
            "No Scientific Data Available"
        }

    top = ranked_plants[0]

    snapshot = {

        "top_material":
        top.get("name", "Unknown"),

        "top_score":
        top.get(
            "material_score", 0
        ),

        "top_intelligence":
        top[
            "intelligence_summary"
        ][
            "intelligence_score"
        ],

        "top_patent":
        top.get(
            "patent_potential_score",
            0
        ),

        "governor":
        top.get(
            "governor_decision",
            "Unknown"
        ),

        "platform_stage":
        platform_evolution.get(
            "stage",
            "Unknown"
        ),

        "runtime":
        runtime_report.get(
            "runtime_seconds",
            0
        ),

        "health":
        health_summary.get(
            "platform_status",
            "Unknown"
        )
    }

    return snapshot