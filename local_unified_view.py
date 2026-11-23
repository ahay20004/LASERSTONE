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
    # Welcome and founder attribution are local-only pending separate public release approval.
    welcome = """
<section id="laserstone-welcome" aria-labelledby="laserstone-welcome-title"
 style="max-width:1100px;margin:24px auto;padding:28px;border-radius:18px;background:#102b47;color:#effaff;border:1px solid #1ba7b8;box-shadow:0 12px 32px #081b2b33">
<p style="letter-spacing:.1em;color:#8ee7eb;font-size:.8rem">LASERSTONE™ SCIENTIFIC RESEARCH PLATFORM</p>
<h1 id="laserstone-welcome-title" lang="ar" dir="rtl" style="color:#fff">مرحبًا بكم في LASERSTONE™</h1>
<p lang="ar" dir="rtl">حيث تلتقي الفيزياء بالابتكار، وتتحد المعرفة والمحاكاة والبحث العلمي في بيئة واحدة، تُبنى فيها النتائج على الأدلة، وتُصان فيها الأمانة العلمية، ويبقى القرار للإنسان.</p>
<p lang="ar" dir="rtl" style="color:#a9f1eb;font-weight:700">«العلم بالمشاورة، والحكم بالدليل، والتنفيذ بالموافقة، والأسرار في أمانة أصحابها».</p>
<h2 style="color:#fff">Welcome to LASERSTONE™</h2>
<p>Where physics meets innovation, and scientific knowledge, simulation, and research converge in one evidence-driven environment.</p>
<p><strong>Founded and Developed by Dr. Abdelrahman A. Hagar</strong><br>Founder &amp; Scientific Director</p>
<p style="font-size:.85rem;color:#b9c9d8">Local preview · Scientific services and independent validation are not implied.</p>
</section>
"""
    if html.count("<body>") != 1:
        raise ValueError("Unexpected body structure in original UI")
    html = html.replace("<body>", "<body>\\n" + welcome, 1)
    # The original preview remains unchanged. This local output forbids outbound connections.
    html = html.replace("<head>", '<head>\n<meta http-equiv="Content-Security-Policy" content="connect-src \'none\'; form-action \'none\'; object-src \'none\'; base-uri \'self\'">', 1)
    result = TARGET / "index.html"
    result.write_text(html, encoding="utf-8")
    return result

if __name__ == "__main__":
    result = build()
    print("Unified original preview design with local scientific evidence:", result)
    webbrowser.open(result.as_uri())
