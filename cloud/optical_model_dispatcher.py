"""Conservative LASERSTONE optical model dispatcher.

This layer selects supported physics; it does not connect to live agents,
external material databases, or experimental validation systems.
"""
from dataclasses import dataclass
from typing import Literal

from cloud.equation_contract import EquationResult
from cloud.material_registry_gate import OpticalRecord, resolve_attenuation

OpticalRegime = Literal[
    "bulk_absorption", "interface_reflection", "thin_film_interference",
    "polarization_anisotropy", "multiple_scattering", "nonlinear_optics",
]


class UnsupportedOpticalRegime(ValueError):
    """Requested physics requires an engine not integrated with this dispatcher."""


@dataclass(frozen=True)
class OpticalScenario:
    material_id: str
    wavelength_nm: float
    incident_mw_cm2: float
    depth_cm: float
    regime: OpticalRegime
    homogeneous: bool
    constant_alpha: bool
    interface_effects_negligible: bool


def dispatch_optical_model(
    scenario: OpticalScenario,
    records: tuple[OpticalRecord, ...],
) -> EquationResult:
    """Run only a justified homogeneous Beer-Lambert model.

    Reject unsupported regimes rather than silently returning a plausible
    but physically incomplete result.
    """
    if scenario.regime != "bulk_absorption":
        raise UnsupportedOpticalRegime(
            f"{scenario.regime}: no verified execution adapter is registered"
        )
    if not all((
        scenario.homogeneous,
        scenario.constant_alpha,
        scenario.interface_effects_negligible,
    )):
        raise UnsupportedOpticalRegime(
            "Beer-Lambert assumptions not confirmed; no fallback model is available"
        )
    return resolve_attenuation(
        material_id=scenario.material_id,
        wavelength_nm=scenario.wavelength_nm,
        incident_mw_cm2=scenario.incident_mw_cm2,
        depth_cm=scenario.depth_cm,
        records=records,
    )
