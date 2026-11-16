# LASERSTONE owner-governed unattended development

## Operating boundary

GitHub Actions runs in GitHub's cloud while the researcher's Windows computer is off. The workflow `.github/workflows/laserstone-governance.yml` runs on development-branch pushes, daily at 03:15 UTC, or manually. It records the last 30 commits with their author timestamps, the current immutable commit SHA, and changed paths. Its review packet is uploaded as a GitHub Actions artifact for 90 days. Git commits and workflow histories remain the primary dated audit trail; artifact retention is not permanent archiving.

The daily workflow **does not autonomously write new features, alter scientific engines, or publish anything**. It performs tests and prepares a decision packet. Unattended code development requires a separately authorized, sandboxed agent with scoped credentials, bounded tasks, spending limits, tests, and approval gates. No such agent is enabled by this change.

## Publication approval contract

The Hugging Face deploy workflow has no push trigger. An owner must explicitly run `huggingface-preview.yml` with `decision=approve` and the full 40-character SHA of the reviewed current development-branch HEAD. `approve_with_changes` and `reject` do not deploy. The workflow rechecks SHA, static-only allowlist, and scientific regressions. The `huggingface-preview` GitHub environment should additionally require the owner's approval via **Settings → Environments → huggingface-preview → Required reviewers**, if the repository plan supports it; enable prevent-self-review where applicable. Restrict workflow dispatch permissions and protect the branch.

Important: GitHub workflow_dispatch is normally discoverable in the Actions UI only after the workflow exists on the repository's default branch. Merge the reviewed workflow changes through the protected PR before relying on the Actions button. Do not merge scientific engine changes merely to activate governance.

## Cockpit decisions

The public Hugging Face Space is static and must never hold GitHub or Hugging Face write tokens. A secure cockpit decision UI is **not yet implemented**. The future cockpit requires authentication, owner authorization, CSRF protection, server-side audit records, one-time signed decisions tied to the exact commit SHA, and a private backend that dispatches the approved workflow. Until then, GitHub Actions is the approval interface.

## Verification doctrine

REPAIR → TEST → VERIFY → APPROVE → PUBLISH. Keep CORE FIRST, UNIVERSITY FROZEN. Distinguish MEASURED, DERIVED, SIMULATED, and PREDICTED. An automated test pass is not scientific validation.
