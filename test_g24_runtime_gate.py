import unittest
from unittest.mock import patch
import sys
import types
from laserstone_governor import laserstone_governor_decision

class RuntimeGateTests(unittest.TestCase):
    def test_governor_high_scores(self):
        self.assertTrue(laserstone_governor_decision({"intelligence_summary":{"intelligence_score":100},"scientific_confidence_score":100}).startswith("HOLD"))

    def test_launcher_preparation(self):
        gateway=types.ModuleType("entry_gateway")
        gateway.open_entry_gateway=lambda *a: None
        executive=types.ModuleType("executive_summary_engine")
        executive.generate_executive_summary=lambda *a: None
        main=types.ModuleType("main")
        rank=types.ModuleType("global_ranking_engine")
        rank.rank_plants=lambda p:p
        with patch.dict(sys.modules,{"entry_gateway":gateway,"executive_summary_engine":executive,"main":main,"global_ranking_engine":rank}):
            from safe_dashboard_launcher import prepare_dashboard_plants
            raw=[{"name":"synthetic"}]
            self.assertEqual(prepare_dashboard_plants(raw),[])
            main.analyze_plant=lambda p:p
            self.assertEqual(prepare_dashboard_plants(raw),[])
            main.analyze_plant=lambda p:dict(p,evidence_decision={"decision":"HOLD"})
            self.assertEqual(prepare_dashboard_plants(raw),[])
            main.analyze_plant=lambda p:dict(p,valid=True,evidence_decision={"decision":"HOLD"})
            self.assertEqual(len(prepare_dashboard_plants(raw)),1)
            rank.rank_plants=lambda p: (_ for _ in ()).throw(RuntimeError("synthetic ranking failure"))
            self.assertEqual(prepare_dashboard_plants(raw),[])

