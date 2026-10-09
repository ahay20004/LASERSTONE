# LASERSTONE™ — Scientific and Engineering Charter (G23 Draft)

**Status:** PROPOSED / NOT YET RATIFIED  
**Scope:** LASERSTONE research platform and its scientific software lifecycle  
**Change policy:** This document is non-executable and does not change approved data, equations, results, or the `main` branch.

## Three complementary principles

### 1. A strong scientific project — مشروع
LASERSTONE shall have one identifiable authoritative source, traceable versions, reproducible workflows, documented interfaces, and testable scientific and engineering requirements. Its modules must be evaluated as parts of one system, not as disconnected copies.

### 2. A setter of rigorous internal methodology — مُشرِّع
LASERSTONE may define **internal** scientific gates, evidence classes, validation procedures, provenance rules, and publication-readiness checks. These rules do **not** supersede physical laws, recognized standards, journal requirements, independent peer review, or experimental evidence.

### 3. Open to new scientific horizons — مُشرَع الآفاق
The platform should support extensible laser and material classes, multiple simulation backends, new validated equations, and new research questions. Expansion must use documented adapters and versioned schemas; an experimental idea is never automatically promoted to established knowledge.

## Non-negotiable scientific controls

1. **Source of truth:** GitHub plus the designated local working tree. Preserve local unpushed work before reconciliation; do not assume a remote branch contains it.
2. **Value origin:** Every reported scientific quantity is labeled measured, literature-sourced, derived, simulated, predicted, or heuristic.
3. **Provenance:** Preserve source identifiers/DOIs when available, measurement or simulation conditions, units, methods, software versions, and uncertainty or a documented reason for its absence.
4. **Dimensional validity:** Physical equations and outputs must pass unit and domain checks. Dimensionless ranking scores cannot be called measured gain, laser efficiency, or thresholds without a validated mapping.
5. **Evidence gates:** Distinguish code correctness, numerical verification, physical validation, independent benchmark comparison, and publication suitability. Passing one gate does not imply passing the others.
6. **No silent promotion:** Novel theoretical proposals remain hypotheses or model predictions until supported by suitable derivation, tests, benchmarks, and external evidence.
7. **Fail safely:** Missing inputs or unsupported regimes must produce explicit unavailable/insufficient-evidence outcomes, not invented values.
8. **Reproducibility:** Store input fingerprints, parameter versions, backend versions, configuration, seeds where relevant, and audit outcomes for scientific runs.
9. **Modular simulation:** External packages (e.g. SCAPS-1D, MATLAB, COMSOL, MEEP) require explicit availability checks, licenses where applicable, backend-specific validity domains, and adapters; no connector is considered operational without a verified end-to-end run.
10. **Protected integration:** Develop and test on branches, review diffs, and propose merging into `main` only after reconciliation and approval. Never delete approved results or overwrite scientific locks silently.

## G23 qualification ladder

| Gate | Required evidence | Outcome |
| --- | --- | --- |
| G0 — Repository integrity | Inventory, branch/working-tree reconciliation, no destructive changes | PASS / BLOCK |
| G1 — Static integrity | Parse, duplicate-symbol and import checks | PASS / BLOCK |
| G2 — Data integrity | Types, units, provenance, ranges, uncertainty | PASS / BLOCK |
| G3 — Mathematical integrity | Dimensional checks, assumptions, limiting cases | PASS / BLOCK |
| G4 — Numerical verification | Reference cases, convergence, deterministic reruns | PASS / BLOCK |
| G5 — Physical validation | Independent experimental/literature benchmarks and applicability domain | PASS / BLOCK |
| G6 — Simulator integration | Real backend execution, I/O mapping, error handling and reproducibility | PASS / BLOCK |
| G7 — Publication support | Claim–evidence mapping, transparent limitations, references and disclosure | PASS / BLOCK |

**Current status:** No G0–G7 gate is declared passed by this charter. The G23 static audit is an initial screening utility, not scientific qualification.

## Adoption

This charter becomes an operational policy only after repository review, tests, and explicit approval. Any future amendment must be versioned and justified by traceable evidence.
