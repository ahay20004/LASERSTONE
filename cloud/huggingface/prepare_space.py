"""Prepare an isolated Hugging Face static Space folder without publishing anything."""
from pathlib import Path
import argparse
import shutil
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
    shutil.copy2(README, out / "README.md")
    print(f"Prepared {out} with {len(ASSETS)} public assets and Space README.")
    print("Not deployed. Review staged contents and IP/security clearance before upload.")
    print("Note: provider-specific HTTP headers from _headers are NOT applied by this static Space.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
