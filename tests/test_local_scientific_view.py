import unittest
from local_scientific_bridge import evaluate_synthetic_case
from local_scientific_view import render

class LocalScientificViewTests(unittest.TestCase):
    def test_synthetic_view_has_evidence_boundary(self):
        page = render(evaluate_synthetic_case())
        self.assertIn("SYNTHETIC DEMONSTRATION ONLY", page)
        self.assertIn("No network requests", page)
        self.assertIn("physics_consistency_engine", page)
        self.assertIn("100", page)
        self.assertIn("connect-src 'none'", page)

    def test_real_data_is_rejected(self):
        report = evaluate_synthetic_case()
        report["input_kind"] = "MEASURED"
        with self.assertRaises(ValueError):
            render(report)

if __name__ == "__main__":
    unittest.main()
