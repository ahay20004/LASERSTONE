"""Test the real analysis function without main startup, GUI or report export."""
import ast
import copy
from pathlib import Path
import unittest
import subprocess
from unittest.mock import patch


def load_analysis(path=None, source=None):
    path = Path(path) if path else Path(__file__).with_name('main.py')
    tree = ast.parse(source if source is not None else path.read_text(encoding='utf-8-sig'))
    function = next(n for n in tree.body if isinstance(n, ast.FunctionDef)
                    and n.name == 'analyze_plant')
    names = {n.id for n in ast.walk(function) if isinstance(n, ast.Name)}
    namespace = {'__name__': 'g23_analysis_test'}
    for node in tree.body:
        if isinstance(node, ast.ImportFrom):
            selected = [a for a in node.names if (a.asname or a.name) in names]
            if selected:
                item = ast.ImportFrom(module=node.module, names=selected, level=node.level)
                module = ast.fix_missing_locations(ast.Module(body=[item], type_ignores=[]))
                exec(compile(module, str(path), 'exec'), namespace)
    module = ast.fix_missing_locations(ast.Module(body=[function], type_ignores=[]))
    exec(compile(module, str(path), 'exec'), namespace)
    return namespace


class AnalysisPipelineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.env = load_analysis()
        from plants_data import plants
        from g23_scientific_input_gate import validate_scientific_inputs
        cls.records = plants
        cls.sample = next(copy.deepcopy(p) for p in plants
                          if validate_scientific_inputs(p)['valid'])

    def run_analysis(self, record):
        return self.env['analyze_plant'](record)

    def test_valid_record_has_complete_dependency_chain(self):
        record = copy.deepcopy(self.sample)
        before = copy.deepcopy(record)
        result = self.run_analysis(record)
        self.assertEqual(record, before)
        self.assertTrue(result['valid'], result)
        self.assertEqual(result['lri_score'], self.env['calculate_lri'](result))
        self.assertEqual(result['physics_consistency_status'], 'HEURISTIC_SCORE_ONLY')
        self.assertIn('final_decision', result)
        self.assertEqual(result['decision_basis'], 'HEURISTIC_RESEARCH_TRIAGE_ONLY')

    def test_invalid_input_never_calls_engines(self):
        for record in (None, {}, dict(self.sample, phi=1.5),
                       dict(self.sample, refractive_index=0),
                       dict(self.sample, tau=float('nan'))):
            with self.subTest(record=record), patch.dict(self.env, calculate_lsi=lambda *a: self.fail('engine called')):
                result = self.run_analysis(record)
                self.assertFalse(result['valid'])
                self.assertNotIn('final_decision', result)

    def test_engine_failure_clears_stale_decisions(self):
        record = dict(self.sample, final_decision='STALE', governor_decision='STALE', lri_score=100)
        before = copy.deepcopy(record)
        def fail(*args):
            raise RuntimeError('controlled test failure')
        with patch.dict(self.env, calculate_lsi=fail):
            result = self.run_analysis(record)
        self.assertEqual(record, before)
        self.assertFalse(result['valid'])
        self.assertEqual(result['validation_status'], 'ENGINE_ERROR')
        self.assertNotIn('final_decision', result)
        self.assertNotIn('governor_decision', result)
        self.assertNotIn('lri_score', result)

    def test_invalid_derived_score_blocks_downstream(self):
        for value in (float('nan'), float('inf'), True, -1, 101):
            with self.subTest(value=value), patch.dict(self.env, evaluate_thermal_stability=lambda *a: value,
                 generate_final_decision=lambda *a: self.fail('decision called')):
                result = self.run_analysis(copy.deepcopy(self.sample))
                self.assertFalse(result['valid'])
                self.assertNotIn('final_decision', result)

    def test_decision_receives_complete_scores(self):
        original = self.env['generate_final_decision']
        def check(record):
            for field in ('lri_score', 'physics_consistency_score', 'scientific_confidence_score',
                          'system_integrity_score', 'intelligence_summary'):
                self.assertIn(field, record)
            return original(record)
        with patch.dict(self.env, generate_final_decision=check):
            self.assertTrue(self.run_analysis(copy.deepcopy(self.sample))['valid'])

    def test_all_records_leave_source_unchanged(self):
        before = copy.deepcopy(self.records)
        for record in self.records:
            result = self.run_analysis(record)
            self.assertIn('valid', result)
        self.assertEqual(before, self.records)

    def test_repeat_analysis_is_deterministic(self):
        first = self.run_analysis(copy.deepcopy(self.sample))
        second = self.run_analysis(first)
        self.assertEqual(first, second)

    def test_base_scores_match_frozen_legacy_calculations(self):
        baseline = Path(__file__).parent.parent / 'baseline_main.py'
        if baseline.exists():
            legacy = load_analysis(baseline)['analyze_plant']
        else:
            frozen = subprocess.run(['git', 'show', '82fe0887b7794e2d56a804d16f069b8043338c2a:main.py'],
                                    cwd=Path(__file__).parent, check=True,
                                    capture_output=True, encoding='utf-8').stdout
            legacy = load_analysis(source=frozen)['analyze_plant']
        for record in self.records:
            old = legacy(copy.deepcopy(record))
            new = self.run_analysis(record)
            self.assertTrue(new['valid'], new)
            for field in ('lsi', 'gain_score', 'thermal_score', 'q_factor_score',
                          'beam_quality_score', 'laser_efficiency_score',
                          'feasibility_score', 'material_score'):
                self.assertEqual(old[field], new[field], (record['name'], field))

    def test_invalid_lri_blocks_final_decision(self):
        with patch.dict(self.env, calculate_lri=lambda *a: float('nan'),
                        generate_final_decision=lambda *a: self.fail('decision called')):
            self.assertFalse(self.run_analysis(copy.deepcopy(self.sample))['valid'])

    def test_invalid_intelligence_blocks_governor(self):
        with patch.dict(self.env, generate_intelligence_summary=lambda *a: {'intelligence_score': float('nan')},
                        laserstone_governor_decision=lambda *a: self.fail('governor called')):
            self.assertFalse(self.run_analysis(copy.deepcopy(self.sample))['valid'])



    def test_downstream_audit_ranking_and_rendering(self):
        from audit_engine import audit_plant
        from global_ranking_engine import rank_plants
        from report_generator import generate_scientific_report
        records = [self.run_analysis(p) for p in self.records]
        before = copy.deepcopy(records)
        ranked = rank_plants(records)
        self.assertEqual(records, before)
        self.assertEqual([p['global_rank'] for p in ranked], list(range(1, len(ranked)+1)))
        self.assertEqual([p['material_score'] for p in ranked], sorted([p['material_score'] for p in records], reverse=True))
        for record in ranked:
            audit = audit_plant(record)
            self.assertEqual(audit['basis'], 'HEURISTIC_SCREEN_ONLY')
            text = generate_scientific_report(record)
            self.assertIn('HEURISTIC_RESEARCH_TRIAGE_ONLY', text)
            self.assertIn('NOT_ESTABLISHED_BY_THIS_PIPELINE', text)

    def test_report_preserves_existing_files_and_handles_name_collision(self):
        import tempfile
        from report_generator import save_single_report
        from global_ranking_engine import rank_plants
        record = rank_plants([self.run_analysis(copy.deepcopy(self.sample))])[0]
        with tempfile.TemporaryDirectory() as folder:
            first = Path(save_single_report(record, folder))
            content = first.read_bytes()
            second = Path(save_single_report(record, folder))
            self.assertNotEqual(first, second)
            self.assertEqual(first.read_bytes(), content)
            hostile = dict(record, name='../../outside')
            third = Path(save_single_report(hostile, folder))
            self.assertEqual(third.parent.resolve(), Path(folder).resolve())

    def test_report_destination_file_is_not_deleted(self):
        import tempfile
        from report_generator import ensure_reports_folder
        with tempfile.TemporaryDirectory() as folder:
            destination = Path(folder) / 'reports'
            destination.write_text('KEEP')
            with self.assertRaises(FileExistsError):
                ensure_reports_folder(destination)
            self.assertEqual(destination.read_text(), 'KEEP')

    def test_blocked_records_cannot_be_ranked_or_exported(self):
        import tempfile
        from audit_engine import audit_plant
        from global_ranking_engine import rank_plants
        from report_generator import save_all_reports
        blocked = self.run_analysis(dict(self.sample, phi=1.5))
        self.assertEqual(audit_plant(blocked)['status'], 'BLOCKED')
        with self.assertRaises(ValueError):
            rank_plants([blocked])
        with tempfile.TemporaryDirectory() as folder:
            with self.assertRaises(ValueError):
                save_all_reports([blocked], folder)
            self.assertEqual(list(Path(folder).iterdir()), [])

    def test_display_exposes_basis_and_handles_blocked_record(self):
        import io
        from contextlib import redirect_stdout
        from display import display_plant_result
        result = self.run_analysis(copy.deepcopy(self.sample))
        stream = io.StringIO()
        with redirect_stdout(stream):
            display_plant_result(result)
        self.assertIn('Physical Validation: NOT_ESTABLISHED_BY_THIS_PIPELINE', stream.getvalue())
        stream = io.StringIO()
        with redirect_stdout(stream):
            display_plant_result(self.run_analysis({}))
        self.assertIn('Analysis blocked:', stream.getvalue())

    def test_empty_ranking_and_export_are_safe(self):
        import tempfile
        from global_ranking_engine import rank_plants
        from report_generator import save_all_reports
        self.assertEqual(rank_plants([]), [])
        with tempfile.TemporaryDirectory() as folder:
            self.assertEqual(save_all_reports([], folder), [])
            self.assertEqual(list(Path(folder).iterdir()), [])

