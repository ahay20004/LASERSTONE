"""Fail-closed bridge from G23-style outputs to G3 evidence eligibility.

This module NEVER converts computed values or heuristic scores into measured
evidence. External evidence labels require an explicit, separately audited G3
intake; a caller cannot self-certify a measurement through this bridge.
"""
import json
from pathlib import Path

PHYSICS_DERIVED = "PHYSICS_DERIVED"
HEURISTIC_SCORE = "HEURISTIC_SCORE"
EXPERIMENTAL_EVIDENCE = "EXPERIMENTAL_EVIDENCE"

DERIVED_FIELDS = frozenset({
    "frequency_hz", "photon_energy_ev", "cavity_length_m",
    "free_spectral_range_hz", "frequency_formula", "energy_formula",
    "cavity_formula", "fsr_formula", "gain_condition", "basis_status",
})
HEURISTIC_FIELDS = frozenset({
    "gain_score", "laser_efficiency_score", "thermal_score", "q_factor_score",
    "material_score", "lri_score", "consistency_score", "consistency_class",
})

def classify(g23_output):
    """Classify known G23 keys without making scientific evidence claims."""
    if not isinstance(g23_output, dict):
        raise ValueError("G23 output must be a mapping")
    classified = []
    for key, value in sorted(g23_output.items()):
        if key in DERIVED_FIELDS:
            kind = PHYSICS_DERIVED
        elif key in HEURISTIC_FIELDS:
            kind = HEURISTIC_SCORE
        else:
            raise ValueError(f"Unreviewed G23 output field: {key}")
        classified.append({"field": key, "kind": kind, "value": value})
    return {
        "bridge_version": "0.1",
        "status": "CLASSIFIED_NOT_VERIFIED",
        "outputs": classified,
        "g3_evidence_types": [],
        "claims_authorized": [],
        "limitations": [
            "Derived fields include model assumptions; their classification is not validation.",
            "Heuristic scores cannot establish laser gain, threshold or measured performance.",
            "No experimental evidence is inferred from G23 outputs.",
            "G3 evidence intake and provenance checks remain separate mandatory gates.",
        ],
    }

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--g23-json", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    data = json.loads(Path(args.g23_json).read_text(encoding="utf-8"))
    result = classify(data)
    target = Path(args.out)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(result, indent=2, allow_nan=False), encoding="utf-8")
    print(json.dumps(result, indent=2, allow_nan=False))

if __name__ == "__main__":
    main()
