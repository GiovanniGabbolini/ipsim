import unittest
from src.sparql.preprocess_uri_name import preprocess_uri_name


class TestPreprocerssUriName(unittest.TestCase):

    def test_preprocess_uri_name(self):
        self.assertEqual(preprocess_uri_name('blink-182'), 'Blink-182')
        self.assertEqual(preprocess_uri_name('G-DRAGON'), 'G-DRAGON')
        self.assertEqual(preprocess_uri_name('A B ci&d'), 'A_B_Ci&d')
        self.assertEqual(preprocess_uri_name("Guns 'n Roses"), "Guns_'n_Roses")
        self.assertEqual(preprocess_uri_name(
            'Guns "n Roses'), 'Guns_%22n_Roses')
