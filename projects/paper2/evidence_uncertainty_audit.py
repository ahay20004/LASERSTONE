"""Stage 3.7: uncertainty-aware evidence comparison for theory predictions.

Records are researcher-supplied and not authenticated. This module only
computes a transparent residual and combined *independent* standard
uncertainty; it never treats numerical compatibility as physical validation.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path


def _finite(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x)


def compare(record):
    required = {"observable", "unit", "prediction", "prediction_standard_uncertainty",
                "measurement", "measurement_standard_uncertainty",
                "source_id", "instrument_id", "calibration_id", "conditions_id"}
    if not isinstance(record, dict) or set(record) != required:
        raise ValueError("Evidence record requires exactly the declared comparison fields")
    for key in ("observable", "unit", "source_id", "instrument_id",
                "calibration_id", "conditions_id"):
        if not isinstance(record[key], str) or not record[key].strip():
            raise ValueError(key + " must be a nonempty string")
    for key in ("prediction", "prediction_standard_uncertainty",
                "measurement", "measurement_standard_uncertainty"):
        if not _finite(record[key]):
            raise ValueError(key + " must be finite")
    up, um = record["prediction_standard_uncertainty"], record["measurement_standard_uncertainty"]
    if up < 0 or um < 0:
        raise ValueError("Standard uncertainties must be nonnegative")
    combined = math.hypot(up, um)
    residual = record["prediction"] - record["measurement"]
    if not math.isfinite(residual) or not math.isfinite(combined):
        raise ValueError("Numerical overflow")
    normalized = abs(residual) / combined if combined > 0 else None
    if normalized is not None and not math.isfinite(normalized):
        raise ValueError("Normalized residual overflow")
    status = "UNCERTAINTY_NOT_RESOLVED" if combined == 0 else "COMPARISON_RECORDED"
    return {
        "status": status, "observable": record["observable"], "unit": record["unit"],
        "residual": residual, "combined_standard_uncertainty": combined,
        "absolute_normalized_residual": normalized,
        "source_id": record["source_id"], "instrument_id": record["instrument_id"],
        "calibration_id": record["calibration_id"], "conditions_id": record["conditions_id"],
        "evidence_authentication": "NOT_VERIFIED", "claims_authorized": [],
        "caveats": [
            "Combined uncertainty assumes independent prediction and measurement errors.",
            "Uncertainty type, calibration, covariance, units and provenance are self-declared, not verified.",
            "Normalized residual is descriptive only; no acceptance threshold or statistical significance is inferred.",
        ],
    }


def bind_report(unified_report, evidence_records):
    if not isinstance(unified_report, dict) or not all(
        isinstance(unified_report.get(k), str) and unified_report[k]
        for k in ("theory_id", "version", "proposal_sha256", "audit_sha256")
    ):
        raise ValueError("Valid version-bound unified audit report required")
    if not isinstance(evidence_records, list) or not evidence_records:
        raise ValueError("At least one evidence comparison required")
    comparisons = [compare(record) for record in evidence_records]
    fingerprint = hashlib.sha256(json.dumps(evidence_records, sort_keys=True,
                              ensure_ascii=False, allow_nan=False).encode("utf-8")).hexdigest()
    return {
        "theory_id": unified_report["theory_id"],
        "version": unified_report["version"],
        "proposal_sha256": unified_report["proposal_sha256"],
        "upstream_audit_sha256": unified_report["audit_sha256"],
        "evidence_input_sha256": fingerprint,
        "comparisons": comparisons, "stage": "PROPOSED",
        "endorsement": "NONE", "claims_authorized": [],
        "caveat": "Self-declared evidence comparisons do not independently validate the theory.",
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--unified-report", required=True)
    p.add_argument("--evidence", required=True)
    p.add_argument("--out", required=True)
    args = p.parse_args()
    report = bind_report(json.loads(Path(args.unified_report).read_text(encoding="utf-8")),
                         json.loads(Path(args.evidence).read_text(encoding="utf-8")))
    dest = Path(args.out)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
