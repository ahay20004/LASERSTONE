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



def generate_integrated_evidence_decision(records, claims_above_threshold=None, fluorescence_correlation=None):
    """Canonical parameter records feed existing engines; no implicit unit conversion."""
    from data_validator import audit_parameter_record
    from physics_evidence_engine import audit_fluorescence_decay, audit_fluorescence_uncertainty
    from qfactor_engine import calculate_physical_q
    from laser_physics_engine import C

    audits = {k: audit_parameter_record(k, v) for k, v in records.items()}
    values = {k: v["value"] for k, v in records.items()
              if audits[k]["status"] == "RECORDED"}
    cavity_keys = ("lambda_em", "refractive_index", "group_index", "cavity_length_m",
                   "mirror_r1", "mirror_r2", "internal_loss_m_inv", "gain_m_inv")
    plant = {k: values[k] for k in cavity_keys if k in values}
    plant["claims_above_threshold"] = claims_above_threshold
    result = generate_evidence_decision(plant)
    fluorescence = audit_fluorescence_decay(values.get("quantum_yield"), values.get("lifetime_s"))
    wavelength = values.get("lambda_em")
    frequency = C / (wavelength * 1e-9) if wavelength and wavelength * 1e-9 else None
    q = calculate_physical_q(frequency, values.get("linewidth_hz"), values.get("energy_lifetime_s"))
    uncertainty = audit_fluorescence_uncertainty(
        values.get("quantum_yield"), values.get("lifetime_s"),
        records["quantum_yield"]["standard_uncertainty"] if "quantum_yield" in values else None,
        records["lifetime_s"]["standard_uncertainty"] if "lifetime_s" in values else None,
        fluorescence_correlation)
    result["fluorescence_uncertainty"] = uncertainty
    result.update(parameter_audits=audits, fluorescence=fluorescence, physical_q=q,
                  uncertainty_propagated=False, source_authentication="NOT_VERIFIED")
    if any(a["status"] == "INVALID" for a in audits.values()) or any(
            a["status"] == "INVALID" for a in (fluorescence, q, uncertainty)):
        result["next_action"] = "CORRECT_INPUTS"
    return result
