"""Acceptance tests for safe plant-to-compound evidence linkage."""

import copy
import unittest

from g23_compound_evidence_linker import link_plant_to_compound_evidence
from photochemcad_evidence_adapter import normalize_photochemcad_record
from plants_data import plants


QUERCETIN = normalize_photochemcad_record({
    "photochemcad_id": "FL109",
    "name": "Quercetin",
    "compound_class": "Flavonol",
    "lambda_abs_nm": 256,
    "epsilon_M_cm": 18700,
    "solvent": "MeOH",
    "source_url": "https://www.photochemcad.com/databases/flavonoids/quercetin",
})


class CompoundEvidenceLinkerTests(unittest.TestCase):
    def test_moringa_links_to_quercetin_as_supporting_evidence_only(self):
        moringa = next(record for record in plants if record["name"] == "Moringa")
        before = copy.deepcopy(moringa)
        result = link_plant_to_compound_evidence(moringa, [QUERCETIN])

        self.assertEqual(result["status"], "SUPPORTING_COMPOUND_EVIDENCE_ONLY")
        self.assertEqual(result["match_count"], 1)
        self.assertFalse(result["substitution_allowed"])
        self.assertEqual(moringa, before)

    def test_compound_evidence_does_not_replace_extract_values(self):
        moringa = next(record for record in plants if record["name"] == "Moringa")
        result = link_plant_to_compound_evidence(moringa, [QUERCETIN])

        self.assertEqual(moringa["lambda_abs"], 410)
        self.assertEqual(result["matches"][0]["lambda_abs_nm"], 256.0)
        self.assertIn(
            "replace plant-extract lambda_abs",
            result["prohibited_use"],
        )

    def test_unmatched_active_compound_remains_unlinked(self):
        hibiscus = next(record for record in plants if record["name"] == "Hibiscus")
        result = link_plant_to_compound_evidence(hibiscus, [QUERCETIN])
        self.assertEqual(result["status"], "NO_EXACT_COMPOUND_EVIDENCE_MATCH")
        self.assertEqual(result["match_count"], 0)

    def test_multiple_exact_records_require_review(self):
        second = copy.deepcopy(QUERCETIN)
        second["photochemcad_id"] = "FL109-ALT"
        result = link_plant_to_compound_evidence(
            next(record for record in plants if record["name"] == "Moringa"),
            [QUERCETIN, second],
        )
        self.assertEqual(
            result["status"],
            "MULTIPLE_COMPOUND_RECORDS_REVIEW_REQUIRED",
        )
        self.assertFalse(result["substitution_allowed"])


if __name__ == "__main__":
    unittest.main()
