# LASERSTONE Mission Control — baseline 2026-11-16

Status: reviewed development snapshot; **not** live monitoring. Branch:
`cloud/hybrid-access-foundation`. The last independently observed
successful cross-platform foundation run before this roadmap update was
commit `8c23f72` (GitHub Actions run 43826260254).

## Adopted development policy — CORE FIRST / UNIVERSITY PRESERVED (2026-11-16)

**Owner decision:** Develop and validate the original LASERSTONE scientific
project first. The scientific university is a **frozen future expansion**, not
a parallel workstream or a condition for core acceptance. Preserve its existing
seven-building campus, UI, code, assets, and history in their current canonical
locations. Do not delete or silently modify them to advance the core.

### Selective university-to-core reuse

- Inspect university modules and assets for **specific, demonstrable** value
  to core scientific calculations, evidence tracking, test automation, project
  navigation, security, or performance.
- Reuse only the **minimum necessary** code/configuration or a bounded adapter
  in the core, with its origin path, source commit, reason, license/dependency
  review, interface contract, and regression tests documented. Keep the
  university original **unchanged and in place**. Prefer referencing an existing
  shared scientific module over creating a second independent engine or dataset.
- Do not clone the entire university, its database, its session state, or its
  architecture into the core. If a genuinely reusable component requires a
  shared owner, propose and test a single canonical shared module, then update
  references without duplicating scientific logic.
- Core integration must remain independently runnable **without** the campus
  UI or university-specific imports. Any copy is a deliberate, traceable
  exception, not permission to fork the scientific truth.
- Record each extraction in a transfer register with fields:
  university source path / revision; core destination; functionality;
  scientific benefit; dependencies and rights; tests; owner approval;
  status. Reject items that add only visual complexity or unverified claims.

### First implementation of selective-reuse audit

- Added `cloud/core_first_university_audit.py`: read-only AST/source inspection of `city/*.py`, with candidate signals and explicit refusal to certify runtime, scientific validation, or transfers.
- Added `cloud/test_core_first_university_audit.py`: synthetic non-execution, non-mutation and invalid-source regression tests; included in Windows/Linux foundation workflow.
- **No university files copied or changed.** No transfers approved. This is a prioritization instrument, not a claim that a university engine has been integrated.
- Next: review candidate source code and actual core interfaces, then propose only narrowly scoped transfers with owner approval and evidence.

### Core acceptance and future university package

1. Reconcile and verify scientific engines, project registry, local Windows
   dashboard, numerical baselines, data provenance, simulation interfaces,
   and explicit unsupported cases.
2. Prepare an invention-disclosure inventory and seek qualified patent advice
   **before any further public technical disclosure**; existing public
   commits/previews require novelty and disclosure review. No patentability
   or grant is implied.
3. Require independent reproducible tests, documented limitations, security
   gates, and owner sign-off before marking the **core** release accepted.
4. Only after core acceptance and IP/disclosure review, unfreeze the university
   as **one separately tested integration package**, retaining its original
   canonical sources and adding explicit compatibility/rollback tests.
5. Until that milestone, university changes are restricted to critical
   preservation/security fixes explicitly approved by the owner; no campus
   expansion, new decorative UI, or independent university release.

**Priority order:** CORE scientific validity → core integration and stability
→ invention/IP review → core acceptance → future university integration.
Public static preview success does not certify the core or the university.

## Verified achievements

1. Bilingual public static preview and bounded hypothetical attenuation UI.
2. Equation contract with units, provenance and simulation status.
3. Exact-wavelength optical material record gate; no interpolation.
4. Optical regime dispatcher: unsupported physics rejected.
5. Universal input contract for units, finite values, bounds, provenance and
   caller-supplied variable relationship checks.
6. GitHub Actions foundation tests on Windows and Linux passed at `8c23f72`.

These are **software-level** milestones, not evidence of validated material
constants, engine convergence or experimental agreement.

## Next execution queue

| Priority | ID | Task | Completion evidence |
|---|---|---|---|
| P0 | LS-01 | Inventory existing physics engines, signatures, registries and test baselines | Versioned integration inventory with supported interfaces and known gaps |
| P0 | LS-02 | Implement dimension-aware unit handling and model-specific contracts | SI conversion regression suite, invalid-unit rejection, dimensional checks |
| P1 | LS-03 | Add traceable material adapters with provenance, validity ranges and conflict policy | Real sourced records with source IDs, uncertainty and applicability tests |
| P1 | LS-04 | Connect one verified engine through an isolated adapter | Reproducible inputs/outputs and independent numerical comparison |
| P2 | LS-05 | Add orchestrated agents and evidence/reproducibility reports | Auditable routing, no invented evidence, explicit validation states |

