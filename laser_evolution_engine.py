def predict_material_evolution(plant):

    evolution_score = 0

    recommendations = []

    thermal = plant.get("thermal_score", 0)
    efficiency = plant.get(
        "laser_efficiency_score", 0
    )
    q_factor = plant.get(
        "q_factor_score", 0
    )
    beam = plant.get(
        "beam_quality_score", 0
    )

    # Thermal optimization
    if thermal < 70:
        evolution_score += 20

        recommendations.append(
            "Advanced cooling may "
            "significantly improve performance."
        )

    # Efficiency optimization
    if efficiency < 75:
        evolution_score += 25

        recommendations.append(
            "Optimized pumping could "
            "increase laser efficiency."
        )

    # Resonator optimization
    if q_factor < 75:
        evolution_score += 25

        recommendations.append(
            "Improved cavity design may "
            "increase coherence and gain."
        )

    # Beam optimization
    if beam < 75:
        evolution_score += 20

        recommendations.append(
            "Beam shaping techniques may "
            "enhance optical quality."
        )

    # Already advanced
    if evolution_score == 0:

        evolution_score = 10

        recommendations.append(
            "Material already operates near "
            "optimal projected conditions."
        )

    evolution_score = min(evolution_score, 100)

    return {
        "score": evolution_score,
        "recommendations": recommendations
    }


def classify_evolution_potential(score):

    if score >= 80:
        return "Extreme Future Improvement Potential"

    elif score >= 60:
        return "High Optimization Potential"

    elif score >= 40:
        return "Moderate Improvement Potential"

    else:
        return "Near-Optimal Current State"