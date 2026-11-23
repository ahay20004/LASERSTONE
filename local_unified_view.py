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
    # Keep the original header, branding, sidebar and navigation as the shared shell.
    # The welcome is page content, not a competing header or separate interface.
    welcome = """
<section id="laserstone-welcome" class="section" aria-labelledby="laserstone-welcome-title"
 style="background:#102b47;color:#effaff;border:1px solid #1ba7b8;border-radius:16px;padding:24px;margin:20px 0">
<p style="color:#8ee7eb;font-size:.85rem">LASERSTONE™</p>
<div data-welcome-lang="en" lang="en" dir="ltr">
<h2 id="laserstone-welcome-title" style="color:#fff">Welcome to LASERSTONE™</h2>
<p>Where physics meets innovation, and scientific knowledge, simulation, and research converge in one evidence-driven environment.</p>
<p>Knowledge through consultation, judgment through evidence, action through approval, and entrusted secrets kept secure.</p>
<p><strong>Founded and Developed by Dr. Abdelrahman A. Hagar</strong> · Founder &amp; Scientific Director</p>
<p style="font-size:.85rem;color:#b9c9d8">Local preview · Independent scientific validation is not implied.</p>
</div>
<div data-welcome-lang="ar" lang="ar" dir="rtl" hidden>
<h2 style="color:#fff">مرحبًا بكم في LASERSTONE™</h2>
<p>حيث تلتقي الفيزياء بالابتكار، وتتحد المعرفة والمحاكاة والبحث العلمي في بيئة واحدة، تُبنى فيها النتائج على الأدلة، وتُصان فيها الأمانة العلمية، ويبقى القرار للإنسان.</p>
<p>«العلم بالمشاورة، والحكم بالدليل، والتنفيذ بالموافقة، والأسرار في أمانة أصحابها».</p>
<p><strong>تأسست وطُوّرت على يد د. عبدالرحمن أ. هجر</strong> · المؤسس والمدير العلمي</p>
<p style="font-size:.85rem;color:#b9c9d8">معاينة محلية · لا تعني التحقق العلمي المستقل.</p>
</div>
</section>
"""
    marker = '<div class="mission-content">'
    if html.count(marker) != 1:
        raise ValueError("Original shared page shell not found")
    html = html.replace(marker, marker + "\\n" + welcome, 1)
    # Synchronize with the existing language selector without modifying original assets.
    lang_script = """document.addEventListener('DOMContentLoaded', () => {
  const selector = document.getElementById('language-select');
  const panels = document.querySelectorAll('[data-welcome-lang]');
  if (!selector || panels.length !== 2) return;
  function updateWelcome() {
    const language = selector.value === 'ar' ? 'ar' : 'en';
    for (const panel of panels) panel.hidden = panel.dataset.welcomeLang !== language;
  }
  selector.addEventListener('change', updateWelcome);
  updateWelcome();
});
"""
    (TARGET / "welcome-language.js").write_text(lang_script, encoding="utf-8")
    html = html.replace("</head>", '<script src="./welcome-language.js" defer></script>\\n</head>', 1)
    # The original preview remains unchanged. This local output forbids outbound connections.
    html = html.replace("<head>", '<head>\n<meta http-equiv="Content-Security-Policy" content="connect-src \'none\'; form-action \'none\'; object-src \'none\'; base-uri \'self\'">', 1)
    result = TARGET / "index.html"
    result.write_text(html, encoding="utf-8")
    return result

if __name__ == "__main__":
    result = build()
    print("Unified original preview design with local scientific evidence:", result)
    webbrowser.open(result.as_uri())
