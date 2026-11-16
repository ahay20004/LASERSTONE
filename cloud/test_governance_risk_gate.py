import unittest
from cloud.governance.risk_gate import classify

class GovernanceRiskTests(unittest.TestCase):
    def test_workflow_changes_are_high_risk(self):
        result = classify([".github/workflows/huggingface-preview.yml"])
        self.assertEqual(result["risk_level"], "HIGH")
        self.assertFalse(result["auto_publish"])

    def test_scientific_entrypoint_is_high_risk(self):
        self.assertEqual(classify(["main.py"])["risk_level"], "HIGH")

    def test_static_changes_still_require_approval(self):
        result = classify(["cloud/site/index.html"])
        self.assertEqual(result["risk_level"], "MEDIUM")
        self.assertTrue(result["owner_decision_required"])

    def test_empty_change_never_grants_publication(self):
        result = classify([])
        self.assertEqual(result["risk_level"], "NONE")
        self.assertFalse(result["auto_publish"])

if __name__ == "__main__":
    unittest.main()
