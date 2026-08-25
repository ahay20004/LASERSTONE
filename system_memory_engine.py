def generate_system_memory(ranked_plants):

    if len(ranked_plants) == 0:

        return {
            "status": "No Data Available"
        }

    top_plant = ranked_plants[0]

    memory = {

        "top_material":
        top_plant.get("name", "Unknown"),

        "top_material_score":
        top_plant.get(
            "material_score", 0
        ),

        "top_intelligence":
        top_plant[
            "intelligence_summary"
        ][
            "intelligence_score"
        ],

        "top_patent":
        top_plant.get(
            "patent_potential_score",
            0
        ),

        "top_decision":
        top_plant.get(
            "governor_decision",
            "Unknown"
        )
    }

    return memory