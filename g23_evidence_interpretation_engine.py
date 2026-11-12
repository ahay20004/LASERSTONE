"""Evidence-aware interpretation for LASERSTONE G23."""

from __future__ import annotations

from typing import Any, Mapping

from physical_spectral_evidence_engine import analyze_physical_spectral_evidence


def generate_evidence_interpretation(
    normalized: Mapping[str, Any],
) -> list[str]:
    analysis = analyze_physical_spectral_evidence(normalized)
    statements = []

    if analysis["lambda_abs_nm"] is not None:
        statements.append(
            f"Reported absorption peak: {analysis['lambda_abs_nm']} nm."
        )

    if analysis["epsilon_M_cm"] is not None:
        statements.append(
            "A molar extinction coefficient is reported, enabling a "
            "traceable Beer-Lambert derivation of molecular absorption "
            "cross section."
        )

    if analysis["sigma_a_cm2"] is not None:
        statements.append(
            "Derived molecular absorption cross section: "
            f"{analysis['sigma_a_cm2']:.6e} cm^2 molecule^-1."
        )

    if analysis["phi_f"] is not None:
        statements.append(
            f"Reported fluorescence quantum yield: {analysis['phi_f']}."
        )

    if analysis["lambda_em_nm"] is not None:
        statements.append(
            f"Reported emission peak: {analysis['lambda_em_nm']} nm."
        )
    else:
        statements.append(
            "Emission peak is not available in the current evidence record."
        )

    if analysis["stokes_shift_nm"] is not None:
        statements.append(
            "Derived Stokes shift: "
            f"{analysis['stokes_shift_nm']:.3f} nm "
            f"({analysis['stokes_shift_cm_inv']:.3f} cm^-1)."
        )

    statements.append(
        "Current spectral evidence does not by itself establish optical gain, "
        "lasing feasibility, laser efficiency, Q-factor, or prototype readiness."
    )

    return statements
