"""Build a LOCAL copy of the exact public-preview design with a synthetic engine panel."""
from __future__ import annotations
from html import escape
from pathlib import Path
import shutil
import webbrowser
from local_scientific_bridge import evaluate_synthetic_case

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "local_unified_site"
TARGET = ROOT / "laserstone_unified_local"
ASSETS = ("index.html", "style.css", "i18n.js", "icon.svg", "manifest.webmanifest")

def build() -> Path:
    report = evaluate_synthetic_case()
    if report["input_kind"] != "SYNTHETIC_DEMONSTRATION":
        raise ValueError("Only synthetic input is authorized")
    if not all((SOURCE / p).is_file() for p in ASSETS):
        raise FileNotFoundError("Reviewed preview assets missing")
    TARGET.mkdir(exist_ok=True)
    for name in ASSETS:
        if name != "index.html":
            shutil.copyfile(SOURCE / name, TARGET / name)
    html = (SOURCE / "index.html").read_text(encoding="utf-8")
    if html.count("</main>") != 1:
        raise ValueError("Unexpected original UI layout")
    rows = "".join(f"<tr><td>{escape(str(k))}</td><td>{escape(str(v))}</td></tr>" for k,v in report["inputs"].items())
    panel = f"""
<section id="local-scientific-evidence" class="section" aria-labelledby="local-evidence-title"
 style="background:#102b47;color:#effaff;border:2px solid #19b4c4;border-radius:16px;padding:24px;margin:30px auto;max-width:1100px">
<p style="font-weight:700;color:#ffd18a">LOCAL ONLY · SYNTHETIC DEMONSTRATION · NOT EXPERIMENTAL VALIDATION</p>
<h2 id="local-evidence-title">Local physics engine evidence / دليل المحرك الفيزيائي المحلي</h2>
<p>Source: <code>{escape(report["source_engine"])}</code></p>
<p>Consistency score: <strong>{escape(str(report["output"]["consistency_score"]))}</strong> ·
Classification: <strong>{escape(report["output"]["classification"])}</strong></p>
<details><summary>Traceable synthetic inputs / المدخلات الاصطناعية</summary><table>{rows}</table></details>
<p>Scientific validation: NOT ESTABLISHED · Private data: NOT ACCESSED · Public deployment: NOT AUTHORIZED</p>
</section>
"""
    html = html.replace("</main>", panel + "</main>")
    # The original preview remains unchanged. This local output forbids outbound connections.
    html = html.replace("<head>", '<head>\n<meta http-equiv="Content-Security-Policy" content="connect-src \'none\'; form-action \'none\'; object-src \'none\'; base-uri \'self\'">', 1)
    result = TARGET / "index.html"
    result.write_text(html, encoding="utf-8")
    return result

if __name__ == "__main__":
    result = build()
    print("Unified original preview design with local scientific evidence:", result)
    webbrowser.open(result.as_uri())