## Attention register — open

- ALERT-01: No authenticated live scientific engine or agent is connected to
  the public static preview.
- ALERT-02: Real material-property sources and experimental validation data
  are not integrated with the public calculator or generic dispatcher.
- ALERT-03: Universal dimensional algebra, approved conversions, uncertainty
  propagation and end-to-end equation coverage remain incomplete.

## Release rules

- Never promote a software test pass into a physical validation claim.
- No guessed coefficients, missing-source defaults, silent interpolation or
  fabricated uncertainty.
- Every engine adapter must specify assumptions, input/output units,
  numerical tolerances, source provenance and regression tests.
- The preview alert control is **local display only**: no push notifications,
  scheduled checks or user account data.
- Update this document, bilingual dashboard and tests together when a
  milestone changes; verify CI before marking it completed.

## Unified legacy restoration protocol — 2026-11-16

**Single authoritative platform:** keep the existing repository, project
registry, local Scientific University city and project dashboard. The public
Scientific Explorer is a separate access surface, not a second science engine.

**Evidence inspected:** root repository listing includes 63 root Python
files with engine-like/helper suffixes; `project_registry.py` declares
32 registry keys. Neither number is a count of validated independent engines.
The legacy `README_CITY.md` documents the seven-building local university
plaza, 16 project dashboard gateway buttons, shared `main.prepare_runtime()`
session and G23 local launch/test procedures. These are local architecture
claims requiring fresh end-to-end verification before release.

**Parallel lanes and gates:**

1. **Inventory / traceability:** run
   `python -m cloud.legacy_integration_inventory` (read-only JSON to stdout).
   Review registry mismatches, duplicate concepts, missing modules and AST
   parse errors. Do not import legacy engines during inventory.
2. **Physics / registry:** verify input/output contracts, source and
   evidence states, numerical regression and actual dependency edges. Test
   each callable independently before composing execution graphs.
3. **University / project UI:** preserve the existing university plaza,
   project dashboard, shared session and local navigation. Perform actual
   Windows GUI smoke tests; do not replace the university with the public
   landing page.
4. **External tools:** distinguish SCAPS executable discovery, explicit
   GUI invocation, saved I–V import, solver execution and physical
   validation. MATLAB synthetic exchange is not a real engine adapter.
   COMSOL/Zemax/Lumerical supported envelope IDs are not evidence of
   installed or licensed applications.
5. **Cloud / AI:** publish only reviewed educational/static content until
   authenticated backend, authorization, audit, provenance and explicit
   user approval exist. AI agents may propose changes, never silently
   rewrite the master, deploy private data or certify physical results.

**Promotion gates:** DISCOVERED → SOURCE_REVIEWED → CONTRACT_TESTED →
INTEGRATION_TESTED → PHYSICS_BENCHMARKED → LOCAL_UI_VERIFIED →
CLOUD_SERVICE_APPROVED. Each transition requires a dated evidence link,
test artifact, platform/OS, assumptions and reviewer sign-off. Never
infer a higher gate from a lower one.

**Open work:** reconcile the user's historical ~57 integrated/tested
engines with repository file and registry counts using actual archived
reports; verify all local GUI and simulator runs; build one isolated
backend adapter; refresh Mission Control only from auditable evidence.
The static public preview remains non-executing.

**No duplicate master:** this document is the current integration roadmap;
the original project modules and `project_registry.py` remain the
authoritative sources for code and declared engine interfaces.

## Master placement register — repository + historical conversation reconciliation

This section is the **single authoritative placement map**, not a second
registry or a duplicate of existing scientific modules. Repository code is
primary evidence for what is present; dated local test logs and archived
conversation notes are historical leads until reconciled to hashes and
artifacts. Do not upload private chat transcripts or unpublished research
to the public static Space.

