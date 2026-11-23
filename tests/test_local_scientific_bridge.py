import unittest
from local_scientific_bridge import evaluate_synthetic_case

class LocalScientificBridgeTests(unittest.TestCase):
    def test_real_engine_called_with_synthetic_inputs(self):
        report = evaluate_synthetic_case()
        self.assertEqual(report["output"]["consistency_score"], 100)
        self.assertEqual(report["output"]["classification"], "Highly Consistent")
        self.assertEqual(report["input_kind"], "SYNTHETIC_DEMONSTRATION")
        self.assertFalse(report["independent_scientific_validation"])
        self.assertFalse(report["public_deployment_authorized"])

if __name__ == "__main__":
    unittest.main()
