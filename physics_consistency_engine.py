def evaluate_physics_consistency(plant):

    consistency_score = 100

    gain = plant.get("gain_score", 0)

    efficiency = plant.get(
        "laser_efficiency_score", 0
    )

    thermal = plant.get("thermal_score", 0)

    q_factor = plant.get(
        "q_factor_score", 0
    )

    material_score = plant.get(
        "material_score", 0
    )

    lri = plant.get("lri_score", 0)

    # Gain vs Efficiency
    if abs(gain - efficiency) > 40:
        consistency_score -= 15

    # Thermal vs Q-Factor
    if thermal < 40 and q_factor > 80:
        consistency_score -= 20

    # Material Score vs LRI
    if abs(material_score - lri) > 35:
        consistency_score -= 15

    # General weak system
    if gain < 30 and efficiency > 85:
        consistency_score -= 25

    consistency_score = max(consistency_score, 0)

    return round(consistency_score, 2)


def classify_consistency(score):

    if score >= 90:
        return "Highly Consistent"

    elif score >= 75:
        return "Scientifically Acceptable"

    elif score >= 60:
        return "Moderately Consistent"

    else:
        return "Physically Inconsistent"