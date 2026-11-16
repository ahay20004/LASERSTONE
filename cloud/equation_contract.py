"""LASERSTONE scientific equation contract, foundation only.

Pure standard-library reference implementation. No live engines, agents,
measured material constants, or experimental validation are implied.
"""
from dataclasses import dataclass
from math import exp, isfinite
from typing import Literal

EvidenceState = Literal["MEASURED", "DERIVED", "SIMULATED", "PREDICTED"]


@dataclass(frozen=True)
class Quantity:
    value: float
    unit: str
    source: str
    evidence_state: EvidenceState


@dataclass(frozen=True)
class AttenuationRequest:
    wavelength_nm: Quantity
    incident_mw_cm2: Quantity
    depth_cm: Quantity
    alpha_inv_cm: Quantity


@dataclass(frozen=True)
class EquationResult:
    model_id: str
    relative_transmission: float
    transmitted_mw_cm2: float
    evidence_state: EvidenceState
    validated_experimentally: bool
    input_provenance: dict[str, str]
    assumptions: tuple[str, ...]


def calculate_attenuation(request: AttenuationRequest) -> EquationResult:
    """Calculate I=I0*exp(-alpha*d) for supplied coefficients only.

    The alpha coefficient must come from a named source; no material database
    or wavelength interpolation is performed here. All outputs are SIMULATED
    and explicitly not experimentally validated.
    """
    inputs = {
        "wavelength_nm": (request.wavelength_nm, "nm"),
        "incident_mw_cm2": (request.incident_mw_cm2, "mW/cm2"),
        "depth_cm": (request.depth_cm, "cm"),
        "alpha_inv_cm": (request.alpha_inv_cm, "cm^-1"),
    }
    for name, (quantity, expected_unit) in inputs.items():
        if quantity.unit != expected_unit:
            raise ValueError(f"{name}: expected unit {expected_unit}")
        if not isfinite(quantity.value):
            raise ValueError(f"{name}: finite value required")
        if not quantity.source.strip():
            raise ValueError(f"{name}: source/provenance required")
        if quantity.evidence_state not in ("MEASURED", "DERIVED", "SIMULATED", "PREDICTED"):
            raise ValueError(f"{name}: invalid evidence state")
    if request.wavelength_nm.value <= 0:
        raise ValueError("wavelength must be positive")
    if request.incident_mw_cm2.value < 0 or request.depth_cm.value < 0 or request.alpha_inv_cm.value < 0:
        raise ValueError("incident intensity, depth and attenuation must be nonnegative")
    ratio = exp(-request.alpha_inv_cm.value * request.depth_cm.value)
    return EquationResult(
        model_id="beer_lambert_uniform_absorption_v1",
        relative_transmission=ratio,
        transmitted_mw_cm2=request.incident_mw_cm2.value * ratio,
        evidence_state="SIMULATED",
        validated_experimentally=False,
        input_provenance={name: quantity.source for name, (quantity, _) in inputs.items()},
        assumptions=(
            "Homogeneous medium and constant alpha at selected wavelength",
            "No interface reflection, scattering, interference, or nonlinear response",
            "No claim of experimental validation or independent engine execution",
        ),
    )
