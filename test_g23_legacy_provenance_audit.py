"""Acceptance tests for G23 legacy provenance audit."""

import unittest

from g23_legacy_provenance_audit import (
    audit_all_legacy_plants,
    audit_legacy_plant,
)
from plants_data import plants


class LegacyProvenanceAuditTests(unittest.TestCase):
    def test_all_legacy_records_require_provenance_upgrade(self):
        report = audit_all_legacy_plants()
        self.assertEqual(report["total_records"], len(plants))
        self.assertEqual(report["records_field_level_provenance_complete"], 0)
        for audit in report["audits"]:
            self.assertEqual(
                audit["promotion_status"],
                "PROVENANCE_UPGRADE_REQUIRED",
            )

    def test_current_reference_coverage_is_reported_not_assumed_complete(self):
        report = audit_all_legacy_plants()
        self.assertEqual(report["records_with_reference"], 6)
        self.assertEqual(report["records_without_reference"], 1)
        self.assertEqual(report["records_with_multiple_references"], 1)
        self.assertEqual(report["records_with_any_doi"], 0)

    def test_henna_reference_aliases_are_detected_as_multiple(self):
        henna = next(record for record in plants if record["name"] == "Henna")
        audit = audit_legacy_plant(henna)
        self.assertEqual(audit["canonical_name"], "Henna")
        self.assertEqual(audit["reference_count"], 2)
        self.assertEqual(
            audit["reference_status"],
            "MULTIPLE_REFERENCE_RECORDS_REQUIRE_RECONCILIATION",
        )

    def test_acacia_missing_reference_is_explicit(self):
        acacia = next(
            record for record in plants if record["name"] == "Acacia Nilotica"
        )
        audit = audit_legacy_plant(acacia)
        self.assertEqual(audit["reference_count"], 0)
        self.assertEqual(audit["reference_status"], "NO_REFERENCE_RECORD")

    def test_unresolved_units_are_not_promoted(self):
        audit = audit_legacy_plant(plants[0])
        for field in ("tau", "sigma_a", "eta", "knr"):
            self.assertIn(field, audit["unresolved_unit_fields"])


if __name__ == "__main__":
    unittest.main()
