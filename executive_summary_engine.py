def generate_executive_summary(plant):

    material_score = plant.get(
        "material_score",
        0
    )

    thermal_score = plant.get(
        "thermal_score",
        0
    )

    feasibility_score = plant.get(
        "feasibility_score",
        0
    )

    q_factor_score = plant.get(
        "q_factor_score",
        0
    )

    lri_score = plant.get(
        "lri_score",
        None
    )

    if lri_score is None:

        lri_score = round(
            (
                material_score
                + thermal_score
                + feasibility_score
                + q_factor_score
            ) / 4,
            2
        )

    if lri_score >= 85:

        status = (
            "READY FOR PROTOTYPE"
        )

        confidence = "HIGH"

    elif lri_score >= 60:

        status = (
            "RESEARCH STAGE"
        )

        confidence = "MEDIUM"

    else:

        status = (
            "NEEDS OPTIMIZATION"
        )

        confidence = "LOW"

    return {

        "plant":
        plant.get("name", "Unknown"),

        "rank":
        plant.get("global_rank", "N/A"),

        "laser_color":
        plant.get("laser_color", "N/A"),

        "wavelength":
        plant.get("lambda_em", "N/A"),

        "lri":
        lri_score,

        "status":
        status,

        "confidence":
        confidence
    }