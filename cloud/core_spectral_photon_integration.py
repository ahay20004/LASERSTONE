"""Bounded real two-module integration: legacy photon physics + spectral region.

The legacy photon adapter is benchmarked independently against SI constants.
The spectral classifier is a *legacy label*, not a certified spectrum taxonomy.
No GUI, university assets, network, or experimental data are used.
"""
from dataclasses import dataclass
from math import isfinite

from cloud.legacy_laser_photon_adapter import (
    LaserPhotonRequest, evaluate_legacy_laser_photon,
)
from spectral_region import predict_spectral_region


@dataclass(frozen=True)
class SpectralPhotonRequest:
    wavelength_nm: float
    refractive_index: float = 1.0


def evaluate_spectral_photon(request: SpectralPhotonRequest):
    if not isinstance(request, SpectralPhotonRequest):
        raise TypeError("SpectralPhotonRequest required")
    wavelength = request.wavelength_nm
    if (isinstance(wavelength, bool) or not isinstance(wavelength, (int, float))
            or not isfinite(wavelength) or not 380 <= wavelength <= 1100):
        raise ValueError("wavelength_nm must be finite and within 380–1100 nm")
    photon = evaluate_legacy_laser_photon(
        LaserPhotonRequest(wavelength, request.refractive_index)
    )
    label = predict_spectral_region(wavelength)
    if label not in ("Visible", "Near Infrared (NIR)"):
        raise ValueError("unexpected legacy spectral classification")
    return {
        "scope": "LEGACY_PHOTON_SPECTRAL_INTEGRATION_380_1100_NM",
        "wavelength_nm": wavelength,
        "spectral_label": label,
        "spectral_label_source": "spectral_region.predict_spectral_region",
        "spectral_boundary_policy": "Legacy 380–750 nm inclusive Visible; >750 nm NIR",
        "photon": photon,
        "integration_passed": photon["benchmark_passed"],
        "experimental_validation": False,
        "cloud_service": False,
        "limitations": [
            "Legacy spectral thresholds are software conventions, not a universal standard",
            "No source recommendation, gain, cavity, material or experimental validation",
            "Input wavelength is shared explicitly by both existing modules",
        ],
    }
