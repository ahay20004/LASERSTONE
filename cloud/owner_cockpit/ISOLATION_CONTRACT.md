# LASERSTONE owner cockpit — isolation contract (design gate)

Status: DESIGN ONLY. This document does not create authentication, deploy an owner service, or change public publication approval.

## Non-negotiable boundaries

1. The public LASERSTONE static preview is informational only. No university assets, private endpoints, privileged controls, or owner session credentials may enter its six-file release bundle.
2. The existing seven-building scientific university must remain intact. Never treat hidden HTML, CSS, JavaScript flags, obscured links, or a password stored in frontend code as access control.
3. The owner cockpit must be hosted in a separate private service or owner-controlled local application, protected by server-side authentication and authorization. Default deny on all routes and data access.
4. Require an authenticated owner identity, short-lived server-managed sessions, secure cookie settings (HttpOnly, Secure, SameSite), CSRF protection for state-changing requests, rate limiting, and auditable owner actions. MFA is recommended before remote exposure.
5. No direct browser access to local scientific engines, project files, raw research data, or execution capabilities. Use explicit server-side, allowlisted operations and isolated workers.
6. Do not store private university code or research data in a public repository or a public Hugging Face Space. A separate folder or branch in a public repository is **not** private. Historical public commits may still expose earlier content.
7. Maintain scientific provenance and validation gates; do not alter the frozen G23 baseline to implement cockpit access.
8. No upload, publication, migration, credential creation, or environment-secret changes without explicit owner approval.

## Acceptance gates for future implementation

- Public bundle contains exactly README.md, index.html, style.css, i18n.js, icon.svg, and manifest.webmanifest; no university identifiers, sections, translations, or private URLs.
- Anonymous access to every private owner route returns an authorization failure; public preview cannot access owner data.
- Non-owner authenticated identity cannot view or operate the university.
- Authorized owner can inspect the seven buildings through the protected service without exposing their content to the public preview.
- Tests cover expired sessions, forged CSRF tokens, direct deep links, unauthorized API calls, and attempts to reach local execution interfaces.
- Audit events do not log secrets or sensitive research content.
- Both Windows and Ubuntu regression suites pass; a separate manual owner security review approves any remote exposure.

## Next implementation decision

Select an actual private runtime and identity provider before writing owner-only UI code. The current public static cockpit is a non-live preview and must not be represented as authenticated.
