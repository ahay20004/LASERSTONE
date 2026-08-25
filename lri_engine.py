from constants import (
    LRI_WEIGHTS,
    THRESHOLDS
)


def calculate_lri(plant):

    thermal_score = plant.get(
        "thermal_score", 0
    )

    q_factor_score = plant.get(
        "q_factor_score", 0
    )

    laser_efficiency_score = plant.get(
        "laser_efficiency_score", 0
    )

    beam_quality_score = plant.get(
        "beam_quality_score", 0
    )

    feasibility_score = plant.get(
        "feasibility_score", 0
    )

    readiness = (

        thermal_score *

        LRI_WEIGHTS["thermal"]

        +

        q_factor_score *

        LRI_WEIGHTS["q_factor"]

        +

        laser_efficiency_score *

        LRI_WEIGHTS["efficiency"]

        +

        beam_quality_score *

        LRI_WEIGHTS["beam_quality"]

        +

        feasibility_score *

        LRI_WEIGHTS["feasibility"]
    )

    return round(readiness, 2)


def classify_lri(score):

    if score >= THRESHOLDS["elite"]:

        return "Laser System Ready"

    elif score >= THRESHOLDS["advanced"]:

        return (
            "Advanced Prototype Candidate"
        )

    elif score >= THRESHOLDS["promising"]:

        return (
            "Experimental Laser Material"
        )

    elif score >= THRESHOLDS["moderate"]:

        return (
            "Early Research Candidate"
        )

    else:

        return "Low Readiness Material"