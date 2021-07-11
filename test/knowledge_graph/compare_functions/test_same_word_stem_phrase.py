import unittest
from src.knowledge_graph.compare_functions.same_word_stem_phrase import same_word_stem_phrase


class TestSameWordStemPhrase(unittest.TestCase):

    def test_same_word_stem_phrase(self):
        v1 = "dancing in the dark"
        v2 = "she dances really good"
        self.assertTrue(same_word_stem_phrase(v1, v2))

        v1 = "dancin"
        v2 = "really good"
        self.assertFalse(same_word_stem_phrase(v1, v2))

        v1 = "dancin"
        v2 = "Dancin really"
        self.assertFalse(same_word_stem_phrase(v1, v2))
