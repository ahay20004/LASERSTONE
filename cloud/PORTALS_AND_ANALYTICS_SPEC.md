# LASERSTONE — Owner, Researcher and Visitor Portal Specification
Status: DESIGN ONLY. No live authentication, tracking, database or analytics is deployed.

## Portals
OWNER: private dashboard with account approvals, project access, deployment approvals, scientific review queue, proposals, security alerts, consent-aware analytics and audit records.
RESEARCHER: personal workspace, assigned projects, approved tools, review requests, own usage history and feedback.
COLLABORATOR: explicitly scoped project access, no global user list.
VISITOR: public bilingual site, approved information and optional feedback with a privacy notice.

## Analytics: privacy-preserving by design
Measure aggregate visits, approximate active sessions, page popularity, research tool invocation counts, errors, performance and proposal status. Distinguish total page views, unique visitors (estimate), registered users and concurrent sessions. Never imply exact real-time physical presence or identity from website events.
Collect only necessary events with purpose, notice, consent/legal basis as applicable, retention policy and access controls. Avoid default precise geolocation, keystroke capture, full session replay, unpublished research content or unrestricted personal tracking. Show individual account activity to owner only where necessary and clearly disclosed for security/project governance.
Define privacy policy and review applicable Saudi PDPL and cross-border hosting requirements with counsel before collecting personal data.

## Security
Enforce server-side RBAC/ABAC with default-deny and tenant/project isolation. Owner login requires MFA. Secure session expiry, access revocation, audit logs, rate limits, encryption in transit/at rest, backups and incident response. Separate public frontend from authenticated API and private scientific compute.
Public static page must not present fake login or active-user numbers.

## Proposed minimal event schema (after review)
event_id, timestamp, event_type, anonymous_session_id_or_account_id (only if justified), project_id (if permitted), action_status, minimal diagnostic metadata. Never log passwords, raw scientific data or secrets.
Aggregate visitor statistics should have explicit time windows and definitions; online users may be approximated from recent authenticated heartbeats, not claimed as exact.

## Owner approval gates
1. Review privacy/data processing and hosting plan.
2. Review authentication and authorization architecture.
3. Build separate staging deployment with synthetic analytics.
4. Test permissions across roles, revocation, data isolation and security.
5. Verify metrics and accessibility in Arabic/English.
6. Obtain owner approval before enabling real users or telemetry.

## Suggested implementation phases
P0: bilingual public static preview and nonfunctional owner dashboard mockup using clearly labeled synthetic data.
P1: secure owner identity and read-only aggregate health dashboard.
P2: researcher invitation/approval and project access.
P3: consent-aware feedback, proposal queue and aggregated analytics.
P4: scientific agent and simulation services behind authorization and scientific validation gates.
