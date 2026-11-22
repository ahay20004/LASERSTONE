"""Stage 4.1: dependency-free read-only HTML scientific dashboard.

Only renders verified-schema Stage 4.0 JSON. Escapes all user-provided fields;
never alters or upgrades scientific validation status.
"""
import argparse
from html import escape
import json
from pathlib import Path

try:
    from .integrated_validation_dashboard import build
except ImportError:
    from integrated_validation_dashboard import build


def render(report):
    if not isinstance(report, dict):
        raise ValueError("Dashboard report must be an object")
    required = {"theory_id", "version", "proposal_sha256", "stages",
                "gaps", "scientific_validity", "publication_readiness",
                "endorsement", "claims_authorized"}
    if not required.issubset(report):
        raise ValueError("Missing Stage 4.0 report fields")
    if (report["scientific_validity"] != "NOT_ESTABLISHED"
            or report["publication_readiness"] != "NOT_ESTABLISHED"
            or report["endorsement"] != "NONE"
            or report["claims_authorized"] != []):
        raise ValueError("Unapproved scientific endorsement")
    if not isinstance(report["stages"], dict) or not isinstance(report["gaps"], list):
        raise ValueError("Invalid stage status or gaps")
    if not all(isinstance(x, str) for x in report["gaps"]):
        raise ValueError("Invalid gap item")
    for key in ("theory_id", "version", "proposal_sha256"):
        if not isinstance(report[key], str) or not report[key].strip():
            raise ValueError("Invalid identity field")
    if not all(isinstance(k, str) and isinstance(v, str) for k, v in report["stages"].items()):
        raise ValueError("Invalid stage item")
    e = lambda v: escape(str(v), quote=True)
    rows = "".join("<tr><th scope='row'>" + e(k) + "</th><td>" + e(v) + "</td></tr>"
                   for k, v in sorted(report["stages"].items()))
    gaps = "".join("<li>" + e(g) + "</li>" for g in report["gaps"])
    if not gaps:
        gaps = "<li>No metadata gaps reported; scientific verification is still outstanding.</li>"
    return """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>LASERSTONE Scientific Validation Dashboard</title>
<style>
:root{color-scheme:light dark;font-family:system-ui,sans-serif}
body{max-width:920px;margin:2rem auto;padding:0 1rem;line-height:1.55}
header{border-bottom:2px solid #64748b;margin-bottom:1.5rem}
section{margin:1.5rem 0}table{border-collapse:collapse;width:100%}
th,td{border-bottom:1px solid #94a3b8;padding:.7rem;text-align:left;vertical-align:top}
th{width:40%}.note{border-left:4px solid #64748b;padding:1rem}
code{overflow-wrap:anywhere}
</style></head><body><header><h1>LASERSTONE™ Scientific Validation Dashboard</h1>
<p>Read-only technical status — not a scientific certification</p></header>
<section><h2>Theory identity</h2><p><strong>""" + e(report["theory_id"]) + """</strong> · version """ + e(report["version"]) + """</p>
<p>Proposal SHA-256: <code>""" + e(report["proposal_sha256"]) + """</code></p></section>
<section><h2>Validation stages</h2><table><thead><tr><th>Stage</th><th>Reported status</th></tr></thead>
<tbody>""" + rows + """</tbody></table></section>
<section><h2>Reported gaps</h2><ul>""" + gaps + """</ul></section>
<section class="note"><h2>Scientific decision</h2>
<p>Scientific validity: <strong>NOT ESTABLISHED</strong></p>
<p>Publication readiness: <strong>NOT ESTABLISHED</strong></p>
<p>Claims authorized: <strong>NONE</strong></p>
<p>Successful software checks and self-declared review records do not authenticate evidence or prove a theory.</p>
</section></body></html>"""


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--dashboard-json", help="Existing Stage 4.0 JSON report")
    p.add_argument("--unified")
    p.add_argument("--uncertainty")
    p.add_argument("--independent-review")
    p.add_argument("--claims")
    p.add_argument("--out", required=True)
    args = p.parse_args()
    sources = {"unified": args.unified, "uncertainty": args.uncertainty,
               "independent_review": args.independent_review, "claims": args.claims}
    if args.dashboard_json and any(sources.values()):
        p.error("Provide either --dashboard-json or upstream reports, not both")
    if args.dashboard_json:
        report = json.loads(Path(args.dashboard_json).read_text(encoding="utf-8"))
    else:
        reports = {k: json.loads(Path(v).read_text(encoding="utf-8"))
                   for k, v in sources.items() if v}
        report = build(reports)
    output = Path(args.out)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render(report), encoding="utf-8")
    print(str(output))


if __name__ == "__main__":
    main()
