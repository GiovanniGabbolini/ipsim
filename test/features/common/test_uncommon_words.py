import unittest
from src.features.used import uncommon_words


class TestUncommonWords(unittest.TestCase):

    def test_uncommon_words(self):
        c = "\nI\nmiss\n\n"
        self.assertEqual(uncommon_words(c), None)

        c = "bla Blaa"
        self.assertEqual(uncommon_words(c), ['blaa'])

        c = "!!!drippin'???!!!!"
        self.assertEqual(uncommon_words(c), ["drippin"])
