import unittest
from src.text_processing.preprocess_phrase import tokenize
from src.text_processing.preprocess_word import lower


class TestPreprocessPhrase(unittest.TestCase):

    def test_tokenize(self):

        phrase = "drippin' sweat"
        self.assertEqual(tokenize(phrase), [
                         'drippin', "'", 'sweat'])

        phrase = "i can't live without  you "
        self.assertEqual(tokenize(phrase), [
                         'i', "can't", 'live', 'without', 'you'])

        phrase = "i'm sickl \n \t no i            dont"
        self.assertEqual(tokenize(phrase), [
                         "i'm", "sickl", "no", "i", "dont"])

        phrase = "she ain't Perfect but yknow"
        self.assertEqual(tokenize(phrase), [
                         "she", "ain't", "Perfect", "but", "yknow"])

        phrase = "i, am. hey!"
        self.assertEqual(tokenize(phrase), [
                         "i", ",", "am", ".", "hey", "!"])

        phrase = "will.i.am"
        self.assertEqual(tokenize(phrase), ["will.i.am"])

        phrase = "/'/\/\A/'''/ a"
        self.assertEqual(tokenize(phrase), [
                         '/', "'", '/', '\\', '/', '\\', 'A', '/', "'", "'", "'", '/', 'a'])

        # Test it with arguments
        phrase = "she ain't Perfect but yknow"
        self.assertEqual(tokenize(phrase, funcs_word=[lower]), [
                         "she", "ain't", "perfect", "but", "yknow"])

        phrase = "i, Am. hey!"
        self.assertEqual(tokenize(phrase, funcs_word=[lower]), [
                         "i", ",", "am", ".", "hey", "!"])

        phrase = "i, am. hey!"
        self.assertEqual(tokenize(phrase, thr_length=4), [])
