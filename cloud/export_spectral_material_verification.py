"""Export a reproducible synthetic spectral-contract verification report."""
import json
from pathlib import Path
from cloud.canonical_spectral_material_adapter import (
    SpectralMaterialRequest, evaluate_spectral_material,
)
from cloud.core_material_score_gate import ScoreInput
from cloud.spectral_material_contract_diagnostic import (
    LABEL_CASES, diagnose_spectral_material_contract,
)


def build_report():
    cases = []
    for label, spectral in LABEL_CASES:
        scores = {key: ScoreInput(value, "synthetic-only", "SIMULATED")
                  for key, value in (
                      ("lsi", 6), ("thermal_score", 80), ("q_factor_score", 75),
                      ("beam_quality_score", 70), ("laser_efficiency_score", 65))}
        result = evaluate_spectral_material(SpectralMaterialRequest(dict(spectral), scores))
        cases.append({
            "label": label, "canonical_score": result["canonical_spectral_score"],
            "legacy_main_style_score": result["legacy_main_style_material_score"],
            "corrected_score": result["corrected_material_score"],
            "delta": result["material_score_delta"],
            "main_pipeline_corrected": result["main_pipeline_corrected"],
        })
    return {
        "scope": "SYNTHETIC_CONTRACT_VERIFICATION_ONLY",
        "baseline": diagnose_spectral_material_contract(),
        "policy": "High=100; Medium=60; Low=30",
        "cases": cases,
        "scientific_validation": False,
        "experimental_validation": False,
        "main_pipeline_modified": False,
        "next_gate": "Test and approve a targeted main.py handoff before production correction",
    }


def main():
    report = build_report()
    out = Path("audit-artifacts")
    out.mkdir(exist_ok=True)
    (out / "spectral_material_verification.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# Spectral-material interface correction — synthetic verification",
        "", "The canonical adapter is implemented and tested; original main.py is NOT changed.",
        "", "| Label | Canonical spectral score | Historical material | Adapter material | Delta |",
        "|---|---:|---:|---:|---:|",
    ]
    for case in report["cases"]:
        lines.append(f"| {case['label']} | {case['canonical_score']} | "
                     f"{case['legacy_main_style_score']:.2f} | "
                     f"{case['corrected_score']:.2f} | {case['delta']:+.2f} |")
    lines += ["", "All values are synthetic regression fixtures, not measured material data.",
              "The historical main.py pipeline still uses its original spectral label handoff.",
              "No physics calibration or full production integration is claimed.", ""]
    (out / "SPECTRAL_MATERIAL_VERIFICATION.md").write_text(
        "\n".join(lines), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
