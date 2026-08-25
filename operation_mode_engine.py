def evaluate_operation_mode(plant, thermal_score, feasibility_score):

    cw_score = 0
    pulsed_score = 0

    # Thermal stability effect
    if thermal_score >= 80:
        cw_score += 40
        pulsed_score += 20

    elif thermal_score >= 60:
        cw_score += 25
        pulsed_score += 25

    else:
        cw_score += 10
        pulsed_score += 35

    # Feasibility contribution
    if feasibility_score >= 80:
        cw_score += 35
        pulsed_score += 35

    elif feasibility_score >= 60:
        cw_score += 25
        pulsed_score += 30

    else:
        pulsed_score += 20

    # Non-radiative decay
    if plant["knr"] <= 0.35:
        cw_score += 25
    else:
        pulsed_score += 15

    # Final classification
    if cw_score > pulsed_score:
        mode = "CW Laser Compatible"

    elif pulsed_score > cw_score:
        mode = "Pulsed Laser Compatible"

    else:
        mode = "Hybrid Operation"

    return {
        "cw_score": cw_score,
        "pulsed_score": pulsed_score,
        "mode": mode
    }