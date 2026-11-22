"""Experimental measurement intake: conservative schema and dimensional checks.

Acceptance is only for a well-formed *record*, never proof of experimental
validity, calibration, independent replication or laser gain.
"""
import json
import math
from pathlib import Path

QUANTITIES = {
    "wavelength": {"dimension": "length", "units": {"nm": 1e-9, "um": 1e-6, "m": 1.0}, "positive": True},
    "frequency": {"dimension": "inverse_time", "units": {"Hz": 1.0, "THz": 1e12}, "positive": True},
    "optical_power": {"dimension": "power", "units": {"W": 1.0, "mW": 1e-3}, "positive": False},
    "pulse_duration": {"dimension": "time", "units": {"s": 1.0, "ns": 1e-9, "fs": 1e-15}, "positive": True},
    "sample_thickness": {"dimension": "length", "units": {"m": 1.0, "mm": 1e-3, "um": 1e-6}, "positive": True},
    "temperature": {"dimension": "temperature", "units": {"K": 1.0}, "positive": True},
}
REQUIRED = ("measurement_id", "quantity", "value", "unit", "uncertainty",
            "uncertainty_type", "instrument_id", "calibration_reference",
            "sample_id", "conditions", "source_id", "method", "equation_id")

def validate(record):
    if not isinstance(record, dict):
        raise ValueError("Measurement record must be an object")
    problems = []
    for key in REQUIRED:
        if key not in record:
            problems.append(f"missing: {key}")
    quantity = record.get("quantity")
    definition = QUANTITIES.get(quantity)
    if definition is None:
        problems.append("unsupported quantity")
    unit = record.get("unit")
    if definition and unit not in definition["units"]:
        problems.append("unit incompatible with quantity")
    for key in ("value", "uncertainty"):
        v = record.get(key)
        if isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v):
            problems.append(f"{key} must be finite numeric")
    value, uncertainty = record.get("value"), record.get("uncertainty")
    if isinstance(uncertainty, (int, float)) and not isinstance(uncertainty, bool) and math.isfinite(uncertainty) and uncertainty < 0:
        problems.append("uncertainty must be nonnegative")
    if definition and isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value):
        if definition["positive"] and value <= 0:
            problems.append("quantity requires positive value")
        elif quantity == "optical_power" and value < 0:
            problems.append("optical power cannot be negative")
    if record.get("uncertainty_type") not in ("standard", "expanded"):
        problems.append("uncertainty_type must be standard or expanded")
    for key in ("measurement_id", "instrument_id", "calibration_reference", "sample_id",
                "source_id", "method", "equation_id"):
        if not isinstance(record.get(key), str) or not record.get(key, "").strip():
            problems.append(f"{key} must be a nonempty string")
    if not isinstance(record.get("conditions"), dict) or not record.get("conditions"):
        problems.append("conditions must be a nonempty mapping")
    if record.get("uncertainty_type") == "expanded":
        factor = record.get("coverage_factor")
        if isinstance(factor, bool) or not isinstance(factor, (int, float)) or not math.isfinite(factor) or factor <= 0:
            problems.append("expanded uncertainty requires positive coverage_factor")
    accepted = not problems
    normalized = None
    if accepted:
        normalized = {"value_si": value * definition["units"][unit],
                      "uncertainty_si": uncertainty * definition["units"][unit],
                      "dimension": definition["dimension"],
                      "si_unit": {"length": "m", "inverse_time": "Hz", "power": "W",
                                  "time": "s", "temperature": "K"}[definition["dimension"]]}
    return {
        "gate": "MEASUREMENT_INTAKE", "status": "RECORD_ACCEPTED_FOR_REVIEW" if accepted else "REJECTED",
        "problems": problems, "normalized": normalized,
        "g3_evidence_types": [], "claims_authorized": [],
        "caveats": [
            "Record acceptance is not measurement authentication or equation validation.",
            "Equation ID is a traceability label only; equation applicability must be reviewed.",
            "Calibration reference is a declaration; its authenticity has not been checked.",
            "No optical gain, stimulated emission, or laser threshold claim is inferred.",
        ],
    }

def main():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--record", required=True)
    p.add_argument("--out", required=True)
    args = p.parse_args()
    result = validate(json.loads(Path(args.record).read_text(encoding="utf-8")))
    target = Path(args.out)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(result, indent=2, allow_nan=False), encoding="utf-8")
    print(json.dumps(result, indent=2, allow_nan=False))
    raise SystemExit(0 if result["status"] == "RECORD_ACCEPTED_FOR_REVIEW" else 1)

if __name__ == "__main__":
    main()
