"""Strict missing-data policy for LASERSTONE G23.

The policy distinguishes absence from a measured numeric zero. It provides
fail-closed helpers for evidence-aware modules and must not mutate source data.
"""

from __future__ import annotations

import math
from typing import Any, Mapping, Sequence


class MissingScientificDataError(ValueError):
    """Raised when a required scientific quantity is absent."""


class InvalidScientificDataError(ValueError):
    """Raised when a present scientific quantity is invalid."""


def assess_required_numeric(
    record: Mapping[str, Any],
    fields: Sequence[str],
) -> dict[str, Any]:
    """Return missing and invalid required numeric fields without coercion."""
    if not isinstance(record, Mapping):
        raise TypeError("record must be a mapping")

    missing = []
    invalid = []

    for field in fields:
        if field not in record or record.get(field) is None:
            missing.append(field)
            continue

        value = record.get(field)
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            invalid.append(field)
            continue

        if not math.isfinite(float(value)):
            invalid.append(field)

    return {
        "valid": not missing and not invalid,
        "missing": missing,
        "invalid": invalid,
        "policy": "MISSING_IS_NOT_ZERO",
    }


def require_finite_number(
    record: Mapping[str, Any],
    field: str,
    *,
    minimum: float | None = None,
    maximum: float | None = None,
) -> float:
    """Read one required finite numeric value, preserving real zero values."""
    if not isinstance(record, Mapping):
        raise TypeError("record must be a mapping")

    if field not in record or record.get(field) is None:
        raise MissingScientificDataError(f"{field} is required and is missing")

    value = record.get(field)
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise InvalidScientificDataError(f"{field} must be numeric")

    value = float(value)
    if not math.isfinite(value):
        raise InvalidScientificDataError(f"{field} must be finite")

    if minimum is not None and value < minimum:
        raise InvalidScientificDataError(
            f"{field} must be >= {minimum}"
        )

    if maximum is not None and value > maximum:
        raise InvalidScientificDataError(
            f"{field} must be <= {maximum}"
        )

    return value


def require_score(record: Mapping[str, Any], field: str) -> float:
    """Require a finite score in [0, 100], with no default substitution."""
    return require_finite_number(record, field, minimum=0.0, maximum=100.0)


def strict_weighted_sum(
    record: Mapping[str, Any],
    weights: Mapping[str, float],
) -> float:
    """Calculate a weighted sum only when every required input is present."""
    if not isinstance(weights, Mapping) or not weights:
        raise ValueError("weights must be a nonempty mapping")

    total = 0.0
    for field, weight in weights.items():
        if isinstance(weight, bool) or not isinstance(weight, (int, float)):
            raise TypeError(f"weight for {field} must be numeric")
        weight = float(weight)
        if not math.isfinite(weight):
            raise ValueError(f"weight for {field} must be finite")
        total += require_finite_number(record, field) * weight

    return total


def strict_mean(record: Mapping[str, Any], fields: Sequence[str]) -> float:
    """Calculate a mean only when all requested values are present."""
    fields = list(fields)
    if not fields:
        raise ValueError("fields must not be empty")

    values = [require_finite_number(record, field) for field in fields]
    return sum(values) / len(values)
