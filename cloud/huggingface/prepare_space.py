"""Prepare an isolated Hugging Face static Space folder without publishing anything."""
from pathlib import Path
import argparse
import shutil
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
SITE = ROOT / "cloud" / "site"
README = Path(__file__).resolve().parent / "README.md"
ASSETS = ("index.html", "style.css", "i18n.js", "icon.svg", "manifest.webmanifest")
FORBIDDEN = ("_headers",)

def main():
    parser = argparse.ArgumentParser(description="Stage a static LASERSTONE Space (no upload).")
    parser.add_argument("--output", required=True, help="New or existing empty directory outside the source site")
    args = parser.parse_args()
    out = Path(args.output).expanduser().resolve()
    if out == SITE.resolve() or SITE.resolve() in out.parents or ROOT.resolve() == out:
        parser.error("Choose a separate staging directory.")
    if out.exists() and any(out.iterdir()):
        parser.error("Output directory must be empty to avoid overwriting other work.")
    out.mkdir(parents=True, exist_ok=True)
    for name in ASSETS:
        source = SITE / name
        if not source.is_file():
            parser.error(f"Missing source asset: {source}")
        shutil.copy2(source, out / name)
    # Build a public-only derivative. The original university source stays intact.
    html_path = out / "index.html"
    html = html_path.read_text(encoding="utf-8")
    html, count = re.subn(
        r'<section id="university-campus"\b.*?</section>',
        "", html, count=1, flags=re.DOTALL,
    )
    if count != 1:
        parser.error("Expected exactly one university section; refusing release")
    html = re.sub(r'<a\s+href="#university-campus"[^>]*>.*?</a>', "", html)
    html_path.write_text(html, encoding="utf-8")

    js_path = out / "i18n.js"
    js = js_path.read_text(encoding="utf-8")
    js = "".join(
        line for line in js.splitlines(keepends=True)
        if not re.match(r'\s*"(?:navCampus|missionCampus|campus[A-Za-z0-9]+)"\s*:', line)
    )
    js_path.write_text(js, encoding="utf-8")

    css_path = out / "style.css"
    css = css_path.read_text(encoding="utf-8")
    # University CSS consists of ordinary flat selector blocks. Fail closed
    # if the expected shape changes; never publish an unreviewed CSS variant.
    css = re.sub(r'/\* University campus:.*?\*/', "", css, flags=re.DOTALL)
    css = re.sub(
        r'([^{}]+)\{([^{}]*)\}',
        lambda m: "" if re.search(r'\.campus-[\w-]+', m.group(1)) else m.group(0),
        css,
    )
    css_path.write_text(css, encoding="utf-8")

    private_markers = {
        "index.html": ("university-campus", "navCampus", "missionCampus", "campus-building"),
        "i18n.js": ("navCampus", "missionCampus", "campusTitle", "campusB1", "campusD7"),
        "style.css": (".campus-sky", ".campus-building", ".campus-section"),
    }
    leaks = [
        f"{name}: {marker}"
        for name, markers in private_markers.items()
        for marker in markers
        if marker in (out / name).read_text(encoding="utf-8")
    ]
    if leaks:
        parser.error("Owner-only university content in staged public preview: " + "; ".join(leaks))
    shutil.copy2(README, out / "README.md")
    print(f"Prepared {out} with {len(ASSETS)} public assets and Space README.")
    print("Not deployed. Review staged contents and IP/security clearance before upload.")
    print("Note: provider-specific HTTP headers from _headers are NOT applied by this static Space.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
