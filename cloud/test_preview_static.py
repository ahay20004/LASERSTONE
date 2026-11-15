"""Static, dependency-free checks for the LASERSTONE bilingual public preview."""
from html.parser import HTMLParser
from pathlib import Path
import json
import re
import unittest

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

    def test_no_private_login_claims(self):
        self.assertNotIn('type="password"', self.html)
        self.assertNotIn("<form", self.html.lower())
        self.assertIn("No account details are collected", self.html)

if __name__ == "__main__":
    unittest.main()
