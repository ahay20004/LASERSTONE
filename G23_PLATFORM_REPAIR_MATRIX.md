# G23 Platform Repair Matrix — Evidence-Safe Parallel Development

## Objective

Maximize the scientific usefulness of PhotochemCAD and other future external
sources across LASERSTONE without weakening the existing source-of-truth,
measured/derived/predicted separation, or production stability.

This work proceeds in parallel with the legacy pipeline. No production engine
is replaced until its migration gate passes.

## Completed parallel repairs

| Area | Legacy risk | G23 repair | Current state |
| --- | --- | --- | --- |
| Missing data | None/unknown may become 0 | `g23_scientific_missing_policy.py` | Experimental verified |
| Standardization | unknown/N/A map to zero | `g23_data_standardization_engine.py` | Experimental verified |
| Unit semantics | legacy units partly undocumented | `g23_unit_contracts.py` | Experimental verified |
| External evidence | direct field mixing | `photochemcad_evidence_adapter.py` | Experimental verified |
| Legacy bridge | unsafe sigma mapping possible | `photochemcad_integration_gate.py` | Experimental verified |
| Physical spectra | heuristic quality only | `physical_spectral_evidence_engine.py` | Experimental verified |
| Engine routing | no per-engine evidence compatibility | `g23_engine_compatibility_audit.py` | Experimental verified |
| Evidence storage | no isolated source registry | `g23_evidence_registry.py` | Experimental verified |
| Decisions | external spectra could be over-promoted | `g23_evidence_decision_gate.py` | Experimental verified |
| Interpretation | wording may exceed evidence | `g23_evidence_interpretation_engine.py` | Experimental verified |
| Trace | missing values may be displayed as scores | `g23_evidence_trace_engine.py` | Experimental verified |
| Output | heuristic power/class may look physical | `g23_evidence_output_engine.py` | Experimental verified |
| Legacy decisions | get(...,0) in decision path | `g23_strict_decision_path.py` | Experimental verified |
| Component governance | experimental code could look production-ready | `g23_component_registry.py` | Experimental verified |
| Legacy provenance | generic references not tied to fields | `g23_legacy_provenance_audit.py` | Experimental verified |
| Plant/compound linkage | isolated compound could overwrite extract data | `g23_compound_evidence_linker.py` | Experimental verified |
| External orchestration | evidence modules could remain fragmented | `g23_external_evidence_pipeline.py` | Experimental verified |
| Regression | no dedicated evidence CI | G23 evidence workflow + local runner | PASS: 74/74 tests on Python 3.12 |

## Current scientific field contracts

### Resolved for safe evidence mapping

- `phi_f -> phi`: dimensionless fluorescence quantum yield.
- `lambda_abs_nm -> lambda_abs`: nm.
- `lambda_em_nm -> lambda_em`: nm.
- `epsilon_M_cm`: M^-1 cm^-1.
- `sigma_a_cm2`: derived molecular absorption cross section in
  cm^2 molecule^-1.
- refractive index: dimensionless when independently sourced.

### Still unresolved in the legacy model

- `tau`: numerical values exist, but the authoritative legacy unit contract
  must be documented.
- `sigma_a`: numerical values of order unity exist, but unit/normalization is
  not documented and is incompatible with direct PhotochemCAD cross sections.
- `eta`: physical definition and normalization require authoritative
  documentation.
- `knr`: physical unit/normalization require authoritative documentation.

No G23 adapter may fabricate these fields simply to satisfy a formula.

## Engine compatibility policy

### Evidence-safe now

These components can operate directly on normalized PhotochemCAD evidence:

- PhotochemCAD evidence adapter
- physical spectral evidence engine
- evidence interpretation engine
- evidence trace engine
- evidence output engine
- evidence decision gate
- evidence registry
- compatibility audit

Conditional legacy utilities may be used only when their exact reported inputs
exist:

- `spectral_analysis`: requires both absorption and emission wavelengths.
- `spectral_region`: requires emission wavelength.
- `color_predictor`: requires emission wavelength.

### Blocked from PhotochemCAD-only promotion

Until missing inputs and unit contracts are resolved, PhotochemCAD-only
records must not directly feed:

- spectral quality scoring
- LSI
- gain scoring
- thermal score
- photobleaching score
- operation mode
- Q-factor score
- beam-quality score
- laser-efficiency score
- material score
- LRI/readiness
- scientific confidence as physical confidence
- final prototype decision
- governor prototype decision
- predicted laser power or safety class

## Important legacy-model findings

The audit identified several patterns that are acceptable only as legacy
heuristics and must not be mistaken for physical evidence:

