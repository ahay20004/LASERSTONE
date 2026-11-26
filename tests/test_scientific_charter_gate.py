import unittest
from scientific_charter_gate import assess, PATHWAYS, REQUIRED

class CharterGateTests(unittest.TestCase):
    def fixture(self):
        return dict(module_id="synthetic", quantity_ids=["frequency"],
                    equation_ids=["vacuum_frequency"], sources=["synthetic reference"],
                    validity_domain="positive wavelength", uncertainty_status="not assessed",
                    evidence_status="synthetic", test_references=["synthetic test"],
                    pathways={p: {"status":"documented", "detail":"synthetic description"}
                              for p in PATHWAYS})

    def test_complete_is_not_validation(self):
        result = assess(self.fixture())
        self.assertEqual(result["status"], "DOCUMENTATION_COMPLETE")
        self.assertFalse(result["scientific_validation"])
        self.assertFalse(result["release_authorized"])

    def test_missing_fields(self):
        for key in REQUIRED + ("pathways",):
            with self.subTest(key=key):
                m = self.fixture()
                del m[key]
                self.assertEqual(assess(m)["status"], "INCOMPLETE")

    def test_pathway_justification(self):
        m = self.fixture()
        m["pathways"]["student"] = {"status":"not_applicable", "detail":""}
        self.assertEqual(assess(m)["status"], "INCOMPLETE")
        m["pathways"]["student"]["detail"] = "Synthetic internal-only fixture"
        self.assertEqual(assess(m)["status"], "DOCUMENTATION_COMPLETE")
