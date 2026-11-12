"""Acceptance tests for the Paper 1 authoritative master contract."""

import json
import unittest
from pathlib import Path

from g23_manuscript_contract import (
    MASTER_FILENAME,
    validate_master_file,
    validate_master_manuscript,
)


ROOT = Path(__file__).resolve().parent


def load_directive():
    return json.loads(
        (ROOT / "LASERSTONE_PAPER1_DIRECTIVE.json").read_text(encoding="utf-8")
    )


class Paper1MasterContractTests(unittest.TestCase):
    def test_authoritative_master_passes_contract(self):
        result = validate_master_file(load_directive(), ROOT)
        self.assertTrue(result["valid"])
        self.assertEqual(result["status"], "MASTER_CONTRACT_PASSED")
        self.assertEqual(result["master_filename"], MASTER_FILENAME)

    def test_title_drift_is_blocked(self):
        directive = load_directive()
        manuscript = (ROOT / MASTER_FILENAME).read_text(encoding="utf-8")
        altered = manuscript.replace(
            f"# {directive['title']}",
            "# Different title",
            1,
        )
        result = validate_master_manuscript(directive, altered)
        self.assertFalse(result["valid"])
        self.assertIn(
            "master manuscript title does not match Research Directive",
            result["errors"],
        )

    def test_missing_results_section_is_blocked(self):
        directive = load_directive()
        manuscript = (ROOT / MASTER_FILENAME).read_text(encoding="utf-8")
        altered = manuscript.replace("## 3. Results", "## Results removed", 1)
        result = validate_master_manuscript(directive, altered)
        self.assertFalse(result["valid"])
        self.assertTrue(
            any("## 3. Results" in error for error in result["errors"])
        )

    def test_multiple_master_policy_is_blocked(self):
        directive = load_directive()
        directive["master_policy"] = "MULTIPLE_MASTERS"
        manuscript = (ROOT / MASTER_FILENAME).read_text(encoding="utf-8")
        result = validate_master_manuscript(directive, manuscript)
        self.assertFalse(result["valid"])
        self.assertTrue(
            any("one-master policy" in error for error in result["errors"])
        )


if __name__ == "__main__":
    unittest.main()
