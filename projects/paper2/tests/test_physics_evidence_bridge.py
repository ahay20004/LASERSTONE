"""Synthetic bridge tests; classification is not experimental verification."""
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("physics_evidence_bridge", ROOT / "physics_evidence_bridge.py")
bridge = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bridge)

class BridgeTests(unittest.TestCase):
    def test_derived_photon_energy_does_not_authorize_gain(self):
        result = bridge.classify({"photon_energy_ev": 1.96, "frequency_hz": 4.74e14})
        self.assertEqual(result["status"], "CLASSIFIED_NOT_VERIFIED")
        self.assertEqual(result["g3_evidence_types"], [])
        self.assertEqual(result["claims_authorized"], [])
        self.assertTrue(all(o["kind"] == bridge.PHYSICS_DERIVED for o in result["outputs"]))

    def test_heuristic_score_is_not_measurement(self):
        result = bridge.classify({"gain_score": 99, "consistency_score": 100})
        self.assertTrue(all(o["kind"] == bridge.HEURISTIC_SCORE for o in result["outputs"]))
        self.assertEqual(result["g3_evidence_types"], [])

    def test_mixed_output_remains_unverified(self):
        result = bridge.classify({"photon_energy_ev": 2.0, "gain_score": 100})
        self.assertEqual({o["kind"] for o in result["outputs"]},
                         {bridge.PHYSICS_DERIVED, bridge.HEURISTIC_SCORE})
        self.assertEqual(result["claims_authorized"], [])

    def test_cannot_inject_experimental_evidence(self):
        with self.assertRaises(ValueError):
            bridge.classify({"measured_optical_gain": 1.2})

    def test_cannot_inject_claim_approval(self):
        with self.assertRaises(ValueError):
            bridge.classify({"laser_threshold_verified": True})

    def test_reject_non_mapping(self):
        with self.assertRaises(ValueError):
            bridge.classify(["gain_score", 100])

if __name__ == "__main__":
    unittest.main()
