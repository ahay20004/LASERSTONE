def generate_mission_control_summary(plant):

    return {

        "name": plant.get("name", "Unknown"),

        "material_score":
        plant.get("material_score", 0),

        "lri":
        plant.get("lri_score", 0),

        "intelligence":
        plant["intelligence_summary"][
            "intelligence_score"
        ],

        "experimental":
        plant.get(
            "experimental_success_score",
            0
        ),

        "novelty":
        plant.get(
            "research_novelty_score",
            0
        ),

        "patent":
        plant.get(
            "patent_potential_score",
            0
        ),

        "integrity":
        plant.get(
            "system_integrity_score",
            0
        ),

        "decision":
        plant.get(
            "governor_decision",
            "Unknown"
        )
    }