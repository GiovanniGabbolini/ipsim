import unittest
from src.knowledge_graph.compare_functions.same_word_different_sense_phrase import same_word_different_sense_phrase


class TestSameWordDifferentMeaningPhrase(unittest.TestCase):

    def test_same_word_different_sense_phrase(self):
        v1 = "strawberry fields"
        v2 = "i like Strawberry"
        self.assertFalse(same_word_different_sense_phrase({'value': v1}, {'value': v2})['outcome'])

        v1 = "I am good!"
        v2 = "good luck"
        self.assertFalse(same_word_different_sense_phrase({'value': v1}, {'value': v2})['outcome'])

        v1 = "working all day"
        v2 = "i'm working hard"
        self.assertFalse(same_word_different_sense_phrase({'value': v1}, {'value': v2})['outcome'])

        v1 = "the river bank"
        v2 = "i went to the bank!"
        self.assertTrue(same_word_different_sense_phrase({'value': v1}, {'value': v2})['outcome'])

        v1 = ""
        v2 = "this should be really false"
        self.assertFalse(same_word_different_sense_phrase({'value': v1}, {'value': v2})['outcome'])
