"""Read-only PhotochemCAD evidence normalization for LASERSTONE G23.

This module does not fetch the web, mutate production registries, or invent
missing photophysical values. It normalizes already sourced PhotochemCAD
records and derives absorption cross section only when molar extinction
coefficient epsilon is explicitly available.
"""

from __future__ import annotations

from math import log
from typing import Any, Mapping

AVOGADRO_CONSTANT = 6.02214076e23  # mol^-1, exact SI definition

REPORTED = "LITERATURE_REPORTED"
DERIVED = "DERIVED"
MISSING = "MISSING"


def epsilon_to_sigma_cm2(epsilon_m_inv_cm_inv: float) -> float:
    """Convert molar extinction coefficient epsilon to molecular cross section.

    Parameters
    ----------
    epsilon_m_inv_cm_inv:
        Molar extinction coefficient in M^-1 cm^-1.

    Returns
    -------
    float
        Absorption cross section in cm^2 molecule^-1.

    Notes
    -----
    From Beer-Lambert law:
        sigma = 1000 * ln(10) * epsilon / N_A
    """
    epsilon = _positive_number(epsilon_m_inv_cm_inv, "epsilon_M_cm")
    return 1000.0 * log(10.0) * epsilon / AVOGADRO_CONSTANT


def normalize_photochemcad_record(raw: Mapping[str, Any]) -> dict[str, Any]:
    """Normalize one user-supplied PhotochemCAD record without fabrication.

    Required identifying fields are ``photochemcad_id``, ``name`` and
    ``source_url``. Scientific fields may be absent; absent values stay None.
    No lifetime, non-radiative rate, refractive index, laser gain, or other
    unsupported quantity is inferred.
    """
    if not isinstance(raw, Mapping):
        raise TypeError("raw must be a mapping")

    photochemcad_id = _required_text(raw, "photochemcad_id")
    name = _required_text(raw, "name")
    source_url = _required_text(raw, "source_url")

    lambda_abs = _optional_positive_number(raw.get("lambda_abs_nm"), "lambda_abs_nm")
    lambda_em = _optional_positive_number(raw.get("lambda_em_nm"), "lambda_em_nm")
    epsilon = _optional_positive_number(raw.get("epsilon_M_cm"), "epsilon_M_cm")
    phi_f = _optional_fraction(raw.get("phi_f"), "phi_f")
    temperature = _optional_positive_number(raw.get("temperature_K"), "temperature_K")

    sigma = epsilon_to_sigma_cm2(epsilon) if epsilon is not None else None

    evidence = {
        "lambda_abs_nm": REPORTED if lambda_abs is not None else MISSING,
        "lambda_em_nm": REPORTED if lambda_em is not None else MISSING,
        "epsilon_M_cm": REPORTED if epsilon is not None else MISSING,
        "phi_f": REPORTED if phi_f is not None else MISSING,
        "sigma_a_cm2": DERIVED if sigma is not None else MISSING,
    }

    missing_fields = [key for key, state in evidence.items() if state == MISSING]

    return {
        "source_database": "PhotochemCAD",
        "photochemcad_id": photochemcad_id,
        "compound_name": name,
        "compound_class": _optional_text(raw.get("compound_class")),
        "plant_origin": _optional_text(raw.get("plant_origin")),
        "lambda_abs_nm": lambda_abs,
        "lambda_em_nm": lambda_em,
        "epsilon_M_cm": epsilon,
        "phi_f": phi_f,
        "sigma_a_cm2": sigma,
        "solvent": _optional_text(raw.get("solvent")),
        "temperature_K": temperature,
        "instrument": _optional_text(raw.get("instrument")),
        "reference": _optional_text(raw.get("reference")),
        "doi": _optional_text(raw.get("doi")),
        "spectrum_abs_source": _optional_text(raw.get("spectrum_abs_source")),
        "spectrum_em_source": _optional_text(raw.get("spectrum_em_source")),
        "source_url": source_url,
        "evidence_type": "LITERATURE",
        "field_evidence": evidence,
        "derivation_method": (
            "sigma_a_cm2 = 1000*ln(10)*epsilon_M_cm/N_A"
            if sigma is not None
            else None
        ),
        "missing_fields": missing_fields,
    }


def _required_text(raw: Mapping[str, Any], key: str) -> str:
    value = raw.get(key)
    text = _optional_text(value)
    if text is None:
        raise ValueError(f"{key} is required")
    return text


def _optional_text(value: Any) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise TypeError("text fields must be strings or None")
    value = value.strip()
    return value or None


def _positive_number(value: Any, field: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{field} must be numeric")
    value = float(value)
    if not math_is_finite(value) or value <= 0.0:
        raise ValueError(f"{field} must be finite and > 0")
    return value


def _optional_positive_number(value: Any, field: str) -> float | None:
    if value is None:
        return None
    return _positive_number(value, field)


def _optional_fraction(value: Any, field: str) -> float | None:
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{field} must be numeric")
    value = float(value)
    if not math_is_finite(value) or not (0.0 <= value <= 1.0):
        raise ValueError(f"{field} must be finite and within [0, 1]")
    return value


def math_is_finite(value: float) -> bool:
    return value == value and value not in (float("inf"), float("-inf"))
