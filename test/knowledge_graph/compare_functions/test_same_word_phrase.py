import unittest
from src.knowledge_graph.compare_functions.same_word_phrase import same_word_phrase


class TestSameWordPhrase(unittest.TestCase):

    def test_same_word_phrase(self):
        v1 = "strawberry fields"
        v2 = "i like Strawberry"
        self.assertTrue(same_word_phrase(v1, v2))

        v1 = "I am good!"
        v2 = "good luck"
        self.assertTrue(same_word_phrase(v1, v2))

        v1 = "working all day"
        v2 = "i'm working hard"
        self.assertTrue(same_word_phrase(v1, v2))

        v1 = "mark the one"
        v2 = "osullivan mark"
        self.assertTrue(same_word_phrase(v1, v2))

        v1 = "Barry O'Sullivan"
        v2 = "Linda O'Sullivan"
        self.assertTrue(same_word_phrase(v1, v2))

        v1 = "Barry dajndanajw"
        v2 = "Linda dajndanajw"
        self.assertTrue(same_word_phrase(v1, v2))

        v1 = "barry!!E1$"
        v2 = "barry!!E121$$"
        self.assertTrue(same_word_phrase(v1, v2))

        v1 = "only"
        v2 = "only"
        self.assertTrue(same_word_phrase(v1, v2))
