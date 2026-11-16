"""Evidence-gated execution of the existing thermal heuristic.

This is a legacy screening score, not thermometry or a physical thermal
stability measurement. Source identifiers are caller supplied, not verified.
"""
from dataclasses import dataclass
from math import isfinite

from thermal_engine import evaluate_thermal_stability, classify_thermal_stability

FIELDS = ("phi", "tau", "knr", "refractive_index")
EVIDENCE = frozenset(("MEASURED", "DERIVED", "SIMULATED", "PREDICTED"))


@dataclass(frozen=True)
class ThermalInput:
    value: float
    unit: str
    source: str
    evidence_state: str


UNITS = {"phi": "1", "tau": "ns", "knr": "ns^-1", "refractive_index": "1"}


def evaluate_thermal_screen(inputs: dict[str, ThermalInput]):
    if not isinstance(inputs, dict) or set(inputs) != set(FIELDS):
        raise ValueError("exactly four required thermal-screen inputs")
    payload, provenance = {}, {}
    for name in FIELDS:
        item = inputs[name]
        if not isinstance(item, ThermalInput):
            raise ValueError(f"{name}: ThermalInput required")
        if (isinstance(item.value, bool) or not isinstance(item.value, (int, float))
                or not isfinite(item.value)):
            raise ValueError(f"{name}: finite numeric value required")
        if item.unit != UNITS[name]:
            raise ValueError(f"{name}: expected canonical unit {UNITS[name]}")
        if not isinstance(item.source, str) or not item.source.strip():
            raise ValueError(f"{name}: source required")
        if item.evidence_state not in EVIDENCE:
            raise ValueError(f"{name}: evidence state required")
        value = float(item.value)
        if (name == "phi" and not 0 <= value <= 1) or (
            name in ("tau", "knr") and value <= 0
        ) or (name == "refractive_index" and not 1 <= value <= 5):
            raise ValueError(f"{name}: outside declared domain")
        payload[name] = value
        provenance[name] = {
            "source": item.source, "unit": item.unit,
            "evidence_state": item.evidence_state,
        }
    score = evaluate_thermal_stability(payload)
    independent = (
        (30 if payload["phi"] >= .7 else 20 if payload["phi"] >= .5 else 10)
        + (25 if payload["tau"] >= 4 else 15 if payload["tau"] >= 2 else 5)
        + (25 if payload["knr"] <= .35 else 15 if payload["knr"] <= .5 else 5)
        + (20 if payload["refractive_index"] <= 1.4 else 10)
    )
    if score != independent:
        raise ValueError("legacy thermal heuristic regression mismatch")
    return {
        "engine": "thermal_engine.evaluate_thermal_stability",
        "scope": "PROVENANCE_GATED_LEGACY_THERMAL_HEURISTIC",
        "score": score,
        "legacy_classification": classify_thermal_stability(score),
        "input_provenance": provenance,
        "independent_formula_agreement": True,
        "physical_thermal_stability_validated": False,
        "experimentally_validated": False,
        "university_connected": False,
        "limitations": [
            "Legacy threshold score is not a measured temperature or thermal lifetime",
            "Legacy coefficients and thresholds lack independent calibration here",
            "Assumed canonical lifetime ns and decay rate ns^-1 require source-level confirmation",
            "Caller-supplied provenance is not independently authenticated",
        ],
    }
