"""Static, dependency-free checks for the LASERSTONE bilingual public preview."""
from html.parser import HTMLParser
from pathlib import Path
import json
import re
import unittest
import subprocess
import sys
import tempfile

SITE = Path(__file__).resolve().parent / "site"

class Markup(HTMLParser):
    def __init__(self):
        super().__init__()
        self.keys = []
        self.languages = []
        self.references = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "data-i18n" in attrs:
            self.keys.append(attrs["data-i18n"])
        if tag == "option" and "value" in attrs:
            self.languages.append(attrs["value"])
        if tag in ("script", "link", "img"):
            self.references.extend(v for k,v in attrs.items() if k in ("src","href") and v and v.startswith("./"))

class PreviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = (SITE / "index.html").read_text(encoding="utf-8")
        cls.js = (SITE / "i18n.js").read_text(encoding="utf-8")
        cls.markup = Markup()
        cls.markup.feed(cls.html)
        match = re.search(r"const translations\s*=\s*(\{.*?\})\s*;\s*const supported", cls.js, re.S)
        if match is None:
            raise AssertionError("Translations dictionary not found")
        cls.messages = json.loads(match.group(1))

    def test_only_arabic_english(self):
        self.assertEqual(set(self.messages), {"en", "ar"})
        self.assertEqual(set(self.markup.languages), {"en", "ar"})
        self.assertEqual(len(self.markup.languages), 2)

    def test_translation_coverage(self):
        self.assertEqual(set(self.messages["en"]), set(self.messages["ar"]))
        for lang in ("en", "ar"):
            for key in self.markup.keys:
                self.assertTrue(self.messages[lang].get(key), f"{lang}: missing {key}")

    def test_static_assets(self):
        for ref in self.markup.references:
            self.assertTrue((SITE / ref).is_file(), f"Missing: {ref}")
        manifest = json.loads((SITE / "manifest.webmanifest").read_text(encoding="utf-8"))
        self.assertTrue(manifest["name"])
        for icon in manifest["icons"]:
            self.assertTrue((SITE / icon["src"]).is_file())

    def test_security_headers(self):
        headers = (SITE / "_headers").read_text(encoding="utf-8")
        self.assertIn("default-src 'none'", headers)
        self.assertIn("script-src 'self'", headers)
        self.assertIn("frame-ancestors 'none'", headers)

    def test_cockpit_is_explicitly_non_live(self):
        for anchor in ('id="cockpit"', 'id="research"', 'id="integrity"', 'id="access"'):
            self.assertIn(anchor, self.html)
        for lang in ("en", "ar"):
            for key in ("cockpitTitle", "cockpitFootnote", "statusDisconnected", "statusRestricted"):
                self.assertTrue(self.messages[lang].get(key), f"{lang}: missing {key}")
        self.assertIn("No live telemetry", self.messages["en"]["cockpitFootnote"])
        self.assertIn("غير متصل", self.messages["ar"]["statusDisconnected"])

    def test_no_external_script_or_form_actions(self):
        self.assertNotRegex(self.html, r'(?i)<script[^>]+src=["\\\']https?://')
        self.assertNotRegex(self.html, r'(?i)<form\b')
        self.assertNotRegex(self.html, r'(?i)<iframe\b')
        self.assertNotRegex(self.js, r'(?i)\b(fetch|XMLHttpRequest|WebSocket|sendBeacon)\s*\(')

    def test_staging_has_only_approved_public_assets(self):
        script = SITE.parent / "huggingface" / "prepare_space.py"
        allowed = {"README.md", "index.html", "style.css", "i18n.js", "icon.svg", "manifest.webmanifest"}
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "preview"
            subprocess.run([sys.executable, str(script), "--output", str(target)],
                           check=True, capture_output=True, text=True)
            self.assertEqual({p.name for p in target.iterdir()}, allowed)
            self.assertFalse((target / "_headers").exists())
            self.assertFalse(any(p.is_dir() for p in target.iterdir()))

    def test_security_headers_are_not_claimed_as_deployed(self):
        # These headers are a source template, not enforced by the static HF Space.
        script = (SITE.parent / "huggingface" / "prepare_space.py").read_text(encoding="utf-8")
        self.assertIn('ASSETS = ("index.html", "style.css", "i18n.js", "icon.svg", "manifest.webmanifest")', script)
        self.assertIn("NOT applied by this static Space", script)

    def test_cockpit_controls_are_accessible_and_non_operational(self):
        from html.parser import HTMLParser
        class Buttons(HTMLParser):
            def __init__(self):
                super().__init__()
                self.panels = []
            def handle_starttag(self, tag, attrs):
                if tag == "button":
                    attrs = dict(attrs)
                    if "data-panel" in attrs:
                        self.panels.append(attrs)
        buttons = Buttons()
        buttons.feed(self.html)
        self.assertEqual({p["data-panel"] for p in buttons.panels},
                         {"evidence", "physics", "solar", "owner"})
        self.assertEqual(len(buttons.panels), 4)
        for panel in buttons.panels:
            self.assertEqual(panel.get("type"), "button")
            self.assertEqual(panel.get("aria-pressed"), "false")
            self.assertEqual(panel.get("aria-controls"), "cockpit-readout")
        self.assertIn('id="cockpit-readout"', self.html)
        self.assertIn('aria-live="polite"', self.html)
        self.assertIn("selectedPanel = button.dataset.panel === selectedPanel ? null", self.js)
        self.assertIn("updateReadout(document.documentElement.lang)", self.js)
        self.assertIn("updateReadout(chosen)", self.js)
        for lang in ("en", "ar"):
            for key in ("selectPanel", "readoutIdle", "readoutIdleDesc",
                        "readoutEvidence", "readoutPhysics", "readoutSolar", "readoutOwner"):
                self.assertTrue(self.messages[lang].get(key), f"{lang}: missing {key}")

    def test_no_private_login_claims(self):
        self.assertNotIn('type="password"', self.html)
        self.assertNotIn("<form", self.html.lower())
        self.assertIn("No account details are collected", self.html)

if __name__ == "__main__":
    unittest.main()
