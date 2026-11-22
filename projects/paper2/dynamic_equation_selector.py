"""Conservative regime-aware equation selector for optical attenuation.

This is an applicability gate, not a numerical optical solver. No universal
'nanometer cutoff' is assumed and no model is automatically validated.
"""
import json
import math
from pathlib import Path

APPLICABLE = "APPLICABLE"
CONDITIONAL = "CONDITIONAL"
NOT_APPLICABLE = "NOT_APPLICABLE"

def _positive_number(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v) and v > 0

def select_optical_model(record):
    if not isinstance(record, dict):
        raise ValueError("Optical regime must be an object")
    thickness = record.get("thickness_m")
    wavelength = record.get("wavelength_m")
    if not _positive_number(thickness) or not _positive_number(wavelength):
        raise ValueError("Positive finite SI thickness_m and wavelength_m are required")
    ratio = thickness / wavelength
    homogeneous = record.get("homogeneous")
    scattering = record.get("scattering_negligible")
    interfaces = record.get("interface_reflections_accounted")
    coherent = record.get("coherent_interference_negligible")
    bulk = record.get("bulk_optical_constants_valid")
    flags = {
        "homogeneous": homogeneous,
        "scattering_negligible": scattering,
        "interface_reflections_accounted": interfaces,
        "coherent_interference_negligible": coherent,
        "bulk_optical_constants_valid": bulk,
    }
    if any(v not in (True, False, None) for v in flags.values()):
        raise ValueError("Physical assumption flags must be true, false, or null")
    contradictions = [name for name, value in flags.items() if value is False]
    unknown = [name for name, value in flags.items() if value is None]
    # Beer-Lambert for direct, single-pass attenuation; the interface and
    # coherence flags distinguish a measured transmittance from ideal bulk loss.
    if contradictions:
        status = NOT_APPLICABLE
    elif unknown:
        status = CONDITIONAL
    else:
        status = APPLICABLE
    # Thin-film transfer-matrix is only a candidate; it requires measured
    # complex optical constants, substrate and stack geometry to be usable.
    multilayer = record.get("layer_stack_characterized")
    optical_constants = record.get("complex_indices_available")
    if multilayer not in (True, False, None) or optical_constants not in (True, False, None):
        raise ValueError("Thin-film model flags must be true, false, or null")
    if multilayer is True and optical_constants is True:
        thin_status = CONDITIONAL  # no full boundary-value or solver validation
        thin_reason = "Candidate only: verify polarization, incidence angle, coherence and boundary conditions"
    else:
        thin_status = NOT_APPLICABLE if multilayer is False or optical_constants is False else CONDITIONAL
        thin_reason = "Missing or incomplete layer-stack and complex-index evidence"
    return {
        "selector": "optical_attenuation", "version": "0.1",
        "dimensionless_thickness_to_wavelength": ratio,
        "models": {
            "beer_lambert": {
                "equation": "I=I0*exp(-alpha*d)",
                "status": status,
                "failed_assumptions": contradictions,
                "unknown_assumptions": unknown,
                "scope": "Idealized homogeneous single-pass bulk attenuation",
            },
            "thin_film_transfer_matrix": {
                "status": thin_status,
                "reason": thin_reason,
                "scope": "Candidate layered optical model, not executed",
            },
        },
        "selected_for_computation": ["beer_lambert"] if status == APPLICABLE else [],
        "claims_authorized": [],
        "caveats": [
            "Thickness/wavelength ratio is descriptive; no universal nanoscale switching threshold.",
            "Boolean assumptions are declarations, not authenticated measurements.",
            "No optical constants, measured attenuation or laser-gain claim is inferred.",
            "APPLICABLE means declared applicability only; no experimental verification.",
        ],
    }

def main():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--regime", required=True)
    p.add_argument("--out", required=True)
    args = p.parse_args()
    result = select_optical_model(json.loads(Path(args.regime).read_text(encoding="utf-8")))
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, allow_nan=False), encoding="utf-8")
    print(json.dumps(result, indent=2, allow_nan=False))

if __name__ == "__main__":
    main()
