"""Read-only cross-engine spectral label contract diagnostic.

Detects semantic mapping discrepancies; never modifies the original engines.
"""
import json
from data_standardization_engine import standardize_quality_value
from material_score_engine import convert_spectral_quality_to_score
from spectral_quality_engine import calculate_spectral_quality

LABEL_CASES = (
    ("High", {"phi": .8, "tau": 5.0, "sigma_a": 4.0, "knr": .2}),
    ("Medium", {"phi": .5, "tau": 3.0, "sigma_a": 2.0, "knr": .4}),
    ("Low", {"phi": .2, "tau": 1.0, "sigma_a": .1, "knr": 2.0}),
)


def diagnose_spectral_material_contract():
    rows = []
    for expected, sample in LABEL_CASES:
        observed = calculate_spectral_quality(sample)
        if observed != expected:
            raise ValueError(f"synthetic fixture expected {expected}, got {observed}")
        standard = standardize_quality_value(observed)
        material = convert_spectral_quality_to_score(observed)
        rows.append({
            "source_engine": "spectral_quality_engine.calculate_spectral_quality",
            "label": observed, "standardization_score": standard,
            "material_direct_conversion_score": material,
            "difference": material - standard,
            "mapping_agrees": standard == material,
            "synthetic_fixture_only": True,
        })
    return {
        "scope": "LEGACY_LABEL_INTERFACE_DIAGNOSTIC",
        "rows": rows,
        "mismatched_labels": [r["label"] for r in rows if not r["mapping_agrees"]],
        "original_engines_modified": False,
        "physical_validation": False,
        "recommendation": (
            "Specify a single explicit mapping contract before connecting raw spectral "
            "labels to material scoring; do not silently replace legacy semantics."
        ),
    }


if __name__ == "__main__":
    print(json.dumps(diagnose_spectral_material_contract(), indent=2))