| Asset / prior achievement | Authoritative location | Placement in platform | Evidence gate / next action |
|---|---|---|---|
| Existing engine modules and declared connections | Root `*_engine.py`, `project_registry.py` | Project scientific core | Inventory → actual import/call tests → physics checks; registry ACTIVE is only a declaration |
| G23 scientific input, consistency, laser and analysis pipeline | `g23_*.py`, `test_g23*.py`, `main.prepare_runtime()` | Project validation and orchestration | Re-run archived baselines against current commit; retain expected failures and known holds |
| Seven-building scientific university and city | `city/`, `README_CITY.md` | Independent campus UI with common project session | Windows visual smoke test and callback navigation; not the static web preview |
| Project dashboard / 16 gateway controls | `dashboard.py`, `dashboard_city.py`, `safe_dashboard_launcher.py` | Project Mission Control (local) | Verify all controls and shared-session state; avoid second database |
| Public Explorer and teaching calculators | `cloud/site/` | Public visitor educational portal | Static CI, no live scientific engine claims |
| Evidence and provenance | `physics_evidence_engine.py`, `scientific_trace_engine.py`, `cloud/equation_contract.py` | Cross-cutting validation layer | Map source/conditions/uncertainty; never elevate heuristics to measurement |
| Plant-dye/material screening and discovery | `database/`, `plants_data.py`, ranking and decision engines | Research laboratory and materials repository | Confirm dataset permissions, traceability and model applicability |
| SCAPS-1D photovoltaic workflow | `g23_simulation_exchange_contract.py`, local executable and saved I–V files | University research laboratories + solar research workspace | Separate installation, GUI launch, parser, solver execution, benchmark and scientific validation; do not redistribute SCAPS binaries |
| MATLAB Online and Python benchmark | G23 exchange contract and historical exchange files | Simulation laboratory | Historical BENCHMARK_MATCH_ONLY is not live solver validation |
| COMSOL, Zemax and Lumerical | G23 supported simulator identifiers | Future external integrations | Contract names only until licenses, installed executables and real adapters verified |
| AI council, agent roles and research assistant | `cloud/PARALLEL_EXECUTION_PLAN.md` | Private owner-controlled AI studio | Planned: secure backend, audit, role boundaries, source-grounded proposals, owner approval |
| Scientific references and DOI source records | `cloud/site/i18n.js` educational glossary (temporary) | Scientific Explorer / future source registry | Refactor to a structured reviewed source catalog; DOI recorded is not automatic source verification |
| Manuscript-derived research knowledge | Owner-controlled manuscript masters and consented extracts | Permissioned research repository, never public by default | One master per paper; provenance and publication/IP clearance required |
| Institutional access, collaboration, public portal | `cloud/ARCHITECTURE.md`, `cloud/site/` | Public gateway vs private research accounts | Auth, roles and data isolation required before accounts or private engines |

### Historical achievements to reconcile, not silently certify

- Prior G23 conversations reported 20/20 and later 70/70 software regression
  passes on dated local baselines; separate project documents mention 79/79
  and review-environment 56/56. These are **different test suites/snapshots**,
  not additive engine counts or current branch certification. Locate the
  original logs, commits, OS and exact test lists before recording them as
  verified current achievements.
- Historical user estimate of ~57 linked/tested engines remains a **reconciliation
  target**. The current source listing has 63 engine-like root filenames and
  32 declared registry keys; neither establishes 57 distinct tested engines.
- Historical SCAPS 3.3.12 Windows executable invocation and saved I–V import,
  and MATLAB Online exchange benchmark, are distinct stages; no automatic
  solver operation, end-to-end scientific validation or web deployment is
  implied by these historical reports.
- Historical SCAPS usage conditions prohibit redistribution/sale without
  authorization; treat the executable and licensed resources as **local only**.

### Placement and promotion protocol

1. Every item has one **canonical code/data owner** and one or more *views*;
   views link to the owner rather than copy its source or state.
2. For every claimed connection capture source module, callable signature,
   dependencies, input/output units, evidence state, version/commit, test
   artifact and explicit failure/unsupported cases.
3. Parallel review roles (inventory, physics, simulator, campus/UI, evidence,
   AI/security) propose findings into this roadmap. Only approved and tested
   changes enter the authoritative project branch.
4. AI is an **assistant**, not a scientific validator: it cannot infer
   measurements, autonomously alter manuscript masters, disclose private
   data, or claim deployed agents without an authenticated service.
5. Prioritize integration over additional decorative pages. The next
   promotion requires a real registry reconciliation report, cross-platform
   test results, local Windows campus checks and one independently benchmarked
   engine adapter.

## First legacy engine integration pilot — pending CI evidence

