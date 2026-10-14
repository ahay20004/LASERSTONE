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


class UnifiedRuntimeTests(unittest.TestCase):
    def test_loader_returns_detached_nonempty_database(self):
        import safe_dashboard_launcher as launcher
        from plants_data import plants
        loaded = launcher.load_plants()
        self.assertEqual(loaded, plants)
        self.assertIsNot(loaded, plants)
        loaded[0]['name'] = 'changed test copy'
        self.assertNotEqual(loaded[0]['name'], plants[0]['name'])

    def test_preparation_runs_once_and_populates_every_material(self):
        import main
        from plants_data import plants
        original = copy.deepcopy(plants)
        with patch.object(main, 'run_startup_diagnostic', return_value=True) as startup, \
                patch.object(main, 'run_code_quality_guard', return_value=True) as quality, \
                patch.object(main, 'analyze_plant', wraps=main.analyze_plant) as analysis, \
                patch.object(main, 'generate_hybrid_candidates', wraps=main.generate_hybrid_candidates) as hybrids, \
                patch.object(main, 'save_all_reports') as export, \
                patch('subprocess.Popen') as process:
            state = main.prepare_runtime()
        startup.assert_called_once()
        quality.assert_called_once()
        hybrids.assert_called_once()
        self.assertEqual(analysis.call_count, len(plants))
        export.assert_not_called()
        process.assert_not_called()
        self.assertEqual(plants, original)
        for plant in state['ranked_plants']:
            self.assertEqual(plant['mission_control']['name'], plant['name'])
            self.assertIn('laser_architecture', plant)
            self.assertIn('laser_output', plant)
            self.assertIn('audit_status', plant)
        self.assertEqual(state['simulators']['simulators']['scaps-1d']['simulation_execution'], 'NOT_TESTED')

    def test_gates_fail_closed_before_analysis(self):
        import main
        with patch.object(main, 'run_startup_diagnostic', return_value=False), \
                patch.object(main, 'analyze_plant') as analysis:
            with self.assertRaisesRegex(RuntimeError, 'Startup diagnostic failed'):
                main.prepare_runtime()
            analysis.assert_not_called()
        with patch.object(main, 'run_startup_diagnostic', return_value=True), \
                patch.object(main, 'run_code_quality_guard', return_value=False), \
                patch.object(main, 'analyze_plant') as analysis:
            with self.assertRaisesRegex(RuntimeError, 'Code quality guard failed'):
                main.prepare_runtime()
            analysis.assert_not_called()
        with patch.object(main, 'run_startup_diagnostic', return_value=True), \
                patch.object(main, 'run_code_quality_guard', return_value=True), \
                patch.object(main, 'run_configuration_validation', return_value={'system_valid': False}), \
                patch.object(main, 'analyze_plant') as analysis:
            with self.assertRaisesRegex(RuntimeError, 'Configuration validation failed'):
                main.prepare_runtime()
            analysis.assert_not_called()

    def test_partial_batch_never_silently_becomes_ready(self):
        import main
        from plants_data import plants
        with self.assertRaisesRegex(RuntimeError, 'Analysis blocked'):
            main.prepare_analysis([plants[0], {'name': 'incomplete'}])

    def test_ranking_failure_is_not_hidden(self):
        import main
        from plants_data import plants
        with patch('global_ranking_engine.rank_plants', side_effect=ValueError('controlled rank failure')):
            with self.assertRaisesRegex(ValueError, 'controlled rank failure'):
                main.prepare_analysis(plants)

    def test_gateway_requires_checked_session_not_import_success(self):
        from entry_gateway import check_system_status
        self.assertEqual(check_system_status({})['status'], 'BLOCKED')
        import main
        state = main.prepare_runtime()
        self.assertEqual(check_system_status(state)['status'], 'ANALYSIS_READY')
        state['checks']['ranking'] = 'FAIL'
        self.assertEqual(check_system_status(state)['status'], 'BLOCKED')

    def test_registered_connections_do_not_prove_execution(self):
        from system_health_engine import describe_runtime_state
        registry = {'a': {'inputs': ['x']}, 'b': {'outputs': []}}
        evidence = describe_runtime_state([], registry=registry)
        self.assertEqual(evidence['registered_engines'], 2)
        self.assertEqual(evidence['declared_connected'], 1)
        self.assertEqual(evidence['declared_isolated'], 1)
        self.assertEqual(evidence['status'], 'NOT_VERIFIED')
        self.assertEqual(evidence['engine_execution'], 'NOT_INSTRUMENTED')
        self.assertEqual(evidence['simulator_execution'], 'NOT_VERIFIED')

    def test_gateway_handoff_reuses_prepared_session(self):
        import safe_dashboard_launcher as launcher
        import main
        state = main.prepare_runtime()
        def gateway(dashboard, city, runtime_state):
            self.assertIs(runtime_state, state)
            dashboard()
            city()
        with patch.object(main, 'prepare_runtime', return_value=state) as prepare, \
                patch.object(launcher, 'open_entry_gateway', side_effect=gateway), \
                patch.object(launcher, 'load_dashboard') as dashboard, \
                patch('dashboard_city.launch_dashboard') as city:
            launcher.main()
        prepare.assert_called_once()
        dashboard.return_value.assert_called_once_with(state['ranked_plants'], runtime_state=state)
        city.assert_called_once_with(state['ranked_plants'], runtime_state=state)

    def test_single_material_and_empty_network_finish_without_stale_loop_variables(self):
        import main
        from plants_data import plants
        import io
        from contextlib import redirect_stdout
        with patch.object(main, 'plants', [plants[0]]), \
                patch.object(main, 'build_material_network', return_value=[]), \
                patch.object(main, 'save_all_reports', return_value=[]), \
                redirect_stdout(io.StringIO()):
            state = main.main(open_dashboard=False)
        self.assertEqual(len(state['ranked_plants']), 1)
        self.assertEqual(state['ranked_plants'][0]['mission_control']['name'], state['ranked_plants'][0]['name'])

    def test_console_uses_same_prepared_records(self):
        import main
        import io
        from contextlib import redirect_stdout
        state = main.prepare_runtime()
        with patch.object(main, 'prepare_runtime', return_value=state) as prepare, \
                patch.object(main, 'save_all_reports', return_value=[]) as export, \
                patch.object(main, 'analyze_plant') as analysis, \
                patch.object(main, 'generate_hybrid_candidates') as hybrids, \
                redirect_stdout(io.StringIO()):
            result = main.main(open_dashboard=False)
        self.assertIs(result, state)
        prepare.assert_called_once()
        export.assert_called_once_with(state['ranked_plants'])
        analysis.assert_not_called()
        hybrids.assert_not_called()

    def test_launcher_check_is_read_only_and_does_not_open_gui(self):
        import main
        import safe_dashboard_launcher as launcher
        import io
        from contextlib import redirect_stdout
        with patch.object(main, 'save_all_reports') as export, \
                patch.object(launcher, 'open_entry_gateway') as gateway, \
                redirect_stdout(io.StringIO()):
            state = launcher.main(check_only=True)
        self.assertEqual(state['status'], 'ANALYSIS_READY')
        export.assert_not_called()
        gateway.assert_not_called()

    def test_declared_layers_are_not_active_engine_count(self):
        from runtime_monitor_engine import generate_runtime_report
        report = generate_runtime_report(1, 7, 8)
        self.assertEqual(report['declared_layers'], 8)
        self.assertIsNone(report['engines_active'])

    def test_gateway_city_closes_root_before_callback_and_propagates_failure(self):
        import entry_gateway as gateway
        from unittest.mock import MagicMock
        root = MagicMock()
        buttons = {}
        def button(parent, **options):
            buttons[options['text']] = options
            return MagicMock()
        def city():
            root.destroy.assert_called_once()
            raise RuntimeError('controlled view failure')
        root.mainloop.side_effect = lambda: buttons['OPEN SCIENTIFIC CITY']['command']()
        ready = {'status': 'ANALYSIS_READY', 'issues': [], 'plants_count': 7,
                 'dashboard_ready': True, 'city_ready': True}
        with patch.object(gateway, 'check_system_status', return_value=ready), \
                patch.object(gateway.tk, 'Tk', return_value=root), \
                patch.object(gateway.tk, 'Label'), patch.object(gateway.tk, 'Text'), \
                patch.object(gateway.tk, 'Frame'), patch.object(gateway.tk, 'Button', side_effect=button):
            with self.assertRaisesRegex(RuntimeError, 'controlled view failure'):
                gateway.open_entry_gateway(lambda: None, city)
        root.withdraw.assert_not_called()

    def test_gateway_blocks_callbacks_even_if_disabled_button_command_is_invoked(self):
        import entry_gateway as gateway
        from unittest.mock import MagicMock
        root = MagicMock()
        buttons = {}
        def button(parent, **options):
            buttons[options['text']] = options
            return MagicMock()
        def attempt():
            buttons['OPEN DASHBOARD']['command']()
            buttons['OPEN SCIENTIFIC CITY']['command']()
        root.mainloop.side_effect = attempt
        blocked = {'status': 'BLOCKED', 'issues': ['incomplete'], 'plants_count': 0,
                   'dashboard_ready': False, 'city_ready': False}
        callback = MagicMock()
        with patch.object(gateway, 'check_system_status', return_value=blocked), \
                patch.object(gateway.tk, 'Tk', return_value=root), \
                patch.object(gateway.tk, 'Label'), patch.object(gateway.tk, 'Text'), \
                patch.object(gateway.tk, 'Frame'), patch.object(gateway.tk, 'Button', side_effect=button):
            gateway.open_entry_gateway(callback, callback)
        callback.assert_not_called()
        self.assertEqual(buttons['OPEN DASHBOARD']['state'], 'disabled')

    def test_post_diagnostics_are_not_duplicated(self):
        import sys
        import tempfile
        import shutil
        source = Path(__file__).resolve().parent
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder) / 'project'
            shutil.copytree(source, root, ignore=shutil.ignore_patterns('.git', '__pycache__', 'reports'))
            result = subprocess.run([sys.executable, str(root / 'main.py'), '--no-gui'], cwd=root,
                                    capture_output=True, encoding='utf-8', timeout=30,
                                    env={**__import__('os').environ, 'PYTHONIOENCODING': 'utf-8'})
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(result.stdout.count('=== LASERSTONE STARTUP DIAGNOSTIC ==='), 1)
        self.assertEqual(result.stdout.count('=== SYSTEM HEALTH REPORT ==='), 1)



