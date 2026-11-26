import json
import unittest
from scientific_knowledge import knowledge_card
from equation_registry import REGISTRY

class KnowledgeTests(unittest.TestCase):
    def test_registry_coverage(self):
        for identifier, equation in REGISTRY.items():
            for language in ("ar", "en"):
                with self.subTest(identifier=identifier, language=language):
                    card = knowledge_card(identifier, language)
                    self.assertEqual(card["language"], language)
                    self.assertEqual(card["equation"]["expression"], equation.expression)
                    self.assertEqual(card["coefficient"], equation.coefficient)
                    self.assertTrue(card["concept"])
                    self.assertTrue(card["derivation"])
                    self.assertFalse(card["scientific_validation"])
                    json.dumps(card, allow_nan=False)
    def test_invalid_language(self):
        with self.assertRaises(ValueError):
            knowledge_card("vacuum_frequency", "invalid")
