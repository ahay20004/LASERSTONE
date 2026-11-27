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


def audit_physical_evidence(plant):
    """Audit explicit SI cavity evidence, not heuristic scores or experimental proof."""
    from laser_physics_engine import calculate_laser_physics

    required = ("lambda_em", "refractive_index", "cavity_length_m",
                "mirror_r1", "mirror_r2", "internal_loss_m_inv", "gain_m_inv")
    missing = [key for key in required if plant.get(key) is None]
    try:
        result = calculate_laser_physics(plant)
        if plant.get("lambda_em") is not None and float(plant["lambda_em"]) <= 0:
            raise ValueError("Explicit wavelength must be positive")
    except (ValueError, TypeError, OverflowError, ZeroDivisionError) as exc:
        return {"status": "INVALID", "missing": missing, "reason": str(exc),
                "experimental_validation": False}
    if missing:
        return {"status": "UNVERIFIED", "missing": missing,
                "experimental_validation": False}
    threshold = result["threshold_status"]
    claim = plant.get("claims_above_threshold")
    if claim is not None and not isinstance(claim, bool):
        return {"status": "INVALID", "missing": [], "reason": "Claim must be boolean",
                "experimental_validation": False}
    status = "UNVERIFIED" if claim is None else (
        "CONSISTENT" if claim == (threshold == "ABOVE_THRESHOLD") else "INCONSISTENT")
    return {"status": status, "missing": [], "threshold_status": threshold,
            "gain_margin_m_inv": result["gain_margin_m_inv"],
            "scope": "Agreement with homogeneous cavity threshold model only",
            "experimental_validation": False}
