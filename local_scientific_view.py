"""Generate a local-only, read-only scientific bridge view. No HTTP server."""
from __future__ import annotations
from html import escape
from pathlib import Path
import webbrowser

from local_scientific_bridge import evaluate_synthetic_case

OUTPUT = Path(__file__).resolve().parent / "laserstone_local_scientific_view.html"

def render(report: dict) -> str:
    if report.get("input_kind") != "SYNTHETIC_DEMONSTRATION":
        raise ValueError("Only the synthetic demonstration is authorized for this view")
    source = escape(str(report["source_engine"]))
    score = escape(str(report["output"]["consistency_score"]))
    classification = escape(str(report["output"]["classification"]))
    rows = "".join(
        f"<tr><td>{escape(str(k))}</td><td>{escape(str(v))}</td></tr>"
        for k, v in report["inputs"].items()
    )
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; base-uri 'none'; form-action 'none'; connect-src 'none'; img-src 'none'">
<title>LASERSTONE Local Scientific View</title>
<style>
body{{background:#091426;color:#e6f2ff;font:16px system-ui,sans-serif;margin:0;padding:30px}}
main{{max-width:860px;margin:auto}}h1{{color:#74d7e6}}section{{background:#13263d;border:1px solid #35536a;border-radius:14px;padding:20px;margin:16px 0}}
strong{{color:#b7f5ee}}table{{border-collapse:collapse;width:100%}}td{{border-bottom:1px solid #35536a;padding:9px}}
.notice{{color:#ffd28c}}small{{color:#a8b9cb}}
</style></head><body><main>
<h1>LASERSTONE™ — Local Scientific View</h1>
<p class="notice"><strong>SYNTHETIC DEMONSTRATION ONLY</strong> · Not experimental evidence · Not independently validated</p>
<section><h2>Physics consistency engine</h2><p>Source: <code>{source}</code></p>
<p>Consistency score: <strong>{score}</strong></p><p>Classification: <strong>{classification}</strong></p></section>
<section><h2>Traceable synthetic inputs</h2><table>{rows}</table></section>
<section><h2>Evidence boundary</h2><p>No private datasets accessed. No network requests. No publication authorized.</p>
<small>This is a local prototype, not the deployed public preview or operational acceptance.</small></section>
</main></body></html>"""

def main() -> None:
    OUTPUT.write_text(render(evaluate_synthetic_case()), encoding="utf-8")
    print("Local view generated:", OUTPUT.name)
    webbrowser.open(OUTPUT.as_uri())

if __name__ == "__main__":
    main()