- Adapter: `cloud/legacy_laser_photon_adapter.py`; original owner
  `laser_physics_engine.calculate_laser_physics` remains unchanged.
- Test: `cloud/test_legacy_laser_photon_adapter.py`, included in the
  cross-platform Cloud foundation workflow.
- Bounded scope: photon frequency and energy only, 100–100000 nm and
  refractive index 1–5; three benchmark wavelengths 532, 632.8 and
  1064 nm. Independent benchmark uses exact SI constants; legacy uses
  rounded constants; maximum permitted relative discrepancy 0.1%.
- Excluded: cavity length, free spectral range, gain, real material
  validity, external solvers, GUI, live cloud service and experimental
  validation. These need separate scientific assessment.
- Status: SOURCE_ADAPTER_COMMITTED; **do not promote to TEST_PASSED until
  GitHub Actions completes successfully**. No public API exposed.

### Core registry reconciliation — static dependency gate

- Added `cloud/core_registry_dataflow_audit.py` to inspect the canonical `project_registry.py` **without importing it** or running any engine. It identifies declared producer-to-consumer input links, input names with no declared producer, output names with multiple providers, and registry entries lacking same-name root modules.
- Added `cloud/test_core_registry_dataflow_audit.py` and Windows/Linux CI inclusion. Missing providers may be external inputs, and multiple declared providers may be intentional: neither is automatically a defect.
- The audit is a **triage tool only**: registry `ACTIVE` does not prove runtime operation, callable compatibility, scientific validity or a patentable innovation. Review each flagged item against source interfaces and actual test evidence before changing the canonical registry.
- University remains frozen and untouched. Next: identify one core dataflow edge with matching function contracts and implement a bounded execution test.

### First bounded core-to-core scientific execution

- `cloud/core_spectral_photon_integration.py` composes the **existing** `laser_physics_engine.calculate_laser_physics` (via its bounded independent-SI adapter) with the **existing** `spectral_region.predict_spectral_region` on the same input wavelength.
- Allowed wavelength: **380–1100 nm**. This deliberately restricts the legacy classifier to visible and near-IR labels, and does not imply that its 750 nm threshold is a universal physical standard.
- Tests: 532, 632.8 and 1064 nm independent SI comparisons; exact legacy 750 nm boundary; refractive-index invariance of photon energy; invalid inputs. `cloud/test_core_spectral_photon_integration.py` added to Windows/Linux foundation CI.
- Acceptance is limited to **bounded software integration and numerical agreement**. No experimental verification, material characterization, gain/cavity claims, cloud execution, or university integration.
- Preserve originals; do not copy or modify university files. Next: CI verification, source-to-contract comparison and broader physical input evidence.

### Provenance-gated material scoring — next bounded core engine

- Added `cloud/core_material_score_gate.py` to call the **existing** `material_score_engine.calculate_material_score` only when all six required fields are explicitly supplied with finite bounded numeric values, named sources, and declared evidence states. Reject missing fields instead of the legacy implicit zero defaults.
- Validate legacy scoring weights and compare the returned result against a separately expressed weighted-sum formula. This establishes numerical implementation agreement **only**; neither the weights nor categories are scientifically calibrated by these tests.
- `cloud/test_core_material_score_gate.py` tests synthetic valid, missing, zero, invalid, and provenance cases on Windows/Linux CI.
- Source declarations are supplied by the caller, **not verified against a primary dataset**. Do not treat the resulting heuristic score as measured laser efficiency, proven material performance, novelty, or patentability. No university source changes or copies.

### Legacy thermal heuristic — evidence gate, not physical certification

- `cloud/core_thermal_screen_gate.py` invokes the **existing** `thermal_engine.evaluate_thermal_stability` after rejecting missing/extra inputs, nonfinite values, unlabelled provenance, incorrect canonical units and out-of-domain values.
- Input conventions: quantum yield dimensionless [0,1], lifetime in ns, nonradiative rate in ns^-1, refractive index dimensionless [1,5]. These unit conventions are **assumptions to verify against primary material sources**, not a validated original engine unit contract.
- Independent branch-by-branch threshold arithmetic is checked against the legacy function. `cloud/test_core_thermal_screen_gate.py` exercises valid, invalid, missing and boundary cases in cross-platform CI.
- **Scientific limitation:** the output is a heuristic screening label, not a measurement of thermal stability, temperature, photobleaching, or physical thermal lifetime. The underlying weights and thresholds require calibration before any predictive claims.
- University assets unchanged. Next: confirm CI and only then propose a documented thermal-to-material scoring handoff, without converting heuristic labels into measured evidence.

