import unittest
from agent_confidentiality import export_context

class ConfidentialityTests(unittest.TestCase):
    def test_denies_confidential_even_with_allowlist(self):
        with self.assertRaises(PermissionError):
            export_context({"objective": "experiment"}, "physics",
                           classification="CONFIDENTIAL", approved_fields=["objective"])

    def test_guest_needs_explicit_approval(self):
        with self.assertRaises(PermissionError):
            export_context({"objective": "public audit"}, "guest",
                           classification="PUBLIC", approved_fields=["objective"], guest=True)

    def test_guest_cannot_receive_internal(self):
        with self.assertRaises(PermissionError):
            export_context({"objective": "internal audit"}, "guest",
                           classification="INTERNAL", approved_fields=["objective"],
                           guest=True, guest_approved=True)

    def test_secret_key_never_exported(self):
        with self.assertRaises(PermissionError):
            export_context({"api_key": "fake"}, "physics",
                           classification="PUBLIC", approved_fields=["api_key"])

    def test_secret_value_blocks_export(self):
        with self.assertRaises(PermissionError):
            export_context({"objective": "read confidential manuscript"}, "physics",
                           classification="PUBLIC", approved_fields=["objective"])

    def test_minimum_public_payload(self):
        result = export_context({"task_id": "T1", "objective": "test optical model",
                                 "private_notes": "do not share"}, "guest",
                                classification="PUBLIC", approved_fields=["task_id", "objective"],
                                guest=True, guest_approved=True)
        self.assertEqual(set(result["payload"]), {"task_id", "objective"})
        self.assertFalse(result["transmitted"])

if __name__ == "__main__":
    unittest.main()
