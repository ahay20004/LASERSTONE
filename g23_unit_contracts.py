"""Unit and semantic contracts for G23 evidence integration.

Contracts are explicit about unresolved legacy quantities. A mapping is allowed
only when both semantics and units are sufficiently defined.
"""

from __future__ import annotations

from copy import deepcopy

RESOLVED = "RESOLVED"
UNRESOLVED = "UNRESOLVED"
DERIVED = "DERIVED"

UNIT_CONTRACTS = {
    "phi_f": {
        "semantic": "fluorescence quantum yield",
        "unit": "1",
        "status": RESOLVED,
        "source_family": "PhotochemCAD",
    },
    "epsilon_M_cm": {
        "semantic": "molar extinction coefficient",
        "unit": "M^-1 cm^-1",
        "status": RESOLVED,
        "source_family": "PhotochemCAD",
    },
    "sigma_a_cm2": {
        "semantic": "molecular absorption cross section",
        "unit": "cm^2 molecule^-1",
        "status": DERIVED,
        "source_family": "PhotochemCAD",
    },
    "lambda_abs_nm": {
        "semantic": "absorption wavelength",
        "unit": "nm",
        "status": RESOLVED,
        "source_family": "PhotochemCAD",
    },
    "lambda_em_nm": {
        "semantic": "emission wavelength",
        "unit": "nm",
        "status": RESOLVED,
        "source_family": "PhotochemCAD",
    },
    "phi": {
        "semantic": "quantum yield",
        "unit": "1",
        "status": RESOLVED,
        "source_family": "LASERSTONE_LEGACY",
    },
    "lambda_abs": {
        "semantic": "absorption wavelength",
        "unit": "nm",
        "status": RESOLVED,
        "source_family": "LASERSTONE_LEGACY",
    },
    "lambda_em": {
        "semantic": "emission wavelength",
        "unit": "nm",
        "status": RESOLVED,
        "source_family": "LASERSTONE_LEGACY",
    },
    "refractive_index": {
        "semantic": "refractive index",
        "unit": "1",
        "status": RESOLVED,
        "source_family": "LASERSTONE_LEGACY",
    },
    "tau": {
        "semantic": "fluorescence lifetime",
        "unit": "UNRESOLVED_LEGACY_UNIT",
        "status": UNRESOLVED,
        "source_family": "LASERSTONE_LEGACY",
    },
    "sigma_a": {
        "semantic": "legacy absorption quantity labelled cross section",
        "unit": "UNRESOLVED_LEGACY_UNIT_OR_NORMALIZATION",
        "status": UNRESOLVED,
        "source_family": "LASERSTONE_LEGACY",
    },
    "eta": {
        "semantic": "legacy optical efficiency quantity",
        "unit": "UNRESOLVED_LEGACY_DEFINITION",
        "status": UNRESOLVED,
        "source_family": "LASERSTONE_LEGACY",
    },
    "knr": {
        "semantic": "legacy non-radiative decay quantity",
        "unit": "UNRESOLVED_LEGACY_UNIT_OR_NORMALIZATION",
        "status": UNRESOLVED,
        "source_family": "LASERSTONE_LEGACY",
    },
}

SAFE_MAPPINGS = {
    ("phi_f", "phi"),
    ("lambda_abs_nm", "lambda_abs"),
    ("lambda_em_nm", "lambda_em"),
}


def get_unit_contract(field: str) -> dict:
    if field not in UNIT_CONTRACTS:
        raise KeyError(f"No unit contract for {field}")
    return deepcopy(UNIT_CONTRACTS[field])


def mapping_assessment(source_field: str, target_field: str) -> dict:
    source = get_unit_contract(source_field)
    target = get_unit_contract(target_field)

    allowed = (source_field, target_field) in SAFE_MAPPINGS
    reason = "SAFE_EXPLICIT_MAPPING" if allowed else "MAPPING_NOT_AUTHORIZED"

    if source_field == "sigma_a_cm2" and target_field == "sigma_a":
        allowed = False
        reason = (
            "BLOCKED_UNIT_MISMATCH: physical cm^2 molecule^-1 cannot be "
            "mapped to unresolved legacy sigma_a"
        )

    return {
        "source_field": source_field,
        "target_field": target_field,
        "source_contract": source,
        "target_contract": target,
        "allowed": allowed,
        "reason": reason,
    }


def unresolved_legacy_contracts() -> list[str]:
    return sorted(
        field
        for field, contract in UNIT_CONTRACTS.items()
        if contract["source_family"] == "LASERSTONE_LEGACY"
        and contract["status"] == UNRESOLVED
    )
