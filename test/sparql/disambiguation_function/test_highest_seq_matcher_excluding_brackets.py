import unittest
from src.sparql.disambiguation_function.highest_seq_matcher_excluding_brackets import highest_seq_matcher_excluding_brackets


class TestHighestSeqMatcherExcludingBrackets(unittest.TestCase):

    def test_highest_seq_matcher_excluding_brackets(self):
        ref = "reference string"
        s1 = "reference_&&&_string_ppppp"
        s2 = "some_other_unrelated_string"
        self.assertEqual(
            highest_seq_matcher_excluding_brackets([s1, s2], ref), s1)
