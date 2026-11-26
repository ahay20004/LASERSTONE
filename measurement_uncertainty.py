"""First-order standard uncertainty for explicitly independent inputs."""
from math import isfinite, hypot
from numbers import Real

def _finite(value):
    if isinstance(value, bool) or not isinstance(value, Real) or not isfinite(value):
        raise ValueError("Expected finite real number")
    return float(value)

def propagate_independent(sensitivities, uncertainties, *, independent):
    if independent is not True:
        raise ValueError("Independence must be explicitly established")
    if not isinstance(sensitivities, dict) or not isinstance(uncertainties, dict):
        raise ValueError("Expected mappings")
    if not sensitivities or set(sensitivities) != set(uncertainties):
        raise ValueError("Every sensitivity requires a standard uncertainty")
    contributions = {}
    for key, sensitivity in sensitivities.items():
        s = _finite(sensitivity)
        u = _finite(uncertainties[key])
        if u < 0:
            raise ValueError("Standard uncertainty cannot be negative")
        contributions[key] = _finite(s * u)
    combined = _finite(hypot(*contributions.values()))
    return {"standard_uncertainty": combined,
            "signed_contributions": contributions,
            "method": "first_order_independent",
            "scientific_validation": False}


def propagate_correlated(sensitivities, uncertainties, correlation):
    """Explicit full correlation matrix; validate positive semidefiniteness."""
    from math import sqrt, fsum
    base = propagate_independent(sensitivities, uncertainties, independent=True)
    keys = list(sensitivities)
    if not isinstance(correlation, dict) or set(correlation) != set(keys):
        raise ValueError("Full correlation matrix required")
    for k in keys:
        if not isinstance(correlation[k], dict) or set(correlation[k]) != set(keys):
            raise ValueError("Full correlation row required")
    a = [[_finite(correlation[k][j]) for j in keys] for k in keys]
    n = len(keys)
    for i in range(n):
        if a[i][i] != 1:
            raise ValueError("Correlation diagonal must be one")
        for j in range(n):
            if abs(a[i][j]) > 1 or a[i][j] != a[j][i]:
                raise ValueError("Correlation must be symmetric and bounded")
    # Semidefinite Cholesky with explicit numerical tolerance.
    tol = 1e-12
    l = [[0.0]*n for _ in keys]
    for i in range(n):
        for j in range(i+1):
            residual = a[i][j] - fsum(l[i][k]*l[j][k] for k in range(j))
            if i == j:
                if residual < -tol:
                    raise ValueError("Correlation matrix is not positive semidefinite")
                l[i][j] = sqrt(max(0.0, residual))
            elif l[j][j] > 0:
                l[i][j] = residual/l[j][j]
            elif abs(residual) > tol:
                raise ValueError("Correlation matrix is not positive semidefinite")
    v = [base["signed_contributions"][k] for k in keys]
    combined = _finite(hypot(*(fsum(l[i][j]*v[i] for i in range(j,n))
                               for j in range(n))))
    return {"standard_uncertainty": combined,
            "signed_contributions": base["signed_contributions"],
            "method": "first_order_correlated",
            "correlation_psd_tolerance": tol,
            "scientific_validation": False}
