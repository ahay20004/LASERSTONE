"""Regression checks for the public Hugging Face payload scanner."""
import tempfile
import unittest
from pathlib import Path

from cloud.huggingface.audit_public_payload import ALLOWED, inspect


class PublicPayloadAuditTests(unittest.TestCase):
    def test_sensitive_payloads_are_blocked(self):
        samples = {
            "credential assignment": 'HF_TOKEN = "not-a-real-token-value"',
            "local Windows path": r"C:\\Users\\Example\\Documents\\file.txt",
            "local POSIX home": "/home/example/private/file.txt",
            "external executable script": '<script src="https://example.org/remote.js"></script>',
            "embedded iframe": '<iframe src="about:blank"></iframe>',
            "private key": "-----BEGIN PRIVATE KEY-----\nplaceholder",
        }
        for label, payload in samples.items():
            with self.subTest(label=label), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                for name in ALLOWED:
                    (root / name).write_text(payload if name == "index.html" else "safe", encoding="utf-8")
                self.assertTrue(any(label in issue for issue in inspect(root)))

    def test_safe_static_payload_is_allowed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for name in ALLOWED:
                (root / name).write_text("Public LASERSTONE preview", encoding="utf-8")
            self.assertEqual(inspect(root), [])


if __name__ == "__main__":
    unittest.main()
