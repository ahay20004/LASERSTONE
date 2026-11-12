# Paper 1 reproducible evidence-gate benchmark

This branch supports the manuscript:

**LASERSTONE: An Evidence-Aware and Provenance-Constrained Framework for Reproducible Screening of Natural Photonic Materials**

The benchmark is a controlled computational stress test of claim admission. It does **not** claim experimental optical gain, lasing, or validated device performance.

## Design

Eight generic photonic-input fields are sampled under numerical completeness levels of 25%, 50%, 75%, and 100%. For each present field, a controlled defect probability q in {0, 0.05, 0.10, 0.20} is applied independently to numerical validity, source traceability, and condition compatibility.

A numerical-only baseline admits a claim when all required values are present and numerically valid. The evidence-aware gate additionally requires a traceable source and compatible condition for each required field.

For a claim depending on k fields, the analytic probability of false promotion *conditional on numerical-only admission* is:

P(false promotion | numerical admission) = 1 - (1-q)^(2k)

because the numerical baseline ignores two evidence dimensions per required field: provenance and condition compatibility.

## Reproducibility

Run:

```
python paper1_evidence_benchmark.py
```

The random seed is fixed at **20261112** and each condition uses **50,000 trials**. Outputs are written to `paper1_outputs/`.

## Interpretation boundary

This benchmark verifies the behavior of the evidence-governance logic under controlled corruption and missingness. It is a software/methodological validation layer only. Experimental spectroscopy and laser measurements remain necessary for claims of gain, threshold, lasing, efficiency, and photostability.
