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
<style>
#laserstone-welcome {position:relative;isolation:isolate;overflow:hidden;clear:both;min-height:580px;display:grid;place-items:center;margin:24px 0 48px;padding:32px 24px;border:1px solid #267b9b;border-radius:22px;background:radial-gradient(ellipse at 50% 34%,#164d68 0%,#102b47 55%,#081b30 100%);color:#f1faff;text-align:center}
#laserstone-welcome .welcome-inner{width:100%;max-width:900px;margin:auto}
#laserstone-welcome h2{color:#fff;font-size:clamp(1.5rem,3vw,2.35rem);margin:12px 0}
#laserstone-welcome p{max-width:760px;margin:12px auto;line-height:1.8}
#laserstone-welcome .laser-scene{display:block;width:100%;max-width:780px;height:auto;margin:8px auto 0;overflow:visible}
#laserstone-welcome .beam{animation:laser-pulse 3.6s ease-in-out infinite;transform-origin:center}
#laserstone-welcome .laser-mirror{transition:stroke .8s ease,fill .8s ease}
#laserstone-welcome .laser-output{transition:stroke 1s ease}
#laserstone-welcome .resonator-status{color:#b8e8f2;font-size:.88rem}
#laserstone-welcome .pump{animation:laser-pulse 2.6s ease-in-out infinite}
#laserstone-welcome .gain{animation:laser-glow 3s ease-in-out infinite}
#laserstone-welcome .welcome-founder{border-top:1px solid #3c7088;padding-top:14px;color:#bceff1}
#laserstone-welcome .welcome-role{margin:12px auto;padding:8px 12px;max-width:360px;border:1px solid #538a9b;border-radius:9px;background:#12364c;color:#fff}
#laserstone-welcome [hidden]{display:none!important}
#laserstone-welcome .scene-caption{color:#9fcbd8;font-size:.82rem}
@keyframes laser-pulse{50%{opacity:.45}}
@keyframes laser-glow{50%{opacity:.68}}
@media(prefers-reduced-motion:reduce){#laserstone-welcome .beam,#laserstone-welcome .pump,#laserstone-welcome .gain{animation:none}}
@media(max-width:600px){#laserstone-welcome{padding:20px 12px;min-height:auto}}
</style>
<section id="laserstone-welcome" class="section" aria-label="LASERSTONE welcome">
<div class="welcome-inner">
<p style="color:#8ee7eb;letter-spacing:.12em;font-size:.85rem">LASERSTONE™ · SCIENTIFIC RESEARCH PLATFORM</p>
<svg class="laser-scene" viewBox="0 0 780 270" role="img" aria-label="Conceptual laser resonator with pump, gain medium, two mirrors and output beam" xmlns="http://www.w3.org/2000/svg">
<defs>
<linearGradient id="ls-beam" x1="0" x2="1"><stop stop-color="#67e9fa" stop-opacity=".2"/><stop offset=".5" stop-color="#79faff"/><stop offset="1" stop-color="#38f0dc"/></linearGradient>
<linearGradient id="ls-gain" x1="0" x2="1"><stop stop-color="#0f7eac"/><stop offset=".5" stop-color="#9ef2c8"/><stop offset="1" stop-color="#0f7eac"/></linearGradient>
<filter id="ls-glow"><feGaussianBlur stdDeviation="5"/></filter>
</defs>
<g fill="none" stroke="#436e8d" stroke-width="1.5" opacity=".55"><path d="M65 224H713"/><path d="M110 43H670"/></g>
<path class="pump laser-pump" d="M360 15V105" stroke="#ff5252" stroke-width="4" stroke-dasharray="10 7" opacity="0.8"/><path class="pump laser-pump" d="M360 15V105" stroke="#ff5252" stroke-width="15" opacity=".16" filter="url(#ls-glow)"/>
<path class="pump laser-pump" d="M375 15V105" stroke="#ff5252" stroke-width="4" stroke-dasharray="10 7" opacity="0.8"/><path class="pump laser-pump" d="M375 15V105" stroke="#ff5252" stroke-width="15" opacity=".16" filter="url(#ls-glow)"/>
<path class="pump laser-pump" d="M390 15V105" stroke="#ff5252" stroke-width="6" stroke-dasharray="10 7" opacity="1"/><path class="pump laser-pump" d="M390 15V105" stroke="#ff5252" stroke-width="15" opacity=".16" filter="url(#ls-glow)"/>
<path class="pump laser-pump" d="M405 15V105" stroke="#ff5252" stroke-width="4" stroke-dasharray="10 7" opacity="0.8"/><path class="pump laser-pump" d="M405 15V105" stroke="#ff5252" stroke-width="15" opacity=".16" filter="url(#ls-glow)"/>
<path class="pump laser-pump" d="M420 15V105" stroke="#ff5252" stroke-width="4" stroke-dasharray="10 7" opacity="0.8"/><path class="pump laser-pump" d="M420 15V105" stroke="#ff5252" stroke-width="15" opacity=".16" filter="url(#ls-glow)"/>
<path id="ls-pump-arrow" class="laser-pump" d="M382 94L390 107 398 94" fill="none" stroke="#ff5252" stroke-width="3"/>
<path id="ls-hr-mirror" class="laser-mirror" d="M150 105V212" fill="none" stroke="#8fe8f8" stroke-width="12" stroke-linecap="round"/>
<path id="ls-oc-mirror" class="laser-mirror" d="M626 105V212" fill="none" stroke="#8fe8f8" stroke-width="12" stroke-opacity=".7" stroke-linecap="round"/>
<path class="beam" d="M159 159H617" stroke="#5cf8f4" stroke-width="18" opacity=".3" filter="url(#ls-glow)"/>
<path class="beam" d="M159 159H617" stroke="url(#ls-beam)" stroke-width="5"/>
<rect class="gain" x="340" y="119" width="100" height="80" rx="15" fill="url(#ls-gain)" fill-opacity=".65" stroke="#baffec" stroke-width="2"/>
<g fill="#e6fff5"><circle cx="365" cy="143" r="3"/><circle cx="411" cy="164" r="4"/><circle cx="385" cy="183" r="3"/><circle cx="418" cy="138" r="2"/></g>
<path class="beam laser-output" d="M634 159H735" stroke="#6dfcf7" stroke-width="15" opacity=".38" filter="url(#ls-glow)"/>
<path class="beam laser-output" d="M634 159H735" stroke="#92ffff" stroke-width="5"/>
<path id="ls-output-arrow" d="M722 151L739 159 722 167" stroke="#bfffff" stroke-width="3" fill="none"/>
<g fill="#b5d9e8" font-size="13" font-family="sans-serif" text-anchor="middle">
<text x="150" y="239">HR</text><text x="626" y="239">OC</text><text x="390" y="222">GAIN MEDIUM</text><text x="390" y="25" dx="76">PUMP</text><text x="698" y="141">OUTPUT</text>
</g>
</svg>
<p class="resonator-status" data-welcome-lang="en" lang="en" aria-live="off"><span id="ls-cavity-en">Plane-parallel</span> · <span id="ls-color-en">Red</span> · Artistic spectrum cycle</p>
<p class="resonator-status" data-welcome-lang="ar" lang="ar" dir="rtl" hidden><span id="ls-cavity-ar">المستوي المتوازي</span> · <span id="ls-color-ar">أحمر</span> · دورة ألوان فنية</p>
<p class="scene-caption" data-welcome-lang="en" lang="en" id="ls-geometry-en"></p>
<p class="scene-caption" data-welcome-lang="ar" lang="ar" dir="rtl" id="ls-geometry-ar" hidden></p>
<p class="scene-caption" data-welcome-lang="en" lang="en">Decorative synchronized pump/output colors · Not a live optical simulation</p>
<p class="scene-caption" data-welcome-lang="ar" lang="ar" dir="rtl" hidden>تزامن لوني جمالي بين الضخ والخرج · ليس محاكاة بصرية تشغيلية</p>
<div data-welcome-lang="en" lang="en" dir="ltr">
<h2 id="laserstone-welcome-title">Welcome to LASERSTONE™</h2>
<p>Where physics meets innovation, and research advances through evidence, responsible simulation and scientific integrity.</p>
<label for="laserstone-role-en">Your research field</label>
<select id="laserstone-role-en" class="welcome-role" data-role-select="en"><option value="general">Researcher</option><option value="laser">Laser physics</option><option value="photonics">Photonics</option><option value="solar">Photovoltaics</option><option value="materials">Materials science</option><option value="computational">Computational physics</option></select>
<p data-role-message="en" aria-live="polite">Welcome, researcher. Explore the scientific platform.</p>
<p class="welcome-founder"><strong>Founded and Developed by Dr. Abdelrahman A. Hagar</strong> · Founder &amp; Scientific Director</p>
<p class="scene-caption">Local preview · Independent scientific validation is not implied.</p>
</div>
<div data-welcome-lang="ar" lang="ar" dir="rtl" hidden>
<h2>مرحبًا بكم في LASERSTONE™</h2>
<p>حيث تلتقي الفيزياء بالابتكار، وتتقدم الأبحاث بالدليل والمحاكاة المسؤولة والأمانة العلمية.</p>
<label for="laserstone-role-ar">مجالك البحثي</label>
<select id="laserstone-role-ar" class="welcome-role" data-role-select="ar"><option value="general">باحث علمي</option><option value="laser">فيزياء الليزر</option><option value="photonics">الفوتونيات</option><option value="solar">الخلايا الشمسية</option><option value="materials">علم المواد</option><option value="computational">الفيزياء الحاسوبية</option></select>
<p data-role-message="ar" aria-live="polite">مرحبًا بك أيها الباحث، اكتشف عالمنا العلمي.</p>
<p class="welcome-founder"><strong>تأسست وطُوّرت على يد د. عبدالرحمن أ. حجر</strong> · المؤسس والمدير العلمي</p>
<p class="scene-caption">معاينة محلية · لا تعني التحقق العلمي المستقل.</p>
</div>
</div>
</section>
"""
    marker = '<div class="mission-content">'
    if html.count(marker) != 1:
        raise ValueError("Original shared page shell not found")
    html = html.replace(marker, marker + "\n" + welcome, 1)
    # Synchronize with the existing language selector without modifying original assets.
    lang_script = """document.addEventListener('DOMContentLoaded', () => {
  const selector = document.getElementById('language-select');
  const panels = document.querySelectorAll('[data-welcome-lang]');
  if (!selector || panels.length < 2) return;
  function updateWelcome() {
    const language = selector.value === 'ar' ? 'ar' : 'en';
    for (const panel of panels) panel.hidden = panel.dataset.welcomeLang !== language;
  }
  const messages = {
    en: {general:'Welcome, researcher. Explore the scientific platform.',laser:'Welcome, laser physicist. Explore gain, cavities and evidence.',photonics:'Welcome, photonics researcher. Explore light and optical systems.',solar:'Welcome, photovoltaics researcher. Explore solar modelling.',materials:'Welcome, materials researcher. Explore structure and optical response.',computational:'Welcome, computational physicist. Explore reproducible models.'},
    ar: {general:'مرحبًا بك أيها الباحث، اكتشف عالمنا العلمي.',laser:'مرحبًا بباحث فيزياء الليزر، اكتشف الكسب والتجاويف والأدلة.',photonics:'مرحبًا بباحث الفوتونيات، اكتشف الضوء والأنظمة البصرية.',solar:'مرحبًا بباحث الخلايا الشمسية، اكتشف النمذجة الكهروضوئية.',materials:'مرحبًا بباحث علم المواد، اكتشف البنية والاستجابة البصرية.',computational:'مرحبًا بباحث الفيزياء الحاسوبية، اكتشف النماذج القابلة لإعادة الإنتاج.'}
  };
  for (const select of document.querySelectorAll('[data-role-select]')) {
    select.addEventListener('change', () => {
      const lang = select.dataset.roleSelect;
      const target = document.querySelector('[data-role-message="' + lang + '"]');
      if (target) target.textContent = messages[lang][select.value] || messages[lang].general;
    });
  }
  // Decorative visualization only: cavity geometry does not determine emission wavelength.
  // L is the vertex separation; signed radii are expressed in units of L.
  // Curvature is exaggerated for legibility, not a ray-traced optical model.
  const cavityModes = [
    {r1:Infinity,r2:Infinity,en:'Plane-parallel',ar:'المستوي المتوازي'},
    {r1:0.5,r2:0.5,en:'Concentric',ar:'متحد المركز'},
    {r1:1,r2:1,en:'Confocal',ar:'متحد البؤرة'},
    {r1:Infinity,r2:1,en:'Hemispherical',ar:'نصف الكروي'},
    {r1:Infinity,r2:2,en:'Hemiconfocal',ar:'نصف متحد البؤرة'},
    {r1:1.5,r2:2,en:'General concave–concave',ar:'المقعر–المقعر العام'},
    {r1:0.8,r2:-2,en:'Concave–convex',ar:'المقعر–المحدب'}
  ];
  function mirrorPath(x, radius, side) {
    const sag = Number.isFinite(radius) ? side * 12 / radius : 0;
    return 'M'+(x+sag)+' 105 Q'+(x-sag)+' 158.5 '+(x+sag)+' 212';
  }
  function radiusLabel(r) { return Number.isFinite(r) ? String(r) : '∞'; }
  const spectrum = [
    ['#ff5252','Red','أحمر'],['#ff9d3d','Orange','برتقالي'],['#ffe15b','Yellow','أصفر'],
    ['#64ef9a','Green','أخضر'],['#56baff','Blue','أزرق'],['#6865ff','Indigo','نيلي'],['#bd6aff','Violet','بنفسجي']
  ];
  const hr = document.getElementById('ls-hr-mirror');
  const oc = document.getElementById('ls-oc-mirror');
  const reducedMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  let frame = 0;
  function renderResonator() {
    const mode = cavityModes[frame % cavityModes.length];
    const color = spectrum[(frame + Math.floor(frame / cavityModes.length)) % spectrum.length];
    const g = (1-1/mode.r1)*(1-1/mode.r2);
    const boundary = Math.abs(g)<1e-9 || Math.abs(g-1)<1e-9;
    const stable = g>0 && g<1;
    const formula = 'R₁/L = '+radiusLabel(mode.r1)+' · R₂/L = '+radiusLabel(mode.r2)+' · g₁g₂ = '+Number(g.toFixed(3));
    for (const [id, suffix] of [['ls-geometry-en',boundary?'Boundary case':stable?'Strict stability region':'Outside strict stability region'],['ls-geometry-ar',boundary?'حالة حدية':stable?'داخل نطاق الاستقرار الصارم':'خارج نطاق الاستقرار الصارم']]) {
      const node = document.getElementById(id); if (node) node.textContent = formula+' · '+suffix;
    }
    if (hr) hr.setAttribute('d', mirrorPath(150, mode.r1, 1));
    if (oc) oc.setAttribute('d', mirrorPath(626, mode.r2, -1));
    for (const node of document.querySelectorAll('.laser-output, .laser-pump')) node.setAttribute('stroke', color[0]);
    const arrow = document.getElementById('ls-output-arrow');
    if (arrow) arrow.setAttribute('stroke', color[0]);
    for (const [id,value] of [['ls-cavity-en',mode.en],['ls-cavity-ar',mode.ar],['ls-color-en',color[1]],['ls-color-ar',color[2]]]) {
      const node = document.getElementById(id);
      if (node) node.textContent = value;
    }
  }
  renderResonator();
  if (!reducedMotion) window.setInterval(() => {frame += 1; renderResonator();}, 3200);
  selector.addEventListener('change', updateWelcome);
  updateWelcome();
});
"""
    (TARGET / "welcome-language.js").write_text(lang_script, encoding="utf-8")
    html = html.replace("</head>", '<script src="./welcome-language.js" defer></script>\n</head>', 1)
    # The original preview remains unchanged. This local output forbids outbound connections.
    html = html.replace("<head>", '<head>\n<meta http-equiv="Content-Security-Policy" content="connect-src \'none\'; form-action \'none\'; object-src \'none\'; base-uri \'self\'">', 1)
    result = TARGET / "index.html"
    result.write_text(html, encoding="utf-8")
    return result

if __name__ == "__main__":
    result = build()
    print("Unified original preview design with local scientific evidence:", result)
    webbrowser.open(result.as_uri())
