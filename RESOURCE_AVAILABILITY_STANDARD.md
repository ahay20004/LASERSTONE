# LS-RAM — Resource Availability and Management
Supports LS-03, LS-14, LS-17, LS-18 and LS-19; does not add a new closure gate.

## Resource contract
Each resource must have a stable identifier, category, version, origin, license/access restrictions, expected integrity digest where applicable, local location, dependencies, acquisition route, verification status and recovery route. Distinguish missing, unverified, verified, incompatible and restricted resources.

## Availability policy
- Prefer verified, version-pinned local resources; support offline use where permitted.
- Preserve original bytes and provenance separately from normalized or derived data.
- Never silently substitute versions, constants, equations, engines or experimental datasets.
- Missing resources block only dependent operations; provide explicit diagnostic and permitted recovery route.
- Verify compatibility and integrity before activation. A digest alone does not establish authenticity.
- Archive permitted dependency packages, reference datasets, documentation and adapters; proprietary executables and licensed data remain subject to their terms.
- Keep secrets and private research data out of public repositories and logs.
- Use isolated staging, atomic activation, last-known-good version, and tested rollback; updates require owner consent.
- Maintain independent backups and periodically test restoration. A Git repository alone is not a complete backup.
- Use one launcher for normal operation and recovery diagnostics; avoid manual workflows where practical.

## Acceptance
Test offline retrieval, missing/corrupted resources, incompatible versions, dependency isolation, recovery, rollback and privacy. Verify actual Windows operation separately from CI. This document specifies requirements; implementation and acceptance remain pending.
