import json
import unittest
from scientific_pathways import build_pathways, PATHWAYS

class PathwayTests(unittest.TestCase):
    def test_shared_contract(self):
        for uncertainty in (None, {"vacuum_wavelength":{"value":1,"unit":"nm"}}):
            payload = build_pathways("photon_energy_wavelength",
                {"vacuum_wavelength":{"value":532,"unit":"nm"}},
                uncertainties=uncertainty, independent=uncertainty is not None,
                output_unit="eV")
            self.assertEqual(set(payload["pathways"]),set(PATHWAYS))
            result = payload["shared_result"]
            for pathway in payload["pathways"].values():
                self.assertTrue(set(pathway["focus"]) <= set(result))
            self.assertAlmostEqual(float(result["result"]["raw_value"]),2.3305300457,places=8)
            self.assertFalse(payload["scientific_validation"])
            self.assertFalse(payload["release_authorized"])
            json.dumps(payload,allow_nan=False)
