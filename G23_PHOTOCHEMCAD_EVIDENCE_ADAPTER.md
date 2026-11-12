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

## Integration gate findings

The legacy G23 scientific input gate explicitly defines `phi` as quantum
yield, so a reported PhotochemCAD fluorescence quantum yield `phi_f` may be
mapped to legacy `phi` with provenance.

The legacy `sigma_a` field does not currently have a documented physical
unit or normalization contract. Existing project values are numerically of
order unity, while a physically derived molecular absorption cross section
from PhotochemCAD is typically of order 1e-16 cm^2 molecule^-1. Therefore
`sigma_a_cm2` must not be copied into legacy `sigma_a`.

The integration gate in `photochemcad_integration_gate.py` therefore permits
only the following evidence-preserving mappings:

- `phi_f -> phi`, when `phi_f` is explicitly reported;
- `lambda_abs_nm -> lambda_abs`, when explicitly reported;
- `lambda_em_nm -> lambda_em`, when explicitly reported.

Derived `sigma_a_cm2` remains a separate unit-bearing physical evidence
field.

Legacy scientific execution remains blocked whenever any required legacy
quantity is unresolved. In particular, PhotochemCAD records must not receive
fabricated values for `tau`, `sigma_a`, `eta`, `knr`,
`refractive_index`, or `lambda_em`.

Run:

```
python -m unittest -v test_g23_photochemcad_integration_gate.py
```

The isolated integration-gate logic has eight acceptance cases covering safe
mapping, sigma separation, missing-data preservation, non-promotion, source
immutability, source validation, and conditional emission-wavelength mapping.

## Production integration status

**BLOCKED FROM LEGACY SCIENTIFIC EXECUTION.**

This is a scientific safeguard, not a software failure. The PhotochemCAD
evidence layer is usable now for traceable evidence storage and analysis, but
it must not be fed into the legacy scoring pipeline until:

- the legacy `sigma_a` unit/normalization contract is defined;
- missing-field behavior is changed so absence is not silently converted to
  zero;
- downstream provenance is preserved through ranking and decision engines;
- any additional photophysical quantities are supplied from traceable sources
  rather than inferred merely to satisfy a score formula.

Until those conditions are met, PhotochemCAD evidence must not be interpreted
as proof of laser gain, lasing feasibility, or prototype readiness.


## Physical spectral evidence path

The branch now includes `physical_spectral_evidence_engine.py`, an
evidence-first analysis path that is intentionally separate from legacy
spectral quality scoring.

The engine uses four independent reported core quantities:

- `lambda_abs_nm`
- `lambda_em_nm`
- `epsilon_M_cm`
- `phi_f`

Derived `sigma_a_cm2` is not counted as an independent evidence item because
it is computed from epsilon.

The evidence completeness metric is therefore:

```
evidence_completeness = 100 * reported_core_fields / 4
```

This is a data-coverage metric only. It is not a laser-performance score.

For the three initial PhotochemCAD records:

| Record | Independent reported core fields | Evidence completeness |
| --- | ---: | ---: |
| BX003 Asn-Bx | 3/4 | 75% |
| FL109 Quercetin | 2/4 | 50% |
| CAR021a-6 Lutein [HPLC] | 1/4 | 25% |

When both absorption and emission peaks are explicitly reported, the engine may
also derive Stokes shift as:

```
Delta_lambda = lambda_em - lambda_abs
Delta_wavenumber = 1e7 * (1/lambda_abs - 1/lambda_em)
```

with wavelengths in nm and the wavenumber shift in cm^-1.

No gain, lasing feasibility, or prototype-readiness claim is produced by this
engine.

Run:

```
python -m unittest -v test_g23_physical_spectral_evidence_engine.py
```

## Legacy versus physical path diagnostic

The branch also includes `spectral_path_comparison.py`.

Its purpose is diagnostic only. It does not convert physical evidence
completeness into legacy spectral quality and does not rank the two outputs
against each other.

For all three initial PhotochemCAD cases:

- the physical evidence path is available;
- the legacy spectral-quality path is blocked by missing or scientifically
  unsafe fields;
- legacy `sigma_a` remains unresolved because its unit contract is not
  documented;
- missing values are not replaced by zero.

The comparison status is explicitly:

`NON_EQUIVALENT_OUTPUTS_DO_NOT_RANK_AGAINST_EACH_OTHER`.

Run:

```
python -m unittest -v test_g23_spectral_path_comparison.py
```