### Verified-contract thermal-to-material handoff (CI pending)

- `cloud/core_thermal_material_handoff.py` runs the existing thermal engine through its bounded gate, passes its output as a `DERIVED` score to the existing material scoring engine through its bounded gate, and retains input-level provenance.
- The handoff rejects caller-injected `thermal_score`, missing fields and invalid physical input domains. No legacy engine, registry or university source was modified.
- Synthetic fixture: thermal heuristic 100 and material heuristic 75.25. These are test values, **not experimental or calibrated physical findings**. `cloud/test_core_thermal_material_handoff.py` runs in Windows/Linux CI.
- Do not certify runtime integration until the updated workflow succeeds; do not claim experimental thermal stability, validated material performance or patentability from these heuristic scores.

### Phase 1 — comprehensive read-only engine inventory (2026-11-16)

- **Baseline from current registry:** 32 declared ACTIVE entries; 31 nominal directed output-to-input edges connecting 24 entries; 8 isolated in the registry graph. These counts do not establish actual runtime activation.
- **Source inventory:** `cloud/full_engine_audit.py` parses every repository Python file with AST, records top-level functions, class methods, signatures, registered engine presence, declared graph, and direct imported call sites in `main.py`. No imports/execution of original project modules; university files are parsed read-only and not changed.
- **Automated tests:** `cloud/test_full_engine_audit.py` covers synthetic graph, signatures, call sites, read-only behavior and current 32/31/24/8 registry baseline. Windows and Linux foundation CI run these tests.
- **Reproducible detailed results:** `python -m cloud.write_full_engine_audit` produces `audit-artifacts/engine_inventory.json` (full callable/signature/call-site evidence) and `audit-artifacts/ENGINE_AUDIT_REPORT.md` (per-engine table). GitHub Actions uploads separate `engine-audit-ubuntu-latest` and `engine-audit-windows-latest` artifacts for each successful workflow run. CI results must be checked before declaring this phase passed.
- **Interpretation:** a direct call site is static evidence only, not reachability; indirect/dynamic dispatch may be missed. Registered inputs/outputs are not necessarily function arguments. This audit neither verifies physical models nor claims full runtime, GUI, simulator or university integration.
- **Next acceptance gate:** review actual generated report, investigate mismatches and prioritize bounded engine contract tests without modifying canonical scientific modules.

### Phase 1 follow-up — confirmed spectral label contract discrepancy

- `cloud/spectral_material_contract_diagnostic.py` invokes the original spectral classifier, data standardizer, and material-score label converter on three explicitly synthetic fixtures. Current outputs: `High` => standardized 100 vs material direct 40; `Medium` => 60 vs 40; `Low` => 30 vs 40. This is an interface-semantic discrepancy, not a numerical calibration claim.
- `cloud/test_spectral_material_contract_diagnostic.py` asserts the current behavior on Windows/Linux CI. The original engines remain unchanged. The guard documents a known defect; a future deliberate canonical mapping policy and independent tests are required before resolving it.
- Prior full inventory generated reproducible Markdown/JSON artifacts successfully on both CI operating systems. Static inventory is not proof of runtime activation or physical correctness.

### Spectral material contract: adapter repair, tests and export

- Explicit canonical policy is the existing `data_standardization_engine` mapping: High=100, Medium=60, Low=30. `cloud/canonical_spectral_material_adapter.py` rejects incomplete/invalid inputs, derives the label using the existing spectral engine, converts it explicitly, and passes the numeric score through the provenance-gated material scoring engine.
- `cloud/test_canonical_spectral_material_adapter.py` tests all three labels, score arithmetic, provenance, and invalid inputs. Synthetic fixture score changes compared with current `main.py` label handoff: High +6.00, Medium +2.00, Low -1.00 points; these are **not** empirical material-ranking changes.
- `cloud/export_spectral_material_verification.py` emits `SPECTRAL_MATERIAL_VERIFICATION.md` and `spectral_material_verification.json` alongside the complete inventory CI artifacts on Windows/Linux.
- **Critical deployment boundary:** original `main.py` and legacy engines remain unchanged; the production analysis path is **not yet corrected**. Before deploying a main.py change, verify actual dataset effects, approve mapping semantics and run full regression. No physical validation claimed.
