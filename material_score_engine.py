from constants import (
    MATERIAL_SCORE_WEIGHTS,
    THRESHOLDS
)


def convert_spectral_quality_to_score(value):

    quality_map = {
        "Excellent": 100,
        "Very Good": 85,
        "Good": 75,
        "Moderate": 60,
        "Low": 40,
        "Weak": 25
    }

    if isinstance(value, (int, float)):
        return value

    return quality_map.get(value, 40)


def calculate_material_score(plant):

    lsi = plant.get("lsi", 0)

    thermal_score = plant.get("thermal_score", 0)

    q_factor_score = plant.get("q_factor_score", 0)

    beam_quality_score = plant.get("beam_quality_score", 0)

    laser_efficiency_score = plant.get(
        "laser_efficiency_score", 0
    )

    spectral_quality = convert_spectral_quality_to_score(
        plant.get("spectral_quality", 0)
    )

    normalized_lsi = min(lsi * 10, 100)

    material_score = (
        normalized_lsi * MATERIAL_SCORE_WEIGHTS["lsi"]
        +
        thermal_score * MATERIAL_SCORE_WEIGHTS["thermal"]
        +
        q_factor_score * MATERIAL_SCORE_WEIGHTS["q_factor"]
        +
        beam_quality_score * MATERIAL_SCORE_WEIGHTS["beam_quality"]
        +
        laser_efficiency_score * MATERIAL_SCORE_WEIGHTS["efficiency"]
        +
        spectral_quality * MATERIAL_SCORE_WEIGHTS["spectral"]
    )

    return round(material_score, 2)


def classify_material_score(score):

    if score >= THRESHOLDS["elite"]:
        return "Excellent Laser Material"

    elif score >= THRESHOLDS["advanced"]:
        return "Very Good Laser Material"

    elif score >= THRESHOLDS["promising"]:
        return "Promising Laser Material"

    elif score >= THRESHOLDS["moderate"]:
        return "Moderate Laser Material"

    else:
        return "Weak Laser Material"