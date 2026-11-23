# LASERSTONE Dynamic Scientific Agent Council — AC-01 scaffold

## Status and boundaries
This is an **offline, deterministic coordination scaffold**, not a deployed multi-agent runtime. It neither invokes Codex agents nor proves their presence on the user's Windows computer. `python agent_council.py discover` inventories only explicitly named repository paths and reports local/Codex runtime as unverified. No claims of independent expert review should be made until actual review records are supplied.

## Operating doctrine
- Convene the minimum relevant specialties; allow named temporary guest advisers.
- Each reviewer submits a distinct evidence-backed position; do not fabricate expert opinions.
- Preserve disagreement rather than converting votes into scientific proof.
- All assigned reviewers, including guests, must report before a recommendation is ready.
- Human decision must be explicit: approve, revise, or reject, with rationale.
- A human approval of a recommendation **does not** authorize code execution, GitHub merge, publication, or release; existing project gates and permissions still apply.
- Never modify main directly; use reviewable branches and tests.
- No unpublished data, secrets, or third-party licensed material in public review records.

## Record format
Create a JSON task, for example:
```json
{"id":"AC-01","summary":"Physics and numerical stability audit","specialties":["physics","numerical"],"guests":["wien2k_guest"]}
```
Convene using `python agent_council.py convene --task task.json --record council.json`. A review input is `{"reviewer":"physics","position":"revise","reason":"Need convergence evidence","evidence":["test/report reference"]}`. Submit with `python agent_council.py review --input review.json --record council.json`. After all reviews, a human decision input is `{"decision":"revise","rationale":"Require independent validation"}`, submitted with `python agent_council.py decide --input decision.json --record council.json`.

## Integration roadmap
1. Audit Windows-local VS Code/Codex agent configurations and verify identities, capabilities, and permissions; no remote GitHub tree scan can prove these.
2. Add adapters for verified real agents; ensure distinct review provenance and scoped context.
3. Integrate council invocation into the existing master launcher without replacing `safe_dashboard_launcher.py` or `city/plaza_launcher.py`.
4. Require evidence-gate and security tests before enabling actions.
5. Validate on actual Windows hardware. CI alone is not operational GO.

## Tests
`python -m unittest discover -s tests -p test_agent_council.py -v` runs only council unit tests. Passing them does not validate physical models, real agent collaboration, or local Windows deployment.
