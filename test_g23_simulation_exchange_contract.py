"""Contract tests using synthetic values, not SCAPS-1D execution."""
import unittest
import copy
from pathlib import Path
import tempfile
from unittest.mock import patch
from g23_simulation_exchange_contract import validate_simulation_envelope, inspect_simulator_runtimes


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

    def test_unhashable_simulator_is_rejected_without_exception(self):
        for value in ([], {}, True, None):
            with self.subTest(value=value):
                self.case["simulator"] = value
                self.assertFalse(validate_simulation_envelope(self.case)["valid"])

    def test_inventory_absent_from_path_never_claims_readiness(self):
        with patch("shutil.which", return_value=None), patch("subprocess.Popen") as launch:
            report = inspect_simulator_runtimes()
        launch.assert_not_called()
        self.assertFalse(report["all_simulators_ready"])
        self.assertEqual(report["simulators"]["matlab"]["availability"], "NOT_FOUND_ON_PATH")
        for entry in report["simulators"].values():
            self.assertEqual(entry["simulation_execution"], "NOT_TESTED")
            self.assertEqual(entry["integration_status"], "NOT_VERIFIED")

    def test_explicit_file_does_not_prove_simulator_execution(self):
        with tempfile.TemporaryDirectory() as directory:
            executable = Path(directory) / "matlab.exe"
            executable.write_bytes(b"synthetic file, not a simulator")
            config = {"matlab": str(executable)}
            snapshot = copy.deepcopy(config)
            with patch("shutil.which", return_value=None), patch("subprocess.Popen") as launch:
                report = inspect_simulator_runtimes(config)
            launch.assert_not_called()
            self.assertEqual(config, snapshot)
            self.assertEqual(report["simulators"]["matlab"]["availability"], "EXPLICIT_FILE_FOUND")
            self.assertFalse(report["all_simulators_ready"])
            executable.unlink()
            with patch("shutil.which", return_value=None):
                missing = inspect_simulator_runtimes(config)
            self.assertEqual(missing["simulators"]["matlab"]["availability"], "EXPLICIT_PATH_MISSING")

    def test_inventory_rejects_invalid_configuration(self):
        for config in ([], {"unknown": "tool"}, {"python": "tool"},
                       {"matlab": ""}, {"matlab": None}):
            with self.subTest(config=config), self.assertRaises(ValueError):
                inspect_simulator_runtimes(config)

    def test_path_discovery_remains_inventory_only(self):
        with patch("shutil.which", return_value="/synthetic/tool"):
            report = inspect_simulator_runtimes()
        self.assertEqual(report["status"], "INVENTORY_ONLY")
        self.assertEqual(report["simulators"]["comsol"]["availability"], "PATH_FOUND")
        self.assertFalse(report["all_simulators_ready"])


if __name__ == "__main__":
    unittest.main()

