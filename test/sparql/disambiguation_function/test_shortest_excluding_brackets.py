import unittest
from src.sparql.disambiguation_function.shortest_excluding_brackets import shortest_excluding_brackets


class TestShortestExcludingBrackets(unittest.TestCase):

    def test_shortest_excluding_brackets(self):
        l = ['AAAA', 'BBBB']
        self.assertEqual(shortest_excluding_brackets(l), 'AAAA')

        l = ['AA(AA)', 'BBBB']
        self.assertEqual(shortest_excluding_brackets(l), 'AA(AA)')

        l = ['AA(AAA', 'BBBB']
        self.assertEqual(shortest_excluding_brackets(l), 'BBBB')
