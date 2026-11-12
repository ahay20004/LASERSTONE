"""Local runner for all G23 evidence-safety acceptance suites.

Run:
    python run_g23_evidence_safety.py

This runner is read-only and does not start simulators, GUIs, dashboards, or
modify production registries.
"""

import sys
import unittest

TEST_MODULES = (
    "test_g23_photochemcad_evidence_adapter",
    "test_g23_photochemcad_integration_gate",
    "test_g23_physical_spectral_evidence_engine",
    "test_g23_spectral_path_comparison",
    "test_g23_evidence_safety_repairs",
    "test_g23_strict_decision_path",
    "test_g23_legacy_provenance_audit",
)


def main() -> int:
    loader = unittest.defaultTestLoader
    suite = loader.loadTestsFromNames(TEST_MODULES)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
