"""Stage 3.2: explicit SI-base dimensional consistency checker.

A declared algebraic equation is represented as sums of multiplicative terms.
Dimensions are checked, not inferred from symbol names; this is not a general
symbolic algebra engine, derivation checker or scientific endorsement.
"""
from collections import Counter
import json
from pathlib import Path

BASE = ("M", "L", "T", "I", "Theta", "N", "J")

def _dimension(value):
    if not isinstance(value, dict) or set(value) - set(BASE):
        raise ValueError("Dimensions must be a map of SI base dimension exponents")
    if any(isinstance(v, bool) or not isinstance(v, int) for v in value.values()):
        raise ValueError("Dimension exponents must be integers")
    return tuple(value.get(key, 0) for key in BASE)

def _term_dimension(term, symbols):
    if not isinstance(term, dict) or not term:
        raise ValueError("Each term must be a nonempty symbol-to-integer-power mapping")
    total = [0] * len(BASE)
    for symbol, power in term.items():
        if symbol not in symbols:
            raise ValueError("Unknown symbol: " + str(symbol))
        if isinstance(power, bool) or not isinstance(power, int):
            raise ValueError("Term powers must be integers")
        dims = _dimension(symbols[symbol])
        for i, exponent in enumerate(dims):
            total[i] += exponent * power
    return tuple(total)

def assess(specification):
    if not isinstance(specification, dict) or set(specification) != {"symbols", "lhs_terms", "rhs_terms"}:
        raise ValueError("Expected symbols, lhs_terms and rhs_terms")
    symbols = specification["symbols"]
    if not isinstance(symbols, dict) or not symbols:
        raise ValueError("Symbols must be a nonempty mapping")
    lhs, rhs = specification["lhs_terms"], specification["rhs_terms"]
    if not isinstance(lhs, list) or not lhs or not isinstance(rhs, list) or not rhs:
        raise ValueError("Both sides require at least one term")
    left = [_term_dimension(term, symbols) for term in lhs]
    right = [_term_dimension(term, symbols) for term in rhs]
    all_dims = left + right
    consistent = len(set(all_dims)) == 1
    return {
        "status": "DIMENSIONALLY_CONSISTENT" if consistent else "DIMENSIONAL_MISMATCH",
        "lhs_term_dimensions": [dict(zip(BASE, x)) for x in left],
        "rhs_term_dimensions": [dict(zip(BASE, x)) for x in right],
        "claims_authorized": [],
        "caveats": [
            "Only declared dimensions and multiplicative monomials are assessed.",
            "Dimensionless functions, coefficients, fractional powers and physical validity are not checked.",
            "Dimensional consistency is necessary in many models but does not prove the equation.",
        ],
    }

def main():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--spec", required=True)
    p.add_argument("--out", required=True)
    args = p.parse_args()
    result = assess(json.loads(Path(args.spec).read_text(encoding="utf-8")))
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["status"] == "DIMENSIONALLY_CONSISTENT" else 1)

if __name__ == "__main__":
    main()
