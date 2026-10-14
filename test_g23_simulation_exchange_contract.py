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


class ScapsInvocationTests(unittest.TestCase):
    def test_explicit_launch_uses_argument_list_and_never_claims_simulation(self):
        import hashlib
        import subprocess
        import g23_simulation_exchange_contract as m
        from unittest.mock import MagicMock
        with tempfile.TemporaryDirectory() as folder:
            executable = Path(folder) / 'scaps3312.exe'
            content = b'MZ synthetic test fixture, not an actual executable'
            executable.write_bytes(content)
            process = MagicMock(pid=123)
            process.poll.return_value = None
            with patch('platform.system', return_value='Windows'), \
                    patch('subprocess.run', return_value=subprocess.CompletedProcess([], 0, stdout='INFO: No tasks match', stderr='')) as inventory, \
                    patch('subprocess.Popen', return_value=process) as launch:
                report = m.launch_scaps_gui(str(executable))
            launch.assert_called_once_with([str(executable.resolve())], cwd=str(executable.parent.resolve()), shell=False)
            self.assertEqual(inventory.call_args.args[0], ['tasklist.exe', '/FI', 'IMAGENAME eq scaps3312.exe', '/FO', 'CSV', '/NH'])
            self.assertEqual(report['sha256'], hashlib.sha256(content).hexdigest())
            self.assertEqual(report['status'], 'PROCESS_STARTED')
            self.assertEqual(report['simulation_execution'], 'NOT_TESTED')
            self.assertEqual(report['physical_validation'], 'NOT_ESTABLISHED')
            self.assertEqual(report['result_import'], 'NOT_REQUESTED')
            self.assertEqual(executable.read_bytes(), content)

    def test_existing_image_name_blocks_duplicate_launch_without_claiming_path_match(self):
        import subprocess
        import g23_simulation_exchange_contract as m
        with tempfile.TemporaryDirectory() as folder:
            executable = Path(folder) / 'scaps3312.exe'
            executable.write_bytes(b'MZ fixture')
            listing = '"scaps3312.exe","456","Console","1","100 K"\n'
            with patch('platform.system', return_value='Windows'), \
                    patch('subprocess.run', return_value=subprocess.CompletedProcess([], 0, stdout=listing, stderr='')), \
                    patch('subprocess.Popen') as launch:
                report = m.launch_scaps_gui(executable)
            launch.assert_not_called()
            self.assertEqual(report['status'], 'IMAGE_NAME_ALREADY_RUNNING')
            self.assertEqual(report['process_ids'], [456])
            self.assertFalse(report['new_process_started'])
            self.assertEqual(report['existing_process_path'], 'NOT_VERIFIED')

    def test_failed_process_listing_never_launches(self):
        import subprocess
        import g23_simulation_exchange_contract as m
        with tempfile.TemporaryDirectory() as folder:
            executable = Path(folder) / 'scaps3312.exe'
            executable.write_bytes(b'MZ fixture')
            with patch('platform.system', return_value='Windows'), \
                    patch('subprocess.run', side_effect=subprocess.TimeoutExpired('tasklist.exe', 10)), \
                    patch('subprocess.Popen') as launch:
                with self.assertRaises(subprocess.TimeoutExpired):
                    m.launch_scaps_gui(executable)
            launch.assert_not_called()

    def test_windows_active_root_and_binary_gates(self):
        import g23_simulation_exchange_contract as m
        with patch('platform.system', return_value='Linux'), patch('subprocess.Popen') as launch:
            with self.assertRaisesRegex(ValueError, 'requires Windows'):
                m.launch_scaps_gui('missing')
            launch.assert_not_called()
        with tempfile.TemporaryDirectory() as folder:
            executable = Path(folder) / 'scaps3312.exe'
            executable.write_bytes(b'not a Windows binary')
            with patch('platform.system', return_value='Windows'), patch('subprocess.Popen') as launch:
                with self.assertRaisesRegex(ValueError, 'absolute'):
                    m.launch_scaps_gui('scaps3312.exe')
                with self.assertRaisesRegex(ValueError, 'header'):
                    m.launch_scaps_gui(executable)
                with patch.object(m.Path, 'cwd', return_value=Path(folder)):
                    with self.assertRaisesRegex(ValueError, 'active project root'):
                        m.launch_scaps_gui(executable)
            launch.assert_not_called()

    def test_cli_arguments_and_early_exit_failures(self):
        import io
        import json
        import sys
        import g23_simulation_exchange_contract as m
        from contextlib import redirect_stdout
        cases = [(['--launch-scaps'], None),
                 (['--launch-scaps', '--executable', 'matlab=x'], None),
                 (['--launch-scaps', '--executable', 'scaps-1d=x', '--run-id', 'unused'], None),
                 (['--launch-scaps', '--executable', 'scaps-1d=x'], {'status': 'PROCESS_EXITED_EARLY', 'exit_code': 1})]
        for args, result in cases:
            stream = io.StringIO()
            with self.subTest(args=args), patch.object(sys, 'argv', [m.__file__] + args), \
                    patch.object(m, 'launch_scaps_gui', return_value=result) as launch, redirect_stdout(stream):
                self.assertEqual(m._main(), 1)
            if result is None:
                launch.assert_not_called()
                self.assertEqual(json.loads(stream.getvalue())['status'], 'ERROR')
            else:
                launch.assert_called_once_with('x')



