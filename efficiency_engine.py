def evaluate_laser_efficiency(
    plant,
    gain_score,
    q_factor_score,
    beam_quality_score,
    thermal_score
):

    efficiency = 0

    # Gain medium influence
    if gain_score >= 85:
        efficiency += 30

    elif gain_score >= 70:
        efficiency += 20

    else:
        efficiency += 10

    # Q-factor contribution
    if q_factor_score >= 85:
        efficiency += 25

    elif q_factor_score >= 70:
        efficiency += 18

    else:
        efficiency += 8

    # Beam quality contribution
    if beam_quality_score >= 85:
        efficiency += 20

    elif beam_quality_score >= 70:
        efficiency += 12

    else:
        efficiency += 5

    # Thermal stability contribution
    if thermal_score >= 80:
        efficiency += 15

    elif thermal_score >= 60:
        efficiency += 10

    else:
        efficiency += 5

    # Quantum yield bonus
    if plant["phi"] >= 0.7:
        efficiency += 10

    elif plant["phi"] >= 0.5:
        efficiency += 5

    return min(efficiency, 100)


def classify_laser_efficiency(score):

    if score >= 85:
        return "Ultra Efficient Laser System"

    elif score >= 70:
        return "High Efficiency Laser System"

    elif score >= 50:
        return "Moderate Efficiency Laser System"

    else:
        return "Low Efficiency Laser System"