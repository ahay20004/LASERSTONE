"""Isolated, evidence-bounded adapter for the existing laser physics engine.

Runs the legacy callable only after strict input validation. Independent SI
benchmark is intentionally separate from legacy rounded constants.
No GUI, material database, network or cloud endpoint is involved.
"""
from dataclasses import dataclass
from math import isfinite

from laser_physics_engine import calculate_laser_physics

H = 6.62607015e-34
C = 299792458.0
EV = 1.602176634e-19


@dataclass(frozen=True)
class LaserPhotonRequest:
    wavelength_nm: float
    refractive_index: float = 1.0


def evaluate_legacy_laser_photon(request: LaserPhotonRequest):
    if not isinstance(request, LaserPhotonRequest):
        raise TypeError("LaserPhotonRequest required")
    for name, value in (("wavelength_nm", request.wavelength_nm),
                        ("refractive_index", request.refractive_index)):
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not isfinite(value) or value <= 0:
            raise ValueError(f"{name} must be a finite positive number")
    if not (100 <= request.wavelength_nm <= 100000):
        raise ValueError("wavelength_nm outside declared adapter scope 100–100000 nm")
    if not (1 <= request.refractive_index <= 5):
        raise ValueError("refractive_index outside declared adapter scope 1–5")
    legacy = calculate_laser_physics({
        "lambda_em": float(request.wavelength_nm),
        "refractive_index": float(request.refractive_index),
    })
    expected_frequency = C / (request.wavelength_nm * 1e-9)
    expected_energy = H * expected_frequency / EV
    comparisons = {}
    for key, expected in (("frequency_hz", expected_frequency),
                          ("photon_energy_ev", expected_energy)):
        observed = legacy.get(key)
        if isinstance(observed, bool) or not isinstance(observed, (int, float)) or not isfinite(observed):
            raise ValueError(f"legacy engine returned invalid {key}")
        comparisons[key] = {
            "legacy_value": observed,
            "independent_si_value": expected,
            "relative_error": abs(observed - expected) / expected,
            "within_tolerance": abs(observed - expected) / expected <= 0.001,
        }
    return {
        "engine": "laser_physics_engine.calculate_laser_physics",
        "scope": "PHOTON_FREQUENCY_ENERGY_ONLY",
        "wavelength_nm": request.wavelength_nm,
        "refractive_index": request.refractive_index,
        "comparisons": comparisons,
        "benchmark_passed": all(item["within_tolerance"] for item in comparisons.values()),
        "evidence_state": "DERIVED",
        "validated_experimentally": False,
        "cloud_connected": False,
        "assumptions": [
            "Vacuum photon frequency and energy independent of refractive index",
            "Legacy engine uses rounded constants; independent reference uses exact SI constants",
            "Legacy cavity length, free spectral range and gain claims are excluded from this benchmark",
            "No experimental measurement, external simulator or live cloud engine is invoked",
        ],
    }