class RuntimeIntegrationTests(unittest.TestCase):
    def test_real_launcher_preparation_preserves_source(self):
        import safe_dashboard_launcher as launcher
        from plants_data import plants
        snapshot = copy.deepcopy(plants)
        ranked = launcher.prepare_dashboard_plants(plants)
        self.assertEqual(len(ranked), len(plants))
        self.assertEqual(plants, snapshot)
        self.assertTrue(all(p['analysis_status'] == 'COMPLETE_HEURISTIC_ANALYSIS'
                            and p['valid'] for p in ranked))

    def test_launcher_does_not_fall_back_to_raw_records(self):
        import safe_dashboard_launcher as launcher
        import main
        raw = [{'name': 'invalid'}]
        with patch.object(main, 'analyze_plant', return_value={'valid': False}):
            self.assertEqual(launcher.prepare_dashboard_plants(raw), [])
        with patch.dict('sys.modules', {'main': None}):
            self.assertEqual(launcher.prepare_dashboard_plants(raw), [])

    def test_launcher_ranking_failure_blocks_results(self):
        import safe_dashboard_launcher as launcher
        import main
        with patch.object(main, 'analyze_plant', return_value={
                'valid': True, 'analysis_status': 'COMPLETE_HEURISTIC_ANALYSIS'}), \
                patch('global_ranking_engine.rank_plants', side_effect=ValueError('bad score')):
            self.assertEqual(launcher.prepare_dashboard_plants([{'name': 'raw'}]), [])

    def test_launcher_rejects_unqualified_analysis(self):
        import safe_dashboard_launcher as launcher
        import main
        for record in ({'valid': True}, {'valid': True, 'analysis_status': 'BLOCKED'}):
            with self.subTest(record=record), patch.object(main, 'analyze_plant', return_value=record):
                self.assertEqual(launcher.prepare_dashboard_plants([{}]), [])

    def test_no_dashboard_launch_when_preparation_is_empty(self):
        import safe_dashboard_launcher as launcher
        import dashboard_city
        with patch.object(launcher, 'load_plants', return_value=[{'name': 'raw'}]), \
                patch.object(launcher, 'prepare_dashboard_plants', return_value=[]), \
                patch.object(launcher, 'load_dashboard') as load_dashboard, \
                patch.object(dashboard_city, 'launch_dashboard') as city:
            launcher.open_dashboard_after_approval()
            launcher.open_city_after_approval()
            load_dashboard.return_value.assert_not_called()
            city.assert_not_called()

    def test_full_no_gui_runtime_preserves_previous_report(self):
        import shutil
        import sys
        import tempfile
        source = Path(__file__).resolve().parent
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder) / 'project'
            shutil.copytree(source, root, ignore=shutil.ignore_patterns('__pycache__', 'reports'))
            reports = root / 'reports'
            reports.mkdir()
            previous = reports / 'hibiscus_report.txt'
            previous.write_text('preserved historical report', encoding='utf-8')
            raw_data = (root / 'plants_data.py').read_bytes()
            result = subprocess.run([sys.executable, str(root / 'main.py'), '--no-gui'],
                                    cwd=root, capture_output=True, text=True, encoding='utf-8',
                                    env={**__import__('os').environ, 'PYTHONIOENCODING': 'utf-8'},
                                    timeout=30)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn('NUMBER OF RANKED PLANTS: 7', result.stdout)
            self.assertIn('END LASERSTONE MAIN SYSTEM', result.stdout)
            self.assertIn('DASHBOARD SKIPPED', result.stdout)
            self.assertNotIn('SYSTEM ERROR:', result.stdout)
            self.assertEqual(previous.read_text(encoding='utf-8'), 'preserved historical report')
            self.assertEqual(len(list(reports.glob('*_report*.txt'))), 8)
            self.assertEqual((root / 'plants_data.py').read_bytes(), raw_data)
            new_report = (reports / 'hibiscus_report_001.txt').read_text(encoding='utf-8')
            self.assertIn('NOT_ESTABLISHED_BY_THIS_PIPELINE', new_report)

    def test_startup_failure_returns_nonzero_exit_status(self):
        import sys
        import tempfile
        with tempfile.TemporaryDirectory() as folder:
            result = subprocess.run([sys.executable, str(Path(__file__).with_name('main.py')),
                                     '--no-gui'], cwd=folder, capture_output=True, text=True,
                                    encoding='utf-8', timeout=30,
                                    env={**__import__('os').environ, 'PYTHONIOENCODING': 'utf-8'})
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('Startup diagnostic failed', result.stdout)
            self.assertFalse((Path(folder) / 'reports').exists())


if __name__ == '__main__':
    unittest.main()

