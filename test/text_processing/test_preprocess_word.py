import unittest
from src.text_processing.preprocess_word import stem


class TestPreprocessPhrase(unittest.TestCase):

    def test_stem(self):
        self.assertEqual(stem('fishing'), 'fish')
        self.assertEqual(stem('FISHING'), 'fish')
        self.assertEqual(stem('Fishing'), 'fish')
        self.assertEqual(stem('disposable'), 'dispos')
        self.assertEqual(stem('disposed'), 'dispos')
