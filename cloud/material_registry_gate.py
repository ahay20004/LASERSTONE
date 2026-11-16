"""Material-property resolution gate for LASERSTONE equation contracts.

An explicit, caller-supplied registry; no bundled material constants or
fabricated measurements. Exact wavelength lookup only (no interpolation).
"""
from dataclasses import dataclass
from math import isclose, isfinite

from cloud.equation_contract import (
    AttenuationRequest, EquationResult, Quantity, calculate_attenuation,
)


@dataclass(frozen=True)
class OpticalRecord:
    material_id: str
    wavelength_nm: float
    alpha_inv_cm: float
    source: str
    evidence_state: str
    applicable_depth_cm: tuple[float, float]
    model: str = "beer_lambert_uniform_absorption_v1"


def resolve_attenuation(
    material_id: str,
    wavelength_nm: float,
    incident_mw_cm2: float,
    depth_cm: float,
    records: tuple[OpticalRecord, ...],
) -> EquationResult:
    """Reject missing, ambiguous or out-of-range properties rather than guessing."""
    if not material_id.strip() or not all(
        isfinite(v) for v in (wavelength_nm, incident_mw_cm2, depth_cm)
    ):
        raise ValueError("material ID and finite inputs required")
    if wavelength_nm <= 0 or incident_mw_cm2 < 0 or depth_cm < 0:
        raise ValueError("invalid wavelength, intensity or depth")
    matches = [
        r for r in records
        if r.material_id == material_id
        and isfinite(r.wavelength_nm)
        and isclose(r.wavelength_nm, wavelength_nm, rel_tol=0, abs_tol=1e-9)
    ]
    if len(matches) != 1:
        raise ValueError("exactly one material record at this wavelength is required")
    record = matches[0]
    if record.model != "beer_lambert_uniform_absorption_v1":
        raise ValueError("unsupported optical model")
    if record.evidence_state not in ("MEASURED", "DERIVED"):
        raise ValueError("material coefficient must be measured or traceably derived")
    if not record.source.strip() or not isfinite(record.alpha_inv_cm) or record.alpha_inv_cm < 0:
        raise ValueError("invalid coefficient or missing provenance")
    lower, upper = record.applicable_depth_cm
    if not (isfinite(lower) and isfinite(upper) and 0 <= lower <= upper):
        raise ValueError("invalid applicability range")
    if not lower <= depth_cm <= upper:
        raise ValueError("depth outside recorded applicability range")
    return calculate_attenuation(AttenuationRequest(
        wavelength_nm=Quantity(wavelength_nm, "nm", "user-selected wavelength", "DERIVED"),
        incident_mw_cm2=Quantity(incident_mw_cm2, "mW/cm2", "user-supplied incident intensity", "DERIVED"),
        depth_cm=Quantity(depth_cm, "cm", "user-supplied path length", "DERIVED"),
        alpha_inv_cm=Quantity(record.alpha_inv_cm, "cm^-1", record.source, record.evidence_state),
    ))
