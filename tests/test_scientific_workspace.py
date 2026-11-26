import json
import unittest
from scientific_workspace import build_workspace
from scientific_pathways import PATHWAYS

class WorkspaceTests(unittest.TestCase):
    def test_shared_calculation(self):
        inputs = {"vacuum_wavelength":{"value":532,"unit":"nm"}}
        baseline = build_workspace("photon_energy_wavelength",inputs,output_unit="eV")
        for language in ("ar","en"):
            for pathway in PATHWAYS:
                payload = build_workspace("photon_energy_wavelength",inputs,
                    language=language,pathway=pathway,output_unit="eV")
                self.assertEqual(payload["shared_result"],baseline["shared_result"])
                self.assertEqual(payload["knowledge"]["language"],language)
                self.assertEqual(payload["pathway"],pathway)
                self.assertFalse(payload["scientific_validation"])
                json.dumps(payload,allow_nan=False)
    def test_unknown_role(self):
        with self.assertRaises(ValueError):
            build_workspace("vacuum_frequency",{},pathway="invalid")
