"""LASERSTONE Paper II - G3 physical-evidence claims gate.

Classifies claim requests by the evidence modalities supplied. A passing result
means a claim is eligible for scientific consideration, NOT that it is proven.
No claim is inferred from data files automatically.

Usage:
    python projects/paper2/gate_g3.py --evidence absorption
    python projects/paper2/gate_g3.py --evidence absorption emission pump_threshold

Accepted evidence labels are deliberately conservative. All claims must still
cite instrument conditions, provenance, and quantitative uncertainty separately.
"""
import argparse
import json
from pathlib import Path

EVIDENCE_TYPES = frozenset({
    "absorption", "emission", "pump_threshold", "stimulated_emission",
    "gain_calibration", "photostability", "sample_concentration",
    "pump_geometry", "quantum_yield", "lifetime", "independent_repeat"
})

# Evidence requirements are necessary, not sufficient.
CLAIM_REQUIREMENTS = {
    "absorption_peak": ({"absorption"},),
    "spectral_shape_similarity": ({"absorption", "independent_repeat"},),
    "emission_peak": ({"emission"},),
    "stokes_shift": ({"absorption", "emission"},),
    "photoluminescence_quantum_yield": ({"quantum_yield"},),
    "photostability": ({"photostability"},),
    "stimulated_emission": ({"stimulated_emission", "pump_geometry"},),
    "optical_gain": ({"gain_calibration", "stimulated_emission", "pump_geometry"},),
    "laser_threshold": ({"pump_threshold", "stimulated_emission", "pump_geometry"},),
}

def evaluate(evidence):
    provided = set(evidence)
    invalid = provided - EVIDENCE_TYPES
    if invalid:
        raise ValueError(f"Unsupported evidence types: {', '.join(sorted(invalid))}")
    claims = {}
    for claim, alternatives in CLAIM_REQUIREMENTS.items():
        minimum = min(alternatives, key=lambda requirement: (len(requirement - provided), len(requirement)))
        missing = sorted(minimum - provided)
        claims[claim] = {
            "status": "ELIGIBLE_FOR_REVIEW" if not missing else "NOT_SUPPORTED",
            "required_evidence": sorted(minimum),
            "missing_evidence": missing,
        }
    return {
        "gate": "G3",
        "version": "1.0",
        "status": "PASS",
        "evidence_types": sorted(provided),
        "claims": claims,
        "physical_boundary_checks": {
            "absorption_only_does_not_prove_gain":
                not (provided == {"absorption"} and claims["optical_gain"]["status"] != "NOT_SUPPORTED"),
            "absorption_only_does_not_prove_threshold":
                not (provided == {"absorption"} and claims["laser_threshold"]["status"] != "NOT_SUPPORTED"),
        },
        "caveats": [
            "Eligibility is not proof; evaluate provenance, experimental conditions, and uncertainty.",
            "Normalized absorption does not provide absolute absorption cross-section.",
            "Optical gain and laser threshold require independent gain/pump-specific evidence.",
            "Independent datasets or measurement repeats are needed to substantiate repeatability.",
        ],
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--evidence", nargs="+", required=True, choices=sorted(EVIDENCE_TYPES))
    parser.add_argument("--out", default="output/g3_gate")
    args = parser.parse_args()
    result = evaluate(args.evidence)
    result["status"] = "PASS" if all(result["physical_boundary_checks"].values()) else "FAIL"
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "g3_report.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["status"] == "PASS" else 1)

if __name__ == "__main__":
    main()
