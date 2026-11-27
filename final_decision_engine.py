def generate_final_decision(plant):

    material_score = plant.get("material_score", 0)
    lri_score = plant.get("lri_score", 0)
    consistency_score = plant.get("physics_consistency_score", 0)

    if (
        material_score >= 85
        and lri_score >= 80
        and consistency_score >= 85
    ):
        return "Recommended for Advanced Laser Prototype"

    elif (
        material_score >= 70
        and lri_score >= 65
        and consistency_score >= 75
    ):
        return "Recommended for Laboratory Laser Testing"

    elif (
        material_score >= 55
        and consistency_score >= 60
    ):
        return "Recommended for Further Spectroscopic Study"

    else:
        return "Not Recommended for Laser Development at This Stage"


def generate_evidence_decision(plant):
    """Research triage only; no prototype or publication authorization."""
    from scientific_confidence_engine import assess_evidence_confidence

    confidence = assess_evidence_confidence(plant)
    status = confidence["model_consistency"]
    next_action = {
        "INVALID": "CORRECT_INPUTS",
        "INCONSISTENT": "RECONCILE_MODEL_AND_CLAIM",
        "UNVERIFIED": "COMPLETE_MODEL_EVIDENCE",
        "CONSISTENT": "VERIFY_INDEPENDENT_EVIDENCE",
    }.get(status, "REVIEW_REQUIRED")
    return {
        "decision": "HOLD",
        "next_action": next_action,
        "confidence": confidence,
        "claims_authorized": [],
        "prototype_authorized": False,
        "publication_authorized": False,
    }
