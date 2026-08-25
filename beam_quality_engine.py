def evaluate_beam_quality(
    gain_score,
    q_factor_score,
    thermal_score,
    cavity_geometry,
    operation_mode
):

    score = 0

    # Gain influence
    if gain_score >= 85:
        score += 25
    elif gain_score >= 70:
        score += 18
    else:
        score += 8

    # Q-factor influence
    if q_factor_score >= 85:
        score += 30
    elif q_factor_score >= 70:
        score += 20
    else:
        score += 10

    # Thermal stability influence
    if thermal_score >= 80:
        score += 20
    elif thermal_score >= 60:
        score += 12
    else:
        score += 5

    # Cavity geometry influence
    if cavity_geometry in ["Compact Fabry-Perot", "Linear Resonator"]:
        score += 15
    else:
        score += 8

    # Operation mode influence
    if operation_mode == "CW Laser Compatible":
        score += 10
    elif operation_mode == "Hybrid Operation":
        score += 8
    else:
        score += 6

    return min(score, 100)


def classify_beam_quality(score):

    if score >= 85:
        return "Excellent Beam Quality"

    elif score >= 70:
        return "High Beam Quality"

    elif score >= 50:
        return "Moderate Beam Quality"

    else:
        return "Poor Beam Quality"