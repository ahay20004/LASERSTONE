def evaluate_q_factor(
    plant,
    gain_score,
    thermal_score,
    photobleaching_score
):

    q_score = 0

    # Gain contribution
    if gain_score >= 85:
        q_score += 35

    elif gain_score >= 70:
        q_score += 25

    else:
        q_score += 10

    # Thermal stability contribution
    if thermal_score >= 80:
        q_score += 25

    elif thermal_score >= 60:
        q_score += 15

    else:
        q_score += 5

    # Photobleaching resistance
    if photobleaching_score >= 80:
        q_score += 20

    elif photobleaching_score >= 60:
        q_score += 12

    else:
        q_score += 5

    # Refractive index influence
    if 1.3 <= plant["refractive_index"] <= 1.5:
        q_score += 20

    else:
        q_score += 10

    return min(q_score, 100)


def classify_q_factor(score):

    if score >= 85:
        return "Ultra High-Q Resonance"

    elif score >= 70:
        return "High-Q Resonance"

    elif score >= 50:
        return "Moderate-Q Resonance"

    else:
        return "Low-Q Resonance"