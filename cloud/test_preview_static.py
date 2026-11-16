"""Static, dependency-free checks for the LASERSTONE bilingual public preview."""
from html.parser import HTMLParser
from pathlib import Path
import json
import re
import unittest
import subprocess
import sys
import tempfile

SITE = Path(__file__).resolve().parent / "site"

class Markup(HTMLParser):
    def __init__(self):
        super().__init__()
        self.keys = []
        self.languages = []
        self.references = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "data-i18n" in attrs:
            self.keys.append(attrs["data-i18n"])
        if tag == "option" and "value" in attrs and attrs["value"] in ("en", "ar"):
            self.languages.append(attrs["value"])
        if tag in ("script", "link", "img"):
            self.references.extend(v for k,v in attrs.items() if k in ("src","href") and v and v.startswith("./"))

class PreviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = (SITE / "index.html").read_text(encoding="utf-8")
        cls.js = (SITE / "i18n.js").read_text(encoding="utf-8")
        cls.markup = Markup()
        cls.markup.feed(cls.html)
        match = re.search(r"const translations\s*=\s*(\{.*?\})\s*;\s*const supported", cls.js, re.S)
        if match is None:
            raise AssertionError("Translations dictionary not found")
        cls.messages = json.loads(match.group(1))

    def test_all_internal_navigation_targets_exist(self):
        ids = set(re.findall(r'\\bid="([^"]+)"', self.html))
        targets = re.findall(r'<a\\b[^>]*\\bhref="#([^"]+)"', self.html)
        self.assertTrue(targets)
        for target in targets:
            self.assertIn(target, ids, f"Broken internal icon/navigation link: #{target}")
        self.assertIn('href="#agent-council"', self.html)
        self.assertIn('id="agent-council"', self.html)
        self.assertEqual(self.html.count('class="research-link"'), 3)
        for lang in ("en", "ar"):
            for key in ("agentsTitle", "agentsIntro", "agentsFootnote",
                        "agentsPhysics", "agentsEvidence", "agentsSimulator",
                        "agentsCoordinator"):
                self.assertTrue(self.messages[lang].get(key))

    def test_only_arabic_english(self):
        self.assertEqual(set(self.messages), {"en", "ar"})
        self.assertEqual(set(self.markup.languages), {"en", "ar"})
        self.assertEqual(len(self.markup.languages), 2)

    def test_translation_coverage(self):
        self.assertEqual(set(self.messages["en"]), set(self.messages["ar"]))
        for lang in ("en", "ar"):
            for key in self.markup.keys:
                self.assertTrue(self.messages[lang].get(key), f"{lang}: missing {key}")

    def test_static_assets(self):
        for ref in self.markup.references:
            self.assertTrue((SITE / ref).is_file(), f"Missing: {ref}")
        manifest = json.loads((SITE / "manifest.webmanifest").read_text(encoding="utf-8"))
        self.assertTrue(manifest["name"])
        for icon in manifest["icons"]:
            self.assertTrue((SITE / icon["src"]).is_file())

    def test_security_headers(self):
        headers = (SITE / "_headers").read_text(encoding="utf-8")
        self.assertIn("default-src 'none'", headers)
        self.assertIn("script-src 'self'", headers)
        self.assertIn("frame-ancestors 'none'", headers)

    def test_cockpit_is_explicitly_non_live(self):
        for anchor in ('id="cockpit"', 'id="research"', 'id="integrity"', 'id="access"'):
            self.assertIn(anchor, self.html)
        for lang in ("en", "ar"):
            for key in ("cockpitTitle", "cockpitFootnote", "statusDisconnected", "statusRestricted"):
                self.assertTrue(self.messages[lang].get(key), f"{lang}: missing {key}")
        self.assertIn("No live telemetry", self.messages["en"]["cockpitFootnote"])
        self.assertIn("غير متصل", self.messages["ar"]["statusDisconnected"])

    def test_no_external_script_or_form_actions(self):
        self.assertNotRegex(self.html, r'(?i)<script[^>]+src=["\\\']https?://')
        self.assertNotRegex(self.html, r'(?i)<form\b')
        self.assertNotRegex(self.html, r'(?i)<iframe\b')
        self.assertNotRegex(self.js, r'(?i)\b(fetch|XMLHttpRequest|WebSocket|sendBeacon)\s*\(')

    def test_staging_has_only_approved_public_assets(self):
        script = SITE.parent / "huggingface" / "prepare_space.py"
        allowed = {"README.md", "index.html", "style.css", "i18n.js", "icon.svg", "manifest.webmanifest"}
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "preview"
            subprocess.run([sys.executable, str(script), "--output", str(target)],
                           check=True, capture_output=True, text=True)
            self.assertEqual({p.name for p in target.iterdir()}, allowed)
            self.assertFalse((target / "_headers").exists())
            self.assertFalse(any(p.is_dir() for p in target.iterdir()))

    def test_security_headers_are_not_claimed_as_deployed(self):
        # These headers are a source template, not enforced by the static HF Space.
        script = (SITE.parent / "huggingface" / "prepare_space.py").read_text(encoding="utf-8")
        self.assertIn('ASSETS = ("index.html", "style.css", "i18n.js", "icon.svg", "manifest.webmanifest")', script)
        self.assertIn("NOT applied by this static Space", script)

    def test_cockpit_controls_are_accessible_and_non_operational(self):
        from html.parser import HTMLParser
        class Buttons(HTMLParser):
            def __init__(self):
                super().__init__()
                self.panels = []
            def handle_starttag(self, tag, attrs):
                if tag == "button":
                    attrs = dict(attrs)
                    if "data-panel" in attrs:
                        self.panels.append(attrs)
        buttons = Buttons()
        buttons.feed(self.html)
        self.assertEqual({p["data-panel"] for p in buttons.panels},
                         {"evidence", "physics", "solar", "owner"})
        self.assertEqual(len(buttons.panels), 4)
        for panel in buttons.panels:
            self.assertEqual(panel.get("type"), "button")
            self.assertEqual(panel.get("aria-pressed"), "false")
            self.assertEqual(panel.get("aria-controls"), "cockpit-readout")
        self.assertIn('id="cockpit-readout"', self.html)
        self.assertIn('aria-live="polite"', self.html)
        self.assertIn("selectedPanel = button.dataset.panel === selectedPanel ? null", self.js)
        self.assertIn("updateReadout(document.documentElement.lang)", self.js)
        self.assertIn("updateReadout(chosen)", self.js)
        for lang in ("en", "ar"):
            for key in ("selectPanel", "readoutIdle", "readoutIdleDesc",
                        "readoutEvidence", "readoutPhysics", "readoutSolar", "readoutOwner"):
                self.assertTrue(self.messages[lang].get(key), f"{lang}: missing {key}")


    def test_mission_navigation_targets_and_monitoring_integrity(self):
        """All cockpit navigation links resolve and monitoring remains explicitly non-live."""
        class Navigation(HTMLParser):
            def __init__(self):
                super().__init__()
                self.ids = []
                self.anchors = []
                self.monitor_cards = 0
            def handle_starttag(self, tag, attrs):
                attrs = dict(attrs)
                if "id" in attrs:
                    self.ids.append(attrs["id"])
                if tag == "a" and attrs.get("href", "").startswith("#"):
                    self.anchors.append(attrs["href"][1:])
                if tag == "article" and "mission-monitor-card" in attrs.get("class", "").split():
                    self.monitor_cards += 1
        nav = Navigation()
        nav.feed(self.html)
        self.assertEqual(len(nav.ids), len(set(nav.ids)), "Duplicate HTML IDs")
        self.assertTrue(nav.anchors, "No navigation anchors found")
        self.assertFalse(set(nav.anchors) - set(nav.ids),
                         f"Broken anchors: {set(nav.anchors) - set(nav.ids)}")
        self.assertEqual(nav.monitor_cards, 4)
        self.assertIn('class="mission-sidebar"', self.html)
        self.assertIn('class="mission-monitor-grid"', self.html)
        for lang in ("en", "ar"):
            for key in ("missionMenu", "missionDashboard", "missionProjects",
                        "missionAgents", "missionEvidence", "missionSecurity",
                        "missionMonitorTitle", "missionNoData"):
                self.assertTrue(self.messages[lang].get(key), f"{lang}: missing {key}")
        self.assertEqual(self.messages["en"]["missionNoData"], "No live data")
        self.assertNotRegex(self.html, r'(?i)\b(?:live|active)\s+(?:users|projects|agents)\s*:\s*\d+')


    def test_scientific_entrance_maxims_are_bilingual_and_attributed(self):
        self.assertIn('id="scientific-gates"', self.html)
        self.assertEqual(self.html.count('class="gate-card"'), 3)
        for lang in ("en", "ar"):
            for key in ("gatesTitle", "gatesIntro", "gatesAttribution",
                        "gatePhysicsQuote", "gateEngineeringQuote", "gateIntegrityQuote"):
                self.assertTrue(self.messages[lang].get(key), f"{lang}: missing {key}")
        self.assertIn("original", self.messages["en"]["gatesAttribution"].lower())
        self.assertIn("أصلية", self.messages["ar"]["gatesAttribution"])
        self.assertIn("البرهان", self.messages["ar"]["gateIntegrityQuote"])


    def test_learning_path_is_bilingual_accessible_and_non_operational(self):
        self.assertIn('id="learning-path"', self.html)
        self.assertEqual(len(re.findall(r'<button[^>]*class="learning-step(?: is-current)?"', self.html)), 5)
        for index in range(5):
            self.assertIn(f'data-step="{index}"', self.html)
            for lang in ("en", "ar"):
                self.assertTrue(self.messages[lang].get(f"learningStep{index}"))
                self.assertTrue(self.messages[lang].get(f"learningDesc{index}"))
        for key in ("learningIntro", "learningDisclaimer", "learningPrev", "learningNext"):
            self.assertTrue(self.messages["en"].get(key))
            self.assertTrue(self.messages["ar"].get(key))
        self.assertIn('id="learning-readout"', self.html)
        self.assertIn('id="learning-prev" disabled', self.html)
        self.assertIn('id="learning-next"', self.html)
        self.assertIn('aria-pressed="true"', self.html)
        self.assertIn("updateLearning(chosen)", self.js)
        self.assertIn("updateLearning(document.documentElement.lang)", self.js)
        self.assertIn("No data collection", self.messages["en"]["learningDisclaimer"])


    def test_physics_example_has_model_limits_and_no_fabricated_results(self):
        self.assertIn('class="learning-example"', self.html)
        self.assertIn("I(z) = I₀ exp(−αz)", self.html)
        for lang in ("en", "ar"):
            for key in ("exampleTitle", "exampleVariables", "exampleAssumptions",
                        "exampleValidation", "exampleWarning"):
                self.assertTrue(self.messages[lang].get(key), f"{lang}: missing {key}")
        self.assertIn("No measured data", self.messages["en"]["exampleValidation"])
        self.assertIn("لا تُعرض هنا بيانات مقاسة", self.messages["ar"]["exampleValidation"])


    def test_physics_teaching_stages_follow_selected_learning_step(self):
        self.assertIn('id="example-stage-title"', self.html)
        self.assertIn('id="example-stage-detail"', self.html)
        self.assertIn("messages['exampleStageTitle' + learningIndex]", self.js)
        self.assertIn("messages['exampleStageDetail' + learningIndex]", self.js)
        for lang in ("en", "ar"):
            for index in range(5):
                self.assertTrue(self.messages[lang].get(f"exampleStageTitle{index}"))
                self.assertTrue(self.messages[lang].get(f"exampleStageDetail{index}"))
        self.assertIn("dI/dz", self.messages["en"]["exampleStageDetail2"])
        self.assertIn("عدم اليقين", self.messages["ar"]["exampleStageDetail3"])


    def test_attenuation_lab_is_bounded_bilingual_and_explicitly_hypothetical(self):
        self.assertIn('class="attenuation-lab"', self.html)
        self.assertIn('id="lab-alpha" type="range" min="0" max="2" step="0.05" value="0.5"', self.html)
        self.assertIn('id="lab-depth" type="range" min="0" max="10" step="0.5" value="2"', self.html)
        self.assertIn("Math.exp(-alpha * depth)", self.js)
        self.assertIn("labAlpha.addEventListener('input', updateAttenuation)", self.js)
        self.assertIn("labDepth.addEventListener('input', updateAttenuation)", self.js)
        for lang in ("en", "ar"):
            for key in ("labEyebrow", "labTitle", "labIntro", "labAlpha",
                        "labDepth", "labResult", "labDisclaimer"):
                self.assertTrue(self.messages[lang].get(key), f"{lang}: missing {key}")
        self.assertIn("hypothetical", self.messages["en"]["labDisclaimer"])
        self.assertIn("افتراضية", self.messages["ar"]["labDisclaimer"])


    def test_wavelength_controls_are_illustrative_not_material_data(self):
        self.assertIn('id="lab-wavelength"', self.html)
        self.assertIn('id="lab-incident" type="range"', self.html)
        self.assertIn('id="lab-absolute"', self.html)
        self.assertIn("Object.freeze({'532': 0.8, '632.8': 0.5, '1064': 0.2})", self.js)
        self.assertIn("incident * ratio", self.js)
        self.assertIn("labWavelength.addEventListener('change'", self.js)
        for lang in ("en", "ar"):
            for key in ("labWavelength", "labCoefficientNote", "labIncident", "labAbsolute"):
                self.assertTrue(self.messages[lang].get(key), f"{lang}: missing {key}")
        self.assertIn("invented teaching coefficients", self.messages["en"]["labCoefficientNote"])
        self.assertIn("افتراضية", self.messages["ar"]["labCoefficientNote"])


    def test_mission_roadmap_is_static_bilingual_and_has_attention_control(self):
        self.assertIn('id="mission-roadmap"', self.html)
        self.assertIn('id="roadmap-alert-button"', self.html)
        self.assertIn('aria-controls="roadmap-alert-details"', self.html)
        self.assertIn('id="roadmap-alert-details" hidden', self.html)
        self.assertIn("roadmapAlertButton.addEventListener('click'", self.js)
        self.assertIn("roadmapAlertDetails.hidden = expanded", self.js)
        self.assertIn("not live GitHub telemetry", self.messages["en"]["roadmapIntro"])
        self.assertIn("ولا يرسل إشعارات", self.messages["ar"]["roadmapAlertDisclaimer"])
        for lang in ("en", "ar"):
            for key in ("navRoadmap", "missionRoadmap", "roadmapTitle",
                        "roadmapAlertButton", "roadmapAlertHide",
                        "roadmapDone6", "roadmapNext5", "roadmapRisk3"):
                self.assertTrue(self.messages[lang].get(key), f"{lang}: missing {key}")
        self.assertTrue((SITE.parent / "MISSION_CONTROL_ROADMAP.md").is_file())


    def test_explorer_lesson_is_bilingual_and_photon_energy_is_bounded(self):
        self.assertIn('id="scientific-explorer"', self.html)
        self.assertIn('id="explorer-wavelength"', self.html)
        self.assertIn('id="explorer-energy"', self.html)
        self.assertIn('id="explorer-frequency"', self.html)
        self.assertIn('id="explorer-joules"', self.html)
        self.assertIn("const h = 6.62607015e-34", self.js)
        self.assertIn("const c = 299792458", self.js)
        self.assertIn("const electronVoltJ = 1.602176634e-19", self.js)
        self.assertIn("[532, 632.8, 1064].includes(wavelengthNm)", self.js)
        self.assertIn("explorerWavelength.addEventListener('change', updatePhotonEnergy)", self.js)
        for lang in ("en", "ar"):
            for key in ("navExplorer", "explorerTitle", "explorerSpontDesc",
                        "explorerStimDesc", "explorerEquation", "explorerEvidence",
                        "explorerSources", "explorerAssumptions"):
                self.assertTrue(self.messages[lang].get(key), f"{lang}: missing {key}")
        self.assertIn("no measured populations", self.messages["en"]["explorerEvidence"])

    def test_curated_library_search_is_bilingual_local_and_safe(self):
        self.assertIn('id="knowledge-library"', self.html)
        self.assertIn('id="library-search" type="search"', self.html)
        self.assertIn('id="library-results"', self.html)
        self.assertIn("const libraryEntries = Object.freeze([", self.js)
        self.assertIn("results.replaceChildren()", self.js)
        self.assertIn("title.textContent =", self.js)
        self.assertIn("librarySearch.addEventListener('input', renderKnowledgeLibrary)", self.js)
        for lang in ("en", "ar"):
            for key in ("libraryTitle", "librarySearchLabel", "libraryEmpty",
                        "libraryDisclaimer", "libraryTopic0", "libraryDesc5"):
                self.assertTrue(self.messages[lang].get(key), f"{lang}: missing {key}")
        self.assertIn("not a live literature search", self.messages["en"]["libraryIntro"])

    def test_library_field_filter_and_source_link(self):
        self.assertIn('id="library-category"', self.html)
        for category in ("all", "laser", "optics", "solar"):
            self.assertIn(f'value="{category}"', self.html)
        self.assertIn("libraryCategory.addEventListener('change', renderKnowledgeLibrary)", self.js)
        self.assertIn('entry.category === libraryCategory.value', self.js)
        self.assertIn('https://doi.org/10.1007/978-1-4419-1302-9', self.js)
        self.assertIn('link.rel = "noopener noreferrer"', self.js)
        for lang in ("en", "ar"):
            for key in ("libraryCategoryLabel", "libraryAll", "libraryLaser",
                        "libraryOptics", "librarySolar", "libraryOpenSource"):
                self.assertTrue(self.messages[lang].get(key), f"{lang}: missing {key}")

    def test_reference_registry_identifiers_and_conservative_status(self):
        for ref in ("LS-REF-001", "LS-REF-002", "LS-REF-003",
                    "LS-REF-004", "LS-REF-005"):
            self.assertIn(ref, self.js)
        self.assertIn('status:"doi_recorded"', self.js)
        self.assertIn('status:"bibliographic"', self.js)
        self.assertIn('provenance.textContent =', self.js)
        for lang in ("en", "ar"):
            for key in ("librarySourceId", "librarySourceStatus",
                        "libraryBibliographic", "libraryDoiRecorded"):
                self.assertTrue(self.messages[lang].get(key), f"{lang}: missing {key}")
        self.assertIn("not automated", self.messages["en"]["libraryDoiRecorded"])

    def test_university_campus_is_bilingual_and_links_to_existing_sections(self):
        self.assertIn('id="university-campus"', self.html)
        self.assertIn('id="campus-title"', self.html)
        self.assertIn('class="campus-sky"', self.html)
        self.assertEqual(self.html.split('id="university-campus"', 1)[1].split('id="agent-council"', 1)[0].count('class="campus-building"'), 7)
        for anchor in ('#knowledge-library', '#scientific-explorer',
                       '#research', '#mission-roadmap', '#integrity', '#cockpit'):
            self.assertIn(f'href="{anchor}"', self.html)
        for lang in ("en", "ar"):
            for key in ("navCampus", "missionCampus", "campusTitle",
                        "campusIntro", "campusSkyLabel", "campusFootnote",
                        "campusExplore"):
                self.assertTrue(self.messages[lang].get(key), f"{lang}: missing {key}")
            for i in range(1, 8):
                self.assertTrue(self.messages[lang].get(f"campusB{i}"))
                self.assertTrue(self.messages[lang].get(f"campusD{i}"))
        self.assertIn("no live campus session", self.messages["en"]["campusFootnote"])

    def test_no_private_login_claims(self):
        self.assertNotIn('type="password"', self.html)
        self.assertNotIn("<form", self.html.lower())
        self.assertIn("No account details are collected", self.html)

if __name__ == "__main__":
    unittest.main()
