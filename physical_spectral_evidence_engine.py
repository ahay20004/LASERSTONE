"""Physical spectral evidence analysis for LASERSTONE G23.

This module evaluates evidence completeness and derives only transparent
spectral quantities. It deliberately does NOT calculate laser gain, lasing
feasibility, or a material-performance score.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from photochemcad_evidence_adapter import DERIVED, MISSING, REPORTED

CORE_REPORTED_FIELDS = (
    "lambda_abs_nm",
    "lambda_em_nm",
    "epsilon_M_cm",
    "phi_f",
)

LASER_CLAIM_STATUS = "NOT_ESTABLISHED_FROM_SPECTRAL_EVIDENCE_ALONE"


def analyze_physical_spectral_evidence(
    normalized: Mapping[str, Any],
) -> dict[str, Any]:
    """Analyze a normalized PhotochemCAD record without inventing data.

    Evidence completeness is based only on four independent reported core
    quantities. Derived sigma_a_cm2 is intentionally excluded from the
    completeness numerator because it is not independent of epsilon.
    """
    if not isinstance(normalized, Mapping):
        raise TypeError("normalized must be a mapping")

    source = deepcopy(dict(normalized))
    if source.get("source_database") != "PhotochemCAD":
        raise ValueError("source_database must be PhotochemCAD")

    field_evidence = source.get("field_evidence")
    if not isinstance(field_evidence, Mapping):
        raise ValueError("field_evidence mapping is required")

    reported_fields = [
        field
        for field in CORE_REPORTED_FIELDS
        if source.get(field) is not None
        and field_evidence.get(field, MISSING) == REPORTED
    ]
    missing_core_fields = [
        field for field in CORE_REPORTED_FIELDS if field not in reported_fields
    ]

    completeness_score = round(
        100.0 * len(reported_fields) / len(CORE_REPORTED_FIELDS),
        2,
    )

    lambda_abs = source.get("lambda_abs_nm")
    lambda_em = source.get("lambda_em_nm")

    stokes_shift_nm = None
    stokes_shift_cm_inv = None
    stokes_flag = "NOT_AVAILABLE"

    if (
        lambda_abs is not None
        and lambda_em is not None
        and field_evidence.get("lambda_abs_nm") == REPORTED
        and field_evidence.get("lambda_em_nm") == REPORTED
    ):
        lambda_abs = float(lambda_abs)
        lambda_em = float(lambda_em)
        stokes_shift_nm = lambda_em - lambda_abs
        stokes_shift_cm_inv = 1.0e7 * (
            (1.0 / lambda_abs) - (1.0 / lambda_em)
        )
        if stokes_shift_nm > 0:
            stokes_flag = "POSITIVE_STOKES_SHIFT"
        elif stokes_shift_nm == 0:
            stokes_flag = "ZERO_STOKES_SHIFT"
        else:
            stokes_flag = "NEGATIVE_STOKES_SHIFT_REQUIRES_REVIEW"

    sigma = source.get("sigma_a_cm2")
    sigma_state = field_evidence.get("sigma_a_cm2", MISSING)
    if sigma is not None and sigma_state != DERIVED:
        raise ValueError(
            "sigma_a_cm2 must be marked DERIVED for PhotochemCAD adapter records"
        )

    epsilon_reported = (
        source.get("epsilon_M_cm") is not None
        and field_evidence.get("epsilon_M_cm") == REPORTED
    )
    phi_reported = (
        source.get("phi_f") is not None
        and field_evidence.get("phi_f") == REPORTED
    )
    abs_wavelength_reported = (
        source.get("lambda_abs_nm") is not None
        and field_evidence.get("lambda_abs_nm") == REPORTED
    )
    em_wavelength_reported = (
        source.get("lambda_em_nm") is not None
        and field_evidence.get("lambda_em_nm") == REPORTED
    )

    capabilities = {
        "absorption_peak_available": abs_wavelength_reported,
        "quantitative_absorption_available": bool(
            abs_wavelength_reported and epsilon_reported and sigma is not None
        ),
        "fluorescence_peak_available": em_wavelength_reported,
        "fluorescence_quantum_yield_available": phi_reported,
        "stokes_shift_available": stokes_shift_nm is not None,
    }

    if completeness_score == 100.0:
        evidence_status = "COMPLETE_CORE_SPECTRAL_EVIDENCE"
    elif completeness_score >= 50.0:
        evidence_status = "PARTIAL_CORE_SPECTRAL_EVIDENCE"
    else:
        evidence_status = "SPARSE_CORE_SPECTRAL_EVIDENCE"

    return {
        "photochemcad_id": source.get("photochemcad_id"),
        "compound_name": source.get("compound_name"),
        "source_database": "PhotochemCAD",
        "source_url": source.get("source_url"),
        "reported_core_fields": reported_fields,
        "missing_core_fields": missing_core_fields,
        "independent_reported_count": len(reported_fields),
        "independent_core_field_count": len(CORE_REPORTED_FIELDS),
        "evidence_completeness_score": completeness_score,
        "evidence_status": evidence_status,
        "lambda_abs_nm": source.get("lambda_abs_nm"),
        "lambda_em_nm": source.get("lambda_em_nm"),
        "epsilon_M_cm": source.get("epsilon_M_cm"),
        "phi_f": source.get("phi_f"),
        "sigma_a_cm2": sigma,
        "sigma_a_unit": "cm^2 molecule^-1" if sigma is not None else None,
        "sigma_a_evidence_state": sigma_state,
        "stokes_shift_nm": stokes_shift_nm,
        "stokes_shift_cm_inv": stokes_shift_cm_inv,
        "stokes_shift_flag": stokes_flag,
        "capabilities": capabilities,
        "performance_score": None,
        "laser_gain_status": LASER_CLAIM_STATUS,
        "lasing_feasibility_status": LASER_CLAIM_STATUS,
    }
