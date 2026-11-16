# LASERSTONE Mission Control — baseline 2026-11-16

Status: reviewed development snapshot; **not** live monitoring. Branch:
`cloud/hybrid-access-foundation`. The last independently observed
successful cross-platform foundation run before this roadmap update was
commit `8c23f72` (GitHub Actions run 43826260254).

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
