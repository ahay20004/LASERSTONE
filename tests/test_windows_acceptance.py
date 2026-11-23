import unittest
from unittest.mock import patch
import laserstone_windows_acceptance as a

class WindowsAcceptanceTests(unittest.TestCase):
    def test_non_windows_never_certifies(self):
        with patch.object(a.platform, "system", return_value="Linux"):
            result = a.collect()
        self.assertFalse(result["host_is_windows"])
        self.assertFalse(result["synthetic_software_checks_passed"])
        self.assertEqual(result["operational_readiness"], "NOT_ESTABLISHED")

    def test_even_passing_windows_checks_do_not_certify_gui(self):
        with patch.object(a.platform, "system", return_value="Windows"), patch.object(
            a, "run_check", return_value={"status": "PASS", "name": "mock"}
        ):
            result = a.collect()
        self.assertTrue(result["synthetic_software_checks_passed"])
        self.assertFalse(result["gui_runtime_verified"])
        self.assertEqual(result["operational_readiness"], "NOT_ESTABLISHED")