class ViewConstructionTests(unittest.TestCase):
    def widgets(self, stack):
        import tkinter as tk
        from tkinter import ttk
        from unittest.mock import MagicMock
        buttons = []
        root = MagicMock()
        frame = MagicMock()
        tree = MagicMock()
        def button(parent, **options):
            buttons.append(options)
            return MagicMock()
        stack.enter_context(patch.object(tk, 'Tk', return_value=root))
        stack.enter_context(patch.object(tk, 'Toplevel', return_value=MagicMock()))
        stack.enter_context(patch.object(tk, 'Frame', return_value=frame))
        for name in ('Label', 'LabelFrame', 'Text', 'Canvas'):
            stack.enter_context(patch.object(tk, name, return_value=MagicMock()))
        stack.enter_context(patch.object(tk, 'Button', side_effect=button))
        stack.enter_context(patch.object(ttk, 'Scrollbar', return_value=MagicMock()))
        stack.enter_context(patch.object(ttk, 'Treeview', return_value=tree))
        return root, frame, tree, buttons

    def test_project_builds_buttons_table_and_loop_without_button_click(self):
        import dashboard
        import main
        from contextlib import ExitStack
        state = main.prepare_runtime()
        with ExitStack() as stack:
            root, frame, tree, buttons = self.widgets(stack)
            result = dashboard.launch_dashboard(state['ranked_plants'], runtime_state=state)
            root.mainloop.assert_called_once()
            tree.pack.assert_called_once()
            self.assertEqual(tree.insert.call_count, len(state['ranked_plants']))
            tree.bind.assert_called_once()
            self.assertGreaterEqual(len(buttons), 16)
            for options in list(buttons):
                self.assertTrue(callable(options['command']), options['text'])
                options['command']()
            self.assertIs(result, root)

    def test_embedded_project_uses_toplevel_and_no_second_loop(self):
        import dashboard
        import main
        import tkinter as tk
        from contextlib import ExitStack
        state = main.prepare_runtime()
        with ExitStack() as stack:
            root, frame, tree, buttons = self.widgets(stack)
            parent = object()
            result = dashboard.launch_dashboard(state['ranked_plants'], runtime_state=state, parent=parent)
            tk.Tk.assert_not_called()
            tk.Toplevel.assert_called_once_with(parent)
            result.mainloop.assert_not_called()
            self.assertEqual(tree.insert.call_count, 7)

    def test_university_buildings_are_live_and_share_project_session(self):
        import dashboard_city
        import main
        import dashboard
        from contextlib import ExitStack
        state = main.prepare_runtime()
        with ExitStack() as stack:
            root, frame, tree, buttons = self.widgets(stack)
            frame.after.side_effect = lambda delay, callback: callback() if delay == 1900 else None
            dashboard_city.launch_dashboard(state['ranked_plants'], runtime_state=state, open_university=True)
            root.mainloop.assert_called_once()
            campus = [b for b in buttons if b.get('state') == 'normal']
            self.assertEqual(len(campus), 7)
            for options in campus:
                self.assertTrue(callable(options['command']))
                options['command']()
            project = next(b for b in buttons if b['text'] == 'OPEN PROJECT DASHBOARD')
            with patch.object(dashboard, 'launch_dashboard') as launch:
                project['command']()
            launch.assert_called_once_with(state['ranked_plants'], runtime_state=state, parent=frame)

    def test_saved_scaps_reader_button_uses_same_session_and_leaves_source_unchanged(self):
        import dashboard_city
        import main
        import g23_simulation_exchange_contract as exchange
        from test_g23_simulation_exchange_contract import SavedScapsIvTests
        from contextlib import ExitStack
        import tempfile
        state = main.prepare_runtime()
        with tempfile.TemporaryDirectory(dir=Path(exchange.__file__).parent) as folder:
            source = Path(folder) / 'synthetic.iv'
            data = SavedScapsIvTests.sample.encode()
            source.write_bytes(data)
            with ExitStack() as stack:
                root, frame, tree, buttons = self.widgets(stack)
                frame.after.side_effect = lambda delay, callback: callback() if delay == 1900 else None
                analysis = stack.enter_context(patch.object(main, 'analyze_plant'))
                process = stack.enter_context(patch('subprocess.Popen'))
                choose = stack.enter_context(patch('tkinter.filedialog.askopenfilename', return_value=str(source)))
                blocked = stack.enter_context(patch('tkinter.messagebox.showerror'))
                inspect = stack.enter_context(patch.object(exchange, 'inspect_scaps_iv', wraps=exchange.inspect_scaps_iv))
                dashboard_city.launch_dashboard(state['ranked_plants'], runtime_state=state, open_university=True)
                labs = next(b for b in buttons if 'Research Laboratories' in b['text'] and b.get('state') == 'normal')
                labs['command']()
                reader = next(b for b in buttons if b['text'] == 'READ SAVED SCAPS I-V')
                reader['command']()
                inspect.assert_called_once_with(str(source))
                choose.assert_called_once()
                blocked.assert_not_called()
                analysis.assert_not_called()
                process.assert_not_called()
            self.assertEqual(source.read_bytes(), data)
            self.assertEqual(list(Path(folder).iterdir()), [source])

    def test_university_missing_callback_is_disabled(self):
        from city.university_plaza import open_university_plaza
        from contextlib import ExitStack
        with ExitStack() as stack:
            root, frame, tree, buttons = self.widgets(stack)
            open_university_plaza(frame, [], {})
            self.assertEqual(len(buttons), 7)
            self.assertTrue(all(b['state'] == 'disabled' for b in buttons))
            self.assertTrue(all(b['wraplength'] == 230 for b in buttons))

    def test_university_launcher_import_has_no_gui_side_effect(self):
        import importlib
        import tkinter as tk
        with patch.object(tk, 'Tk') as root:
            module = importlib.import_module('city.plaza_launcher')
            importlib.reload(module)
        root.assert_not_called()



if __name__ == '__main__':
    unittest.main()

