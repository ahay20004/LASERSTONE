# LASERSTONE Paper II — Project Governance

## Scope
This directory is reserved for "Physics-Constrained Spectral Evidence Integration for Reproducible Screening of Natural Photonic Materials" (Paper II). It is a subproject of LASERSTONE, not a transfer of authorship, copyright, or ownership.

## Ownership and attribution
- Research manuscripts retain their actual authors and their existing rights and obligations.
- Source datasets, third-party software, figures, and external materials retain their original licenses and attribution requirements.
- Integration into LASERSTONE does not by itself grant rights to redistribute, sublicense, or publish materials.
- Do not upload unpublished manuscripts, confidential data, or third-party materials without the rights holder's authorization.
- Record the authors, provenance, rights status, and permitted uses for each artifact before publication.
- Repository access and code contribution do not establish scientific authorship.

## Development controls
- Never modify `main` as part of Paper II development without explicit review and approval.
- Develop and test on `paper2/physics-constrained-spectral-evidence`.
- Maintain one authoritative manuscript master, with evidence traceability and targeted green-marked revisions.
- Keep measured, derived, predicted, and hypothetical claims distinct.
- Use gates for provenance (G1), analysis validity (G2), physical consistency (G3), numerical robustness (G4), reproducibility (G5), manuscript traceability (G6), and publication readiness (G7).
- A gate passes only after its specified tests actually execute; no fabricated results.
- Keep test inputs and outputs traceable to checksums, versions, and stated methods.

## Current migration status
Governance scaffold only. The user's local Paper II project files have NOT yet been imported or synchronized to this branch. No claim of local deployment or gate execution is made.

## Next migration requirement
Import the exact authoritative project contents using a secure authorized synchronization method. Inspect the file list and rights status before publishing to a public repository. Exclude virtual environments, secrets, private data, and generated output unless explicitly approved.
