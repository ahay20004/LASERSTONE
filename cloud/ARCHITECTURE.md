# LASERSTONE Cloud — Hybrid Research Access (Design v0.1)

Status: PROPOSED; no public deployment, authentication integration, or production infrastructure is active.

## Objective
Publish a public scientific discovery/demo site while keeping research workspaces, private files, and privileged computation restricted to owner-approved users. Preserve the Windows SCAPS-1D workflow and G23 scientific provenance contracts.

## Trust boundaries
1. Public web: documentation, published examples and explicitly public synthetic datasets only; no arbitrary Python execution.
2. Authentication: managed identity provider; default deny; verified identity is not an approval to access private workspaces.
3. Authorization: server-side policy checks on every project, file, simulation request, and result; owner-managed invitations and revocation; deny cross-tenant access.
4. Scientific API: bounded, validated inputs, rate limits, execution budgets, immutable provenance and audit trail; never expose GitHub secrets or host file paths.
5. Worker tier: separate process/container, no direct public access; CPU/time/memory quotas; no SCAPS GUI exposed on cloud.
6. Data: private by default; separate public publication copies; per-project ownership, retention, export, and deletion policy; encrypt in transit and at rest.

## Roles and enforcement
- OWNER: manage invitations, memberships, publications, and deployments.
- RESEARCHER: manage own authorized projects; run permitted models.
- COLLABORATOR: explicitly scoped project-level read/write permissions.
- VISITOR: read public content and run bounded synthetic demonstrations only.

Roles are not UI-only. All permissions must be enforced by a backend and tested with negative cross-user cases. No open self-registration into RESEARCHER.

## Proposed stack (subject to deployment constraints)
- Frontend: responsive static site/PWA with public science pages, accessible branding, bilingual-ready content.
- API: Python FastAPI behind managed HTTPS; deploy separately from static site.
- Identity/data: managed authentication and PostgreSQL row-level access controls, if service selected and configured.
- Compute: Python workers for validated, sandboxed numerical jobs; Windows SCAPS execution remains offline or on a private, authenticated agent after separate security review.
- GitHub: pull requests, code review, test gates, and protected production deployments. Never deploy on a pull request from untrusted contributors with production credentials.

## Scientific integrity
Every output must distinguish MEASURED, DERIVED, SIMULATED, PREDICTED; include model version, inputs, units, provenance, warnings, and validation status. Parsing an IV file does not certify convergence or experimental agreement. Public demos must be labeled synthetic unless backed by traceable data.

## Deployment stages and acceptance gates
1. Foundation: architecture, threat model, CI, repo audit and dependency inventory. No public endpoints.
2. Public preview: static science landing page and read-only documented synthetic examples; verify no secrets/private data exposed.
3. Private beta: invite-only sign-in, owner approval, server-side authorization, audit and revocation tests; private storage.
4. Controlled compute: queue, quotas, timeouts, rate limiting, per-job provenance, and failure isolation.
5. Public launch: custom domain optional, HTTPS, PWA icon/manifest, social preview cards, privacy policy, terms, support, backup/restore tests, abuse controls.

## Release blockers
- No provider credentials or domain have been configured.
- SCAPS 3.0 legacy IV parser PR #2 remains under review; do not claim 31-run import or physical validation.
- Security and data classification audit required before publishing any current project artifacts.
- Confirm hosting plan limits, availability, cost, data residency, and provider terms before selection.
- Do not upload manuscript drafts, unpublished data, .def files, user details, or private keys to public demos.

## Operating rules
Keep g23/stage13-integration stable. Cloud work occurs on cloud/* branches, reviewed through draft PRs. Preserve local uncommitted/untracked Windows files. Do not use git reset --hard or git clean. Do not auto-merge or auto-deploy.
