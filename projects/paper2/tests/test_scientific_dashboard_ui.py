"""Synthetic tests for the Stage 4.1 read-only HTML dashboard."""
import importlib.util
from pathlib import Path
import sys
import unittest

root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root))
spec = importlib.util.spec_from_file_location("scientific_dashboard_ui", root / "scientific_dashboard_ui.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def report():
    return {"theory_id": "SYNTHETIC-1", "version": "0.1",
            "proposal_sha256": "synthetic-hash",
            "stages": {"unified": "NOT_RUN", "claims": "CLAIMS_NOT_AUTHORIZED"},
            "gaps": ["unified:NOT_RUN"], "scientific_validity": "NOT_ESTABLISHED",
            "publication_readiness": "NOT_ESTABLISHED", "endorsement": "NONE",
            "claims_authorized": []}


class DashboardUITests(unittest.TestCase):
    def test_identity_and_stages_rendered(self):
        html = mod.render(report())
        self.assertIn("SYNTHETIC-1", html)
        self.assertIn("CLAIMS_NOT_AUTHORIZED", html)

    def test_html_escaping_identity(self):
        r = report()
        r["theory_id"] = "<script>alert(1)</script>"
        html = mod.render(r)
        self.assertNotIn("<script>", html)
        self.assertIn("&lt;script&gt;", html)

    def test_html_escaping_gaps(self):
        r = report()
        r["gaps"] = ["<img src=x onerror=alert(1)>"]
        html = mod.render(r)
        self.assertNotIn("<img", html)

    def test_reject_promotion(self):
        r = report()
        r["scientific_validity"] = "VERIFIED"
        with self.assertRaises(ValueError):
            mod.render(r)

    def test_reject_authorized_claims(self):
        r = report()
        r["claims_authorized"] = ["claim-1"]
        with self.assertRaises(ValueError):
            mod.render(r)

    def test_reject_missing_fields(self):
        r = report()
        del r["stages"]
        with self.assertRaises(ValueError):
            mod.render(r)

    def test_reject_malformed_gaps(self):
        r = report()
        r["gaps"] = ["ok", {"unexpected": True}]
        with self.assertRaises(ValueError):
            mod.render(r)

    def test_no_gaps_still_disclaims_validation(self):
        r = report()
        r["gaps"] = []
        html = mod.render(r)
        self.assertIn("scientific verification is still outstanding", html)

if __name__ == "__main__":
    unittest.main()
