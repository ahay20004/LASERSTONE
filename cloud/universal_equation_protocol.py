"""Generic, fail-closed equation contract validation for LASERSTONE.

A schema/relationship gate, not a claim of physics-engine integration.
Units are exact canonical strings: conversions require an explicit adapter.
"""
from dataclasses import dataclass
from math import isfinite
from typing import Callable

from cloud.equation_contract import Quantity

EVIDENCE = frozenset(("MEASURED", "DERIVED", "SIMULATED", "PREDICTED"))


@dataclass(frozen=True)
class VariableSpec:
    name: str
    unit: str
    minimum: float | None = None
    maximum: float | None = None
    required_evidence: tuple[str, ...] = ("MEASURED", "DERIVED", "SIMULATED", "PREDICTED")


@dataclass(frozen=True)
class EquationSpec:
    equation_id: str
    variables: tuple[VariableSpec, ...]
    assumptions: tuple[str, ...]
    relation_checks: tuple[Callable[[dict[str, Quantity]], bool], ...] = ()


def validate_equation_inputs(
    spec: EquationSpec, values: dict[str, Quantity]
) -> dict[str, Quantity]:
    """Validate a complete immutable snapshot before any equation executes."""
    if not spec.equation_id.strip() or not spec.variables or not spec.assumptions:
        raise ValueError("incomplete equation specification")
    names = [variable.name for variable in spec.variables]
    if any(not name.strip() for name in names) or len(names) != len(set(names)):
        raise ValueError("duplicate or blank variable name")
    if set(values) != set(names):
        raise ValueError("missing or unexpected equation inputs")
    snapshot = dict(values)
    for variable in spec.variables:
        value = snapshot[variable.name]
        if not isinstance(value, Quantity):
            raise ValueError(f"{variable.name}: Quantity required")
        if not variable.unit.strip() or value.unit != variable.unit:
            raise ValueError(f"{variable.name}: unit mismatch; explicit conversion required")
        if not isfinite(value.value) or not value.source.strip():
            raise ValueError(f"{variable.name}: invalid number or provenance")
        if not variable.required_evidence or any(
            state not in EVIDENCE for state in variable.required_evidence
        ):
            raise ValueError(f"{variable.name}: invalid evidence policy")
        if value.evidence_state not in variable.required_evidence:
            raise ValueError(f"{variable.name}: evidence state not permitted")
        if variable.minimum is not None and value.value < variable.minimum:
            raise ValueError(f"{variable.name}: below minimum")
        if variable.maximum is not None and value.value > variable.maximum:
            raise ValueError(f"{variable.name}: above maximum")
        if (variable.minimum is not None and not isfinite(variable.minimum)) or (
            variable.maximum is not None and not isfinite(variable.maximum)
        ):
            raise ValueError(f"{variable.name}: invalid bounds")
        if (variable.minimum is not None and variable.maximum is not None
                and variable.minimum > variable.maximum):
            raise ValueError(f"{variable.name}: inverted bounds")
    for check in spec.relation_checks:
        try:
            passed = check(dict(snapshot))
        except Exception as exc:
            raise ValueError("equation relation check failed") from exc
        if passed is not True:
            raise ValueError("equation variable relationship violated")
    return snapshot
