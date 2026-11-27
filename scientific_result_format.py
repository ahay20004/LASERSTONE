"""Display-only rounding; preserve original decimal values."""
from decimal import Decimal, InvalidOperation, localcontext, ROUND_HALF_EVEN

def _decimal(value):
    if isinstance(value, bool):
        raise ValueError("Boolean is not a measurement")
    try:
        d = Decimal(str(value))
    except (InvalidOperation, ValueError, TypeError) as exc:
        raise ValueError("Invalid measurement") from exc
    if not d.is_finite():
        raise ValueError("Nonfinite measurement")
    return d

def format_result(value, uncertainty, unit, *, digits=2):
    v = _decimal(value)
    if not isinstance(unit, str) or not unit.strip():
        raise ValueError("Explicit unit required")
    if type(digits) is not int or not 1 <= digits <= 3:
        raise ValueError("Uncertainty digits must be 1 to 3")
    result = {"raw_value": str(v), "unit": unit, "scientific_validation": False}
    if uncertainty is None:
        return dict(result, raw_uncertainty=None, display_value=str(v),
                    display_uncertainty=None, uncertainty_status="unknown")
    u = _decimal(uncertainty)
    if u < 0:
        raise ValueError("Negative uncertainty")
    if u == 0:
        return dict(result, raw_uncertainty=str(u), display_value=str(v),
                    display_uncertainty="0", uncertainty_status="reported_zero")
    exponent = u.adjusted() - digits + 1
    with localcontext() as ctx:
        ctx.prec = max(34, v.adjusted()-exponent+5, len(v.as_tuple().digits)+5)
        q = Decimal(1).scaleb(exponent)
        rounded_u = u.quantize(q, rounding=ROUND_HALF_EVEN)
        if rounded_u.adjusted() > u.adjusted():
            q = Decimal(1).scaleb(exponent+1)
            rounded_u = u.quantize(q, rounding=ROUND_HALF_EVEN)
        rounded_v = v.quantize(q, rounding=ROUND_HALF_EVEN)
    return dict(result, raw_uncertainty=str(u), display_value=str(rounded_v),
                display_uncertainty=str(rounded_u), uncertainty_status="reported",
                rounding_policy="half_even", uncertainty_significant_digits=digits)
