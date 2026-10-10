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


if __name__ == '__main__':
    unittest.main()
