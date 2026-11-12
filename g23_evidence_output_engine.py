"""Evidence-safe spectral output representation for LASERSTONE G23."""

from __future__ import annotations

from typing import Any, Mapping

from physical_spectral_evidence_engine import analyze_physical_spectral_evidence

C = 299792458.0


def generate_evidence_output(normalized: Mapping[str, Any]) -> dict[str, Any]:
    analysis = analyze_physical_spectral_evidence(normalized)

    wavelength_nm = analysis["lambda_em_nm"]
    frequency_hz = None
    photon_energy_ev = None

    if wavelength_nm is not None:
        wavelength_m = float(wavelength_nm) * 1e-9
        frequency_hz = C / wavelength_m
        photon_energy_ev = 1239.8419843320026 / float(wavelength_nm)

    return {
        "photochemcad_id": analysis["photochemcad_id"],
        "compound_name": analysis["compound_name"],
        "reported_emission_wavelength_nm": wavelength_nm,
        "derived_frequency_hz": frequency_hz,
        "derived_photon_energy_ev": photon_energy_ev,
        "estimated_laser_power": None,
        "laser_safety_class": None,
        "laser_output_claim": "NOT_ESTABLISHED",
        "prototype_status": "NOT_ESTABLISHED",
        "evidence_status": analysis["evidence_status"],
        "source_url": analysis["source_url"],
    }