class SavedScapsIvTests(unittest.TestCase):
    # Synthetic format fixture only; these numbers are not a physics benchmark.
    sample = """SCAPS 3.3.12 ELIS-UGent: Version scaps3312.exe, dated synthetic
Simulation of I-V curves
Single shot simulation # 1
Calculation started : 14-10-2026 at 9:00:00
problem definition file : synthetic-device.def
Calculation under illumination
spectrum file :
synthetic-spectrum.spe  last saved: synthetic
Transmission of ND filter: 1.0000e+00
Incident power on solar cell structure 100.0000 mW/cm2
Temperature 300.00 K
Workpoint bias voltage 0.0000 Volt
Frequency 1.0000e+06 Hz
Voltage reference convention: synthetic fixture
Current reference convention: synthetic fixture
Power generated by the cell: = -V*I; synthetic fixture
v(V) jtot(mA/cm2) jbulk(mA/cm2)
0.0 -10.0 1.0
0.5 -5.0 2.0
1.0 1.0 3.0
solar cell parameters deduced from calculated IV-curve:
Voc = 0.9 Volt
Jsc = 10.0 mA/cm2
FF = 50.0 %
eta = 4.5 %
V_MPP = 0.5 Volt
J_MPP = 9.0 mA/cm2
"""

    def test_all_runs_and_origins_are_preserved(self):
        import g23_simulation_exchange_contract as m
        second = self.sample.replace('# 1', '# 2').replace('9:00:00', '10:00:00')
        runs = m.parse_scaps_iv(self.sample + '\n' + second)
        self.assertEqual([r['single_shot_number'] for r in runs], [1, 2])
        self.assertEqual(runs[0]['curve']['rows'][0], [0.0, -10.0, 1.0])
        self.assertEqual(runs[0]['curve']['value_origin'], 'SIMULATED')
        self.assertEqual(runs[0]['outputs']['jsc']['value_origin'], 'SCAPS_DERIVED_FROM_SIMULATED_IV')
        self.assertEqual(runs[0]['conditions']['incident_power_si']['value'], 1000)
        self.assertEqual(runs[0]['physical_validation'], 'NOT_ESTABLISHED')
        self.assertEqual(runs[0]['solver_convergence'], 'NOT_ESTABLISHED_FROM_IV_EXPORT')
        self.assertFalse(runs[0]['definition_file_verified'])

    def test_incomplete_final_run_and_wrong_kind_are_not_silently_skipped(self):
        import g23_simulation_exchange_contract as m
        for data in (self.sample + '\nSCAPS 3.3.12 incomplete',
                     self.sample.replace('Simulation of I-V curves', 'Spatial profile'),
                     self.sample.replace('J_MPP = 9.0 mA/cm2', ''),
                     self.sample.replace('0.5 -5.0 2.0', '0.5 -5.0')):
            with self.subTest(data=data), self.assertRaises(ValueError):
                m.parse_scaps_iv(data)

    def test_nonfinite_units_and_duplicate_headers_are_rejected(self):
        import g23_simulation_exchange_contract as m
        for old, new in [('0.5 -5.0 2.0', '0.5 NaN 2.0'),
                         ('Jsc = 10.0 mA/cm2', 'Jsc = 10.0 A/cm2'),
                         ('Temperature 300.00 K', 'Temperature 300.00 C'),
                         ('eta = 4.5 %', 'eta = 4.5 %\neta = 5.5 %'),
                         ('jbulk(mA/cm2)', 'jbulk(V)'),
                         ('problem definition file : synthetic-device.def', 'problem definition file :'),
                         ('100.0000 mW/cm2', '1e308 mW/cm2')]:
            with self.subTest(old=old), self.assertRaises(ValueError):
                m.parse_scaps_iv(self.sample.replace(old, new))

    def test_duplicate_blocks_rejected_without_auto_selection(self):
        import g23_simulation_exchange_contract as m
        with self.assertRaisesRegex(ValueError, 'Duplicate SCAPS run block'):
            m.parse_scaps_iv(self.sample + self.sample)

    def test_convergence_message_requires_review_without_changing_values(self):
        import g23_simulation_exchange_contract as m
        result = m.parse_scaps_iv(self.sample + 'convergence failure\n')[0]
        self.assertEqual(result['status'], 'REVIEW_REQUIRED')
        self.assertEqual(result['outputs']['efficiency']['value'], 4.5)
        self.assertTrue(result['warnings'])

    def test_reversed_scan_is_reported_without_silent_sorting(self):
        import g23_simulation_exchange_contract as m
        result = m.parse_scaps_iv(self.sample.replace('0.0 -10.0 1.0\n0.5 -5.0 2.0\n1.0 1.0 3.0',
                             '1.0 1.0 3.0\n0.5 -5.0 2.0\n0.0 -10.0 1.0'))[0]
        self.assertEqual(result['curve']['rows'][0][0], 1.0)
        self.assertEqual(result['status'], 'REVIEW_REQUIRED')

    def test_file_and_cli_inspection_preserve_source_and_write_no_reports(self):
        import hashlib
        import json
        import subprocess
        import sys
        import g23_simulation_exchange_contract as m
        with tempfile.TemporaryDirectory(dir=Path(m.__file__).parent) as folder:
            source = Path(folder) / 'synthetic.iv'
            data = self.sample.replace('\n', '\r\n').encode()
            source.write_bytes(data)
            before = sorted(Path(folder).iterdir())
            report = m.inspect_scaps_iv(source)
            self.assertEqual(report['source']['sha256'], hashlib.sha256(data).hexdigest())
            self.assertFalse(report['new_simulation_executed'])
            self.assertEqual(report['run_count'], 1)
            cli = subprocess.run([sys.executable, '-B', m.__file__, '--inspect-scaps-iv', '--result', str(source)],
                                 cwd=Path(m.__file__).parent, capture_output=True, text=True)
            self.assertEqual(cli.returncode, 0, cli.stderr + cli.stdout)
            exported = json.loads(cli.stdout)
            self.assertNotIn('rows', exported['runs'][0]['curve'])
            self.assertEqual(exported['runs'][0]['curve']['point_count'], 3)
            self.assertEqual(source.read_bytes(), data)
            self.assertEqual(sorted(Path(folder).iterdir()), before)

    def test_source_must_be_explicit_active_and_nonhistorical(self):
        import g23_simulation_exchange_contract as m
        with tempfile.TemporaryDirectory() as outside:
            source = Path(outside) / 'synthetic.iv'
            source.write_text(self.sample)
            with self.assertRaises(ValueError):
                m.inspect_scaps_iv(source)
        with tempfile.TemporaryDirectory(dir=Path(m.__file__).parent) as inside:
            backup = Path(inside) / 'Backup'
            backup.mkdir()
            source = backup / 'synthetic.iv'
            source.write_text(self.sample)
            with self.assertRaisesRegex(ValueError, 'backup sources'):
                m.inspect_scaps_iv(source)
            with patch.object(m.Path, 'cwd', return_value=backup):
                with self.assertRaisesRegex(ValueError, 'active project root'):
                    m.inspect_scaps_iv(source)



if __name__ == "__main__":
    unittest.main()
