# LASERSTONE public preview

Static, no JavaScript, no authentication, no data collection, no simulations. No private datasets or repository secrets should be copied here.

## Preview locally
From repository root: `python -m http.server 8000 --directory cloud/site`, then visit `http://localhost:8000`.

## Cloudflare Pages (when owner approves deployment)
- Connect the GitHub repository with the least privilege possible.
- Production branch: select a reviewed release branch only, not a development branch.
- Build command: none; output directory: `cloud/site` (relative to repo root).
- Set a public domain only after reviewing content, privacy policy, deployment access and licensing.
- Do not add authentication by hiding UI elements: enforce backend access on every request.

## Acceptance
- All links point to public page sections; no login or form collects data.
- Mobile layout and keyboard navigation checked.
- Security headers verified on deployed host.
- Social preview requires a deployed absolute OG image URL; not configured yet.
- SVG favicon and web manifest included; cross-browser installability not guaranteed.
