REQUIRED_FIELDS = [

    "name",
    "scientific_name",
    "origin",

    "phi",
    "tau",
    "sigma_a",
    "eta",
    "knr",
    "refractive_index",

    "lambda_abs",
    "lambda_em"
]


def validate_plant_data(plant):

    missing_fields = []

    for field in REQUIRED_FIELDS:

        if field not in plant:

            missing_fields.append(field)

    if missing_fields:

        return {
            "valid": False,
            "missing": missing_fields
        }

    return {
        "valid": True,
        "missing": []
    }


# Canonical units for the current cavity and fluorescence models.
PHYSICAL_PARAMETER_RULES = {
    "lambda_em": ("nm", 0, None, True),
    "refractive_index": ("1", 0, None, True),
    "group_index": ("1", 0, None, True),
    "cavity_length_m": ("m", 0, None, True),
    "mirror_r1": ("1", 0, 1, True),
    "mirror_r2": ("1", 0, 1, True),
    "internal_loss_m_inv": ("m^-1", 0, None, False),
    "gain_m_inv": ("m^-1", None, None, False),
    "quantum_yield": ("1", 0, 1, False),
    "lifetime_s": ("s", 0, None, True),
    "resonance_frequency_hz": ("Hz", 0, None, True),
    "linewidth_hz": ("Hz", 0, None, True),
    "energy_lifetime_s": ("s", 0, None, True),
}


def audit_parameter_record(name, record):
    """Check declared metadata and physical domain, not source authenticity."""
    import math
    if name not in PHYSICAL_PARAMETER_RULES or not isinstance(record, dict):
        return {"status": "INVALID"}
    unit, lower, upper, strict = PHYSICAL_PARAMETER_RULES[name]
    value = record.get("value")
    u = record.get("standard_uncertainty")
    for x in (value, u):
        if x is not None and (isinstance(x, bool) or not isinstance(x, (int, float))
                              or not math.isfinite(x)):
            return {"status": "INVALID"}
    if value is not None and ((lower is not None and
            (value < lower or (strict and value == lower))) or
            (upper is not None and value > upper)):
        return {"status": "INVALID"}
    if u is not None and u < 0:
        return {"status": "INVALID"}
    if record.get("unit") is not None and record["unit"] != unit:
        return {"status": "INVALID"}
    missing = [k for k in ("value", "unit", "standard_uncertainty", "source_id",
                           "conditions_id", "basis") if record.get(k) is None]
    for k in ("source_id", "conditions_id"):
        if k not in missing and (not isinstance(record[k], str) or not record[k].strip()):
            return {"status": "INVALID"}
    if "basis" not in missing and record["basis"] not in ("measured", "derived", "assumed", "literature"):
        return {"status": "INVALID"}
    return {"status": "UNVERIFIED" if missing else "RECORDED",
            "missing": missing, "expected_unit": unit,
            "source_authentication": "NOT_VERIFIED"}
