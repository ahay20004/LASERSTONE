# LASERSTONE isolated release — conditional approval evidence

Status: **NOT APPROVED FOR MERGE OR PUBLIC DEPLOYMENT**. Owner authorized remediation and re-review only.

## Separation
- Release PR #4 includes static preview, governance tooling, test fixtures and manual deploy workflow.
- Scientific integration and modified `main.py` remain in PR #3; no core or university modifications in this isolated PR.
- `cloud/MISSION_CONTROL_ROADMAP.md` and `cloud/site/_headers` are test/review files; neither is included in the six-file Hugging Face deploy allowlist.

## Security and permission gates — unresolved
- [ ] Verify repository visibility and all public assets for private research data, identifying information, unpublished claims and third-party licenses.
- [ ] Owner verifies GitHub Environment `huggingface-preview` has required reviewers, with prevent-self-review where supported.
- [ ] Owner verifies branch protection and authorized workflow dispatchers; the `approve` input alone is **not authentication**.
- [ ] Owner verifies `HF_TOKEN` remains private and limited to the intended Space.
- [ ] Confirm default-branch workflow-dispatch activation via a separately reviewed governance change. Do not merge the scientific PR for this purpose.

## Scientific and user-experience gates — unresolved
- [ ] Independent comparison of the frozen `main.py` and university modules to the release PR base.
- [ ] Browser/manual checks: Arabic RTL, English, keyboard, mobile, localStorage-disabled mode, green seven-day unread and full 48-hour post-open.
- [ ] Confirm HTTPS/CSP behavior on actual Hugging Face hosting; local `_headers` may not be honored by Hugging Face static Spaces.
- [ ] Confirm static examples and derived CSV outputs do not imply measured or solver-validated data.
- [ ] Owner explicitly reviews and approves the **exact** release SHA after all checks.

## CI evidence
The isolated Windows/Linux workflow compiles the cloud code, runs static preview and governance tests, verifies original G23 scientific regressions, and stages a six-file allowlisted payload. CI success is necessary but not sufficient for publication.

## Publication decision
**HOLD**. No merge and no Hugging Face upload under conditional remediation authorization.
