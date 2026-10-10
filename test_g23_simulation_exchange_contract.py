"""Contract tests using synthetic values, not SCAPS-1D execution."""
import unittest
from g23_simulation_exchange_contract import validate_simulation_envelope


class SimulationExchangeTests(unittest.TestCase):
    def setUp(self):
        self.case = {
            "simulator": "scaps-1d", "simulator_version": "unverified",
            "model_id": "synthetic-device", "run_id": "synthetic-001",
            "inputs": {"temperature": {"value": 300.0, "unit": "K"}},
            "outputs": {"voc": {"value": 0.7, "unit": "V"}},
            "conditions": {"illumination": "synthetic example"},
            "provenance": {"origin": "synthetic test only"},
        }

    def test_valid_synthetic_envelope(self):
        self.assertTrue(validate_simulation_envelope(self.case)["valid"])

    def test_missing_provenance_rejected(self):
        del self.case["provenance"]
        self.assertFalse(validate_simulation_envelope(self.case)["valid"])

    def test_missing_unit_rejected(self):
        del self.case["outputs"]["voc"]["unit"]
        self.assertFalse(validate_simulation_envelope(self.case)["valid"])

    def test_nonfinite_output_rejected(self):
        self.case["outputs"]["voc"]["value"] = float("nan")
        self.assertFalse(validate_simulation_envelope(self.case)["valid"])

    def test_unknown_simulator_rejected(self):
        self.case["simulator"] = "unknown"
        self.assertFalse(validate_simulation_envelope(self.case)["valid"])


if __name__ == "__main__":
    unittest.main()
