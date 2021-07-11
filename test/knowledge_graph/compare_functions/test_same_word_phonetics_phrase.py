import unittest
from src.knowledge_graph.compare_functions.same_word_phonetics_phrase import same_word_phonetics_phrase


class TestSameWordPhoneticsPhrase(unittest.TestCase):

    def test_same_word_phonetics_phrase(self):
        v1 = "strawberry wright"
        v2 = "you r Right man"
        self.assertTrue(same_word_phonetics_phrase(v1, v2))

        v1 = "I am good!"
        v2 = "good luck"
        self.assertFalse(same_word_phonetics_phrase(v1, v2))

        v1 = "I am GOOD!"
        v2 = "good luck"
        self.assertFalse(same_word_phonetics_phrase(v1, v2))
