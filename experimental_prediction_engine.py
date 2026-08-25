from constants import (
    THRESHOLDS
)


def predict_experimental_success(plant):

    material_score = plant.get(
        "material_score", 0
    )

    lri = plant.get(
        "lri_score", 0
    )

    consistency = plant.get(
        "physics_consistency_score", 0
    )

    efficiency = plant.get(
        "laser_efficiency_score", 0
    )

    prediction = (

        material_score * 0.30

        +

        lri * 0.25

        +

        consistency * 0.25

        +

        efficiency * 0.20
    )

    return round(prediction, 2)


def classify_experimental_probability(score):

    if score >= THRESHOLDS["elite"]:

        return (
            "High Experimental Success "
            "Probability"
        )

    elif score >= THRESHOLDS["advanced"]:

        return (
            "Promising Experimental Candidate"
        )

    elif score >= THRESHOLDS["promising"]:

        return (
            "Moderate Experimental Potential"
        )

    else:

        return (
            "Low Experimental Feasibility"
        )