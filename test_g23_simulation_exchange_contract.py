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




class MatlabFileExchangeTests(unittest.TestCase):
    def test_round_trip_history_and_rejections(self):
        import json
        import subprocess
        import sys
        import g23_simulation_exchange_contract as m
        with tempfile.TemporaryDirectory() as root:
            exported = m.export_matlab_request(root, 'G23-MATLAB-002')
            request_path = Path(exported['request'])
            request = m._read_json(request_path)
            self.assertNotIn('outputs', request)
            self.assertFalse(Path(exported['expected_result']).exists())
            before = request_path.read_bytes()
            with self.assertRaises(FileExistsError):
                m.export_matlab_request(root, request['run_id'])
            self.assertEqual(before, request_path.read_bytes())
            result = {k: copy.deepcopy(request[k]) for k in ('simulator', 'model_id', 'run_id', 'request_token', 'inputs', 'conditions')}
            result.update(simulator_version='26.2.0.3386108 (R2026b)', provenance={'origin': 'synthetic fixture, no MATLAB execution'}, outputs={'frequency': {'value': 299792458 / request['inputs']['wavelength']['value'], 'unit': 'Hz'}})
            report = m.verify_matlab_result(request, result)
            self.assertTrue(report['valid'])
            self.assertEqual(report['physical_validation'], 'NOT_ESTABLISHED')
            for key, value in [('run_id', 'other'), ('request_token', 'other'), ('model_id', 'other'), ('simulator', 'python'), ('conditions', {'medium': 'air'}), ('inputs', {'wavelength': {'value': 621e-9, 'unit': 'm'}})]:
                bad = copy.deepcopy(result)
                bad[key] = value
                with self.subTest(key=key):
                    self.assertFalse(m.verify_matlab_result(request, bad)['valid'])
            for value, unit in [(1, 'Hz'), (True, 'Hz'), (float('nan'), 'Hz'), (float('inf'), 'Hz'), (result['outputs']['frequency']['value'], 'THz')]:
                bad = copy.deepcopy(result)
                bad['outputs']['frequency'] = {'value': value, 'unit': unit}
                with self.subTest(value=value, unit=unit):
                    self.assertFalse(m.verify_matlab_result(request, bad)['valid'])
            result_path = Path(exported['expected_result'])
            result_path.write_text(json.dumps(result))
            result_before = result_path.read_bytes()
            first = m.import_matlab_result(request_path, result_path)
            second = m.import_matlab_result(request_path, result_path)
            self.assertNotEqual(first['report_path'], second['report_path'])
            self.assertEqual(before, request_path.read_bytes())
            self.assertEqual(result_before, result_path.read_bytes())
            cli = [sys.executable, m.__file__, '--verify-matlab', '--request', str(request_path), '--result', str(result_path)]
            self.assertEqual(subprocess.run(cli, capture_output=True).returncode, 0)
            result['run_id'] = 'other'
            result_path.write_text(json.dumps(result))
            self.assertEqual(subprocess.run(cli, capture_output=True).returncode, 1)

    def test_export_invalid_inputs_and_strict_json(self):
        import g23_simulation_exchange_contract as m
        with tempfile.TemporaryDirectory() as root:
            for value in ('../escape', '/absolute', 'x/y'):
                with self.subTest(run=value), self.assertRaises(ValueError):
                    m.export_matlab_request(root, value)
            for value in (True, 0, -1, float('nan'), float('inf'), 1e-320):
                with self.subTest(wavelength=value), self.assertRaises(ValueError):
                    m.export_matlab_request(root, wavelength_nm=value)
            bad = Path(root) / 'bad.json'
            for content in ('{"x":1,"x":2}', '{"x":NaN}', '{', ' ' * 1048577):
                bad.write_text(content)
                with self.subTest(size=len(content)), self.assertRaises(ValueError):
                    m._read_json(bad)

    def test_cli_export_inventory_and_argument_errors(self):
        import json
        import subprocess
        import sys
        import g23_simulation_exchange_contract as m
        with tempfile.TemporaryDirectory() as root:
            cli = [sys.executable, m.__file__]
            exported = subprocess.run(cli + ['--export-matlab', '--output-root', root, '--run-id', 'cli-run'], capture_output=True, text=True)
            self.assertEqual(exported.returncode, 0, exported.stdout + exported.stderr)
            self.assertTrue(Path(json.loads(exported.stdout)['matlab_script']).exists())
            inventory = subprocess.run(cli + ['--inventory'], capture_output=True, text=True)
            self.assertEqual(inventory.returncode, 0)
            self.assertFalse(json.loads(inventory.stdout)['all_simulators_ready'])
            bad = subprocess.run(cli + ['--inventory', '--run-id', 'ignored'], capture_output=True)
            self.assertEqual(bad.returncode, 1)


if __name__ == "__main__":
    unittest.main()
