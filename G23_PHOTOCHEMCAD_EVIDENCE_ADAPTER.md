# G23 PhotochemCAD Evidence Adapter Specification

## Purpose

Provide LASERSTONE with a read-only normalization layer for externally sourced
PhotochemCAD records while preserving provenance and separating reported,
derived, and missing scientific values.

## Stage boundary

This stage is intentionally isolated.

- No changes to `main.py`.
- No changes to production scientific results.
- No automatic web scraping or runtime network access.
- No insertion into `plants_data.py`.
- No production registry wiring yet.
- No default values are created for missing scientific quantities.

The adapter accepts already verified source records and returns a normalized
evidence object.

## Evidence states

- `LITERATURE_REPORTED`: value is explicitly present in the source record.
- `DERIVED`: value is calculated from a reported quantity using a stated
  equation.
- `MISSING`: source does not provide the quantity used by this adapter.

A missing value remains `None`; it must not be converted to zero or to a
typical/estimated value.

## Normalized fields

The current schema supports:

- source_database
- photochemcad_id
- compound_name
- compound_class
- plant_origin
- lambda_abs_nm
- lambda_em_nm
- epsilon_M_cm
- phi_f
- sigma_a_cm2
- solvent
- temperature_K
- instrument
- reference
- doi
- spectrum_abs_source
- spectrum_em_source
- source_url
- evidence_type
- field_evidence
- derivation_method
- missing_fields

## Derived absorption cross section

When the molar extinction coefficient epsilon is explicitly available in
M^-1 cm^-1, the adapter derives the molecular absorption cross section as:

```
sigma_a_cm2 = 1000 * ln(10) * epsilon_M_cm / N_A
```

with `N_A = 6.02214076e23 mol^-1`.

The derived value is marked `DERIVED`; epsilon itself remains
`LITERATURE_REPORTED`.

## Acceptance records

The initial acceptance test uses three records chosen to exercise different
evidence completeness states.

### BX003 — Asn-Bx

Source:
https://www.photochemcad.com/databases/betaxanthins/asn-bx

Verified fields used in the test:
- lambda_abs_nm = 476
- epsilon_M_cm = 56200
- phi_f = 0.0074
- solvent = Water

Expected behavior:
- preserve reported values;
- derive sigma_a_cm2;
- do not create lambda_em_nm.

### FL109 — Quercetin

Source:
https://www.photochemcad.com/databases/flavonoids/quercetin

Verified fields used in the test:
- lambda_abs_nm = 256
- epsilon_M_cm = 18700
- solvent = MeOH

Expected behavior:
- derive sigma_a_cm2;
- leave phi_f and lambda_em_nm missing.

### CAR021a-6 — Lutein [HPLC]

Source:
https://photochemcad.com/databases/carotenoids/lutein-hplc

Verified fields used in the test:
- lambda_abs_nm = 444.5
- solvent = HPLC condition 8 [MeOH/MTBE (97:3)]

Expected behavior:
- leave epsilon_M_cm and sigma_a_cm2 missing;
- do not infer fluorescence data.

## Acceptance gates

The adapter is accepted for this isolated stage only when all of the following
are true:

1. Source mappings are not mutated.
2. Reported values are preserved numerically.
3. Missing values remain missing.
4. sigma_a_cm2 is derived only when epsilon is present.
5. The derivation formula is explicitly recorded.
6. Nonphysical wavelengths are rejected.
7. Quantum yield outside [0, 1] is rejected.

Run:

```
python -m unittest -v test_g23_photochemcad_evidence_adapter.py
```

## Future integration gate

Production integration must be a separate reviewed step. Before wiring this
adapter to `spectral_quality_engine.py`, LASERSTONE must define:

- unit compatibility for legacy `sigma_a`;
- mapping rules for `phi_f` versus legacy `phi`;
- behavior when tau, knr, eta, or refractive_index are absent;
- provenance propagation through downstream ranking engines;
- explicit prevention of missing scientific values being replaced by zero.

Until those points are resolved, this adapter remains evidence-only and must
not be interpreted as proof of laser gain, lasing feasibility, or prototype
readiness.
