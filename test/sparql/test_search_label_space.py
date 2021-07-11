import unittest
from src.sparql.search_label_space import _preprocess_label


class TestSearchLabelSpace(unittest.TestCase):

    def test_preprocess_label(self):
        self.assertEqual(_preprocess_label('blink-182'), 'blink-182')
        self.assertEqual(_preprocess_label('A B ci&d'), 'A B ci&d')
        self.assertEqual(_preprocess_label(
            "Guns 'n Roses"), "Guns \\\\'n Roses")
        self.assertEqual(_preprocess_label(
            'Guns "n Roses'), 'Guns \\\\\\"n Roses')
        self.assertEqual(_preprocess_label(
            '   AAA & \n d   bb .'), 'AAA d bb')
        self.assertEqual(_preprocess_label(
            '   AAA - d   bb '), 'AAA d bb')
