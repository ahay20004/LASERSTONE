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



def generate_integrated_evidence_decision(records, claims_above_threshold=None, fluorescence_correlation=None, threshold_independent=None, q_correlation=None):
    """Canonical parameter records feed existing engines; no implicit unit conversion."""
    from data_validator import audit_parameter_record
    from physics_evidence_engine import audit_fluorescence_decay, audit_fluorescence_uncertainty
    from qfactor_engine import calculate_physical_q, audit_q_uncertainty
    from laser_physics_engine import C, audit_threshold_uncertainty

    audits = {k: audit_parameter_record(k, v) for k, v in records.items()}
    values = {k: v["value"] for k, v in records.items()
              if audits[k]["status"] == "RECORDED"}
    cavity_keys = ("lambda_em", "refractive_index", "group_index", "cavity_length_m",
                   "mirror_r1", "mirror_r2", "internal_loss_m_inv", "gain_m_inv")
    def compatible(keys):
        return len({records[k]["conditions_id"] for k in keys if k in values}) <= 1
    cavity_ok = compatible(cavity_keys)
    fluorescence_ok = compatible(("quantum_yield", "lifetime_s"))
    q_ok = compatible(("resonance_frequency_hz", "linewidth_hz", "energy_lifetime_s"))
    plant = {k: values[k] for k in cavity_keys if k in values and cavity_ok}
    plant["claims_above_threshold"] = claims_above_threshold
    result = generate_evidence_decision(plant)
    fluorescence = audit_fluorescence_decay(values.get("quantum_yield"), values.get("lifetime_s"))
    frequency = values.get("resonance_frequency_hz")
    q = calculate_physical_q(frequency, values.get("linewidth_hz"), values.get("energy_lifetime_s"))
    uncertainty = audit_fluorescence_uncertainty(
        values.get("quantum_yield"), values.get("lifetime_s"),
        records["quantum_yield"]["standard_uncertainty"] if "quantum_yield" in values else None,
        records["lifetime_s"]["standard_uncertainty"] if "lifetime_s" in values else None,
        fluorescence_correlation)
    if not fluorescence_ok:
        fluorescence = uncertainty = {"status": "UNVERIFIED", "reason": "CONDITIONS_MISMATCH"}
    if not q_ok:
        q = {"status": "UNVERIFIED", "reason": "CONDITIONS_MISMATCH"}
    result["conditions_compatible"] = {"cavity": cavity_ok, "fluorescence": fluorescence_ok, "q": q_ok}
    if not all(result["conditions_compatible"].values()):
        result["next_action"] = "RECONCILE_CONDITIONS"
    threshold_u = audit_threshold_uncertainty(
        plant, {k: records[k]["standard_uncertainty"] for k in plant if k in values},
        threshold_independent)
    q_u = {"status": "UNVERIFIED"}
    if q_ok and q["status"] == "DERIVED" and q.get("basis") == "power_fwhm":
        u_frequency = records["resonance_frequency_hz"]["standard_uncertainty"]
        q_u = audit_q_uncertainty(frequency, values["linewidth_hz"], u_frequency,
                                  records["linewidth_hz"]["standard_uncertainty"], q_correlation)
    result["threshold_uncertainty"] = threshold_u
    result["q_uncertainty"] = q_u
    result["fluorescence_uncertainty"] = uncertainty
    result.update(parameter_audits=audits, fluorescence=fluorescence, physical_q=q,
                  uncertainty_propagated=False, source_authentication="NOT_VERIFIED")
    if any(a["status"] == "INVALID" for a in audits.values()) or any(
            a["status"] == "INVALID" for a in (fluorescence, q, uncertainty, threshold_u, q_u)):
        result["next_action"] = "CORRECT_INPUTS"
    return result
