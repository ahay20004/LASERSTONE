import unittest
from pathlib import Path
from local_unified_view import build, SOURCE

class UnifiedViewTests(unittest.TestCase):
    def test_original_ui_and_local_engine_evidence(self):
        original = (SOURCE / "index.html").read_text(encoding="utf-8")
        result = build().read_text(encoding="utf-8")
        self.assertIn('LASERSTONE | Scientific Research Platform', result)
        self.assertIn('local-scientific-evidence', result)
        self.assertIn('laserstone-welcome', result)
        self.assertIn('Dr. Abdelrahman A. Hagar', result)
        self.assertIn('Founder &amp; Scientific Director', result)
        self.assertIn('مرحبًا بكم', result)
        self.assertIn('data-welcome-lang="ar"', result)
        self.assertIn('data-welcome-lang="en"', result)
        self.assertIn('class="topbar"', result)
        self.assertIn('class="mission-sidebar"', result)
        self.assertIn('welcome-language.js', result)
        self.assertIn('selector.addEventListener(\'change\', updateWelcome)', (build().parent / 'welcome-language.js').read_text(encoding='utf-8'))
        self.assertIn('id="laserstone-role-ar"', result)
        self.assertIn('id="laserstone-role-en"', result)
        self.assertIn('GAIN MEDIUM', result)
        self.assertIn('د. عبدالرحمن أ. حجر', result)
        self.assertNotIn('د. عبدالرحمن أ. هجر', result)
        self.assertIn('ls-hr-mirror', result)
        self.assertIn('ls-oc-mirror', result)
        self.assertIn('ls-output-arrow', result)
        self.assertEqual(result.count('class="pump laser-pump"'), 10)
        self.assertIn('id="ls-pump-arrow"', result)
        self.assertIn(".laser-output, .laser-pump", (build().parent / 'welcome-language.js').read_text(encoding='utf-8'))
        script = (build().parent / 'welcome-language.js').read_text(encoding='utf-8')
        modes = [
            ("Infinity", "Infinity", "Plane-parallel"),
            ("0.5", "0.5", "Concentric"),
            ("1", "1", "Confocal"),
            ("Infinity", "1", "Hemispherical"),
            ("Infinity", "2", "Hemiconfocal"),
            ("1.5", "2", "General concave–concave"),
            ("0.8", "-2", "Concave–convex"),
        ]
        block = script.split("const cavityModes = [", 1)[1].split("];", 1)[0]
        self.assertEqual(block.count("{r1:"), 7)
        for r1, r2, name in modes:
            self.assertIn(f"r1:{r1},r2:{r2},en:'{name}'", block)
        self.assertIn("(1-1/mode.r1)*(1-1/mode.r2)", script)
        self.assertIn("mirrorPath(150, mode.r1, 1)", script)
        self.assertIn("mirrorPath(626, mode.r2, -1)", script)
        self.assertIn('id="ls-geometry-en"', result)
        self.assertIn('id="ls-geometry-ar"', result)
        self.assertIn('prefers-reduced-motion: reduce', script)
        self.assertIn('Violet', script)
        self.assertIn('prefers-reduced-motion', result)
        self.assertIn('class="topbar"', result)
        self.assertIn('SYNTHETIC DEMONSTRATION', result)
        self.assertIn('physics_consistency_engine', result)
        self.assertIn('connect-src \'none\'', result)
        self.assertEqual(original, (SOURCE / "index.html").read_text(encoding="utf-8"))

    def test_registered_pipeline_and_council(self):
        from local_scientific_bridge import evaluate_registered_records
        from agent_council import ROLES
        summary = evaluate_registered_records()
        self.assertGreater(summary["registered_count"], 0)
        self.assertTrue(summary["complete"])
        self.assertEqual(summary["status"], "HOLD")
        html = build().read_text(encoding="utf-8")
        self.assertIn('id="registered-pipeline-summary"', html)
        self.assertIn(f'{summary["analyzed_count"]} / {summary["registered_count"]}', html)
        self.assertIn('id="advisory-council"', html)
        for role in ROLES:
            self.assertIn(role, html)
        self.assertIn("Active agents: NOT VERIFIED", html)
        self.assertIn("Execution authorization: NONE", html)

    def test_registry_backed_workspace(self):
        from scientific_workspace import build_workspace
        from html import escape
        html=build().read_text(encoding="utf-8")
        for language in ("ar","en"):
            workspace=build_workspace("vacuum_frequency",{"vacuum_wavelength":{"value":532,"unit":"nm"}},language=language,output_unit="THz")
            result=workspace["shared_result"]
            self.assertIn(escape(workspace["knowledge"]["title"]),html)
            self.assertIn(escape(str(result["value_si"]))+" Hz",html)
            self.assertIn(escape(result["source_url"],quote=True),html)
            self.assertFalse(workspace["scientific_validation"])
        self.assertIn("Calculated educational example; not an experimental measurement.",html)
        self.assertIn("مثال تعليمي محسوب؛ لا يمثل قياسًا تجريبيًا.",html)

    def test_all_registered_equations_are_rendered(self):
        from equation_registry import REGISTRY
        from scientific_knowledge import knowledge_card
        from html import escape
        html=build().read_text(encoding="utf-8")
        for identifier, equation in REGISTRY.items():
            self.assertEqual(html.count(f'data-equation-id="{identifier}"'),2)
            self.assertIn(escape(equation.expression),html)
            self.assertIn(escape(equation.source_url,quote=True),html)
            for language in ("ar","en"):
                self.assertIn(escape(knowledge_card(identifier,language)["title"]),html)

if __name__ == "__main__":
    unittest.main()
