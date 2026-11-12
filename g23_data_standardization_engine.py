"""Strict data standardization for LASERSTONE G23.

Unlike the legacy standardizer, missing/unknown values are not converted to
numeric zero. The function returns value plus an explicit evidence state.
"""

from __future__ import annotations

import math
from copy import deepcopy
from typing import Any, Mapping

QUALITY_MAP = {
    "high": 100.0,
    "medium": 60.0,
    "low": 30.0,
    "excellent": 100.0,
    "very good": 85.0,
    "good": 75.0,
    "moderate": 60.0,
    "fair": 50.0,
    "poor": 20.0,
}

MISSING_TOKENS = {"", "unknown", "n/a", "na", "none", "missing"}


def standardize_quality_value_strict(value: Any) -> dict[str, Any]:
    if value is None:
        return {"value": None, "status": "MISSING"}

    if isinstance(value, bool):
        return {"value": None, "status": "INVALID"}

    if isinstance(value, (int, float)):
        numeric = float(value)
        if not math.isfinite(numeric) or not 0.0 <= numeric <= 100.0:
            return {"value": None, "status": "INVALID"}
        return {"value": numeric, "status": "NUMERIC_REPORTED"}

    text = str(value).strip().lower()
    if text in MISSING_TOKENS:
        return {"value": None, "status": "MISSING"}

    if text in QUALITY_MAP:
        return {
            "value": QUALITY_MAP[text],
            "status": "CATEGORY_MAPPED",
            "source_category": text,
        }

    return {"value": None, "status": "UNRECOGNIZED"}


def classify_numeric_score_strict(value: Any) -> str:
    result = standardize_quality_value_strict(value)
    score = result["value"]
    if score is None:
        return "UNAVAILABLE"
    if score >= 85:
        return "Excellent"
    if score >= 70:
        return "Very Good"
    if score >= 55:
        return "Moderate"
    if score >= 35:
        return "Low"
    return "Very Low"


def standardize_field_strict(
    record: Mapping[str, Any],
    source_key: str,
    target_score_key: str,
    target_class_key: str,
) -> dict[str, Any]:
    """Return a detached standardized record with explicit state metadata."""
    if not isinstance(record, Mapping):
        raise TypeError("record must be a mapping")

    output = deepcopy(dict(record))
    result = standardize_quality_value_strict(record.get(source_key))

    output[target_score_key] = result["value"]
    output[target_class_key] = classify_numeric_score_strict(result["value"])
    output[f"{target_score_key}_status"] = result["status"]

    return output
