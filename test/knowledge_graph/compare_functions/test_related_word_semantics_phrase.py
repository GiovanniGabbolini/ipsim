import unittest
from src.knowledge_graph.compare_functions.related_word_semantics_phrase import related_word_semantics_phrase


class TestRelatedWordSemanticsPhrase(unittest.TestCase):

    def test_related_word_semantics_phrase(self):
        v1 = "to the moon"
        v2 = "the sun"
        self.assertTrue(related_word_semantics_phrase({'value': v1}, {'value': v2}))