1. Some score engines award positive baseline points even in low-performance
   branches.
2. Several decision modules use `get(field, 0)`, conflating absent evidence
   with a real zero.
3. The legacy standardizer maps unknown/N/A values to zero.
4. Legacy `sigma_a` is normalized/undocumented while PhotochemCAD-derived
   cross section is a physical unit-bearing value.
5. Some interpretation/output modules use language such as gain, prototype,
   power or laser class even though the underlying path is heuristic.

The G23 parallel path blocks or relabels each of these behaviors rather than
silently changing legacy results.

## Initial PhotochemCAD evidence benchmark

| Record | Core reported evidence | Completeness | Legacy decision path |
| --- | ---: | ---: | --- |
| BX003 Asn-Bx | 3/4 | 75% | Blocked |
| FL109 Quercetin | 2/4 | 50% | Blocked |
| CAR021a-6 Lutein [HPLC] | 1/4 | 25% | Blocked |

The completeness metric measures evidence coverage only, not laser quality.

## Test gates

Local read-only runner:

```
python run_g23_evidence_safety.py
```

Dedicated suites cover:

- evidence normalization and epsilon-to-sigma derivation;
- integration gate and unit isolation;
- physical spectral evidence;
- legacy/physical path comparison;
- Missing != Zero policy;
- strict standardization;
- engine compatibility;
- evidence registry conflict handling;
- evidence decision gating;
- strict decision wrappers;
- evidence-aware interpretation, trace and output.

A GitHub Actions workflow is staged at:

`.github/workflows/g23-evidence-safety.yml`

Latest verified GitHub Actions evidence-safety run completed successfully on
Python 3.12 with **74/74 tests passed**. The suite includes normalization,
integration gates, strict missing-data behavior, unit contracts, reporting,
legacy provenance audit, plant/compound linkage, and the unified external
evidence pipeline.

## Promotion sequence

Production promotion should occur only in this order:

1. Verify all G23 evidence tests locally/CI.
2. Resolve or explicitly retire legacy unit contracts for tau, sigma_a, eta,
   and knr.
3. Replace missing-to-zero behavior in production standardization and decision
   paths with strict states.
4. Validate the physical meaning of thermal, gain, Q-factor, beam-quality and
   efficiency formulas before calling them physical scores.
5. Propagate provenance through material score, LRI, confidence and final
   decision outputs.
6. Add experimental G23 components to PROJECT_REGISTRY only after their
   production promotion is approved.
7. Run regression against the frozen legacy dataset.
8. Merge only when no accepted scientific result changes without an explicit,
   reviewed reason.

## Current promotion decision

**GO for parallel development and evidence ingestion.**

**NO-GO for direct replacement of the production legacy decision pipeline.**

The platform can already use PhotochemCAD safely for evidence storage,
absorption/fluorescence analysis, unit-bearing derivations, evidence-aware
reporting, and compatibility assessment while the remaining legacy contracts
and scoring semantics are repaired.


## Legacy provenance audit result

For the current seven legacy plant records:

- 6/7 have at least one general reference record;
- 1/7 has no reference record (Acacia Nilotica);
- Henna resolves to two reference records and requires reconciliation;
- 0/7 currently have field-level provenance complete for the critical
  photophysical values;
- 0/7 current reference bundles contain a DOI in the stored metadata.

These findings do not invalidate the legacy records; they define the evidence
upgrade work required before those values can be promoted as physical source
data.

## Safe plant/compound linkage

The new compound linker permits exact-name supporting links while enforcing:

`substitution_allowed = False`

Current verified example:

- Legacy Moringa record lists active compound **Quercetin**.
- PhotochemCAD FL109 is **Quercetin**.
- The link is stored as `SUPPORTING_COMPOUND_EVIDENCE_ONLY`.
- Moringa extract `lambda_abs = 410 nm` remains untouched.
- PhotochemCAD isolated-compound `lambda_abs = 256 nm` remains a separate
  evidence object.

This boundary is required because isolated-compound spectra and plant-extract
spectra are not interchangeable.

## Unified external evidence pipeline

`g23_external_evidence_pipeline.py` now provides one evidence-safe entry path:

PhotochemCAD raw record
-> normalization
-> evidence registry
-> physical spectral analysis
-> engine compatibility audit
-> evidence decision gate
-> bounded interpretation
-> provenance trace
-> evidence-safe output
-> optional exact compound linkage to legacy plants

The returned package explicitly records:

- `legacy_scoring_invoked = False`
- `production_registry_mutated = False`
- `advanced_claims_authorized = False`

This enables continued database expansion while the legacy scoring contracts
are repaired in parallel.
