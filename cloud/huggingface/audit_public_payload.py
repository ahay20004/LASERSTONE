"""Fail-closed inspection of the exact static public staging payload (not a legal/IP clearance)."""
from pathlib import Path
import argparse
import re

ALLOWED = frozenset({"README.md", "index.html", "style.css", "i18n.js", "icon.svg", "manifest.webmanifest"})
DANGEROUS = (
    ("private key", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----", re.I)),
    ("credential assignment", re.compile(r"""(?i)\b(?:HF_TOKEN|GITHUB_TOKEN|AWS_SECRET_ACCESS_KEY|PRIVATE_API_KEY)\s*[:=]\s*['"][^'"]{8,}""")),
    ("local Windows path", re.compile(r"(?i)[A-Z]:\\(?:Users|Documents and Settings)\\")),
    ("local POSIX home", re.compile(r"""(?i)/(?:home|Users)/[^/\s'"<>]+/""")),
    ("external executable script", re.compile(r"""(?is)<script\b[^>]*\bsrc\s*=\s*['"]https?://""")),
    ("embedded iframe", re.compile(r"(?is)<iframe\b")),
)

def inspect(folder):
    folder = Path(folder)
    if not folder.is_dir():
        raise ValueError("Missing staged public payload")
    names = {p.name for p in folder.iterdir()}
    issues = []
    if names != ALLOWED:
        issues.append(f"Public allowlist mismatch: {sorted(names ^ ALLOWED)}")
    for p in folder.iterdir():
        if p.is_symlink() or not p.is_file():
            issues.append(f"Not a regular public asset: {p.name}")
            continue
        if p.stat().st_size > 750_000:
            issues.append(f"Oversized public asset requiring review: {p.name}")
        try:
            content = p.read_text(encoding="utf-8")
        except UnicodeError:
            issues.append(f"Non-UTF-8 public asset: {p.name}")
            continue
        for label, pattern in DANGEROUS:
            if pattern.search(content):
                issues.append(f"{p.name}: {label}")
    return issues

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("folder")
    args = parser.parse_args()
    problems = inspect(args.folder)
    if problems:
        for issue in problems:
            print("BLOCK:", issue)
        raise SystemExit(1)
    print("PASS: static public payload automated checks; manual security, privacy, IP and hosting review still required.")

if __name__ == "__main__":
    main()
