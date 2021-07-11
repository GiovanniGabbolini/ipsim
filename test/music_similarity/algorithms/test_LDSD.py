import unittest
from unittest.mock import patch
import networkx as nx
from src.music_similarity.algorithms.LDSD import _cd, _cd_n, _cii, _cio, _cii_n, _cio_n

"""
"""


class TestLDSD(unittest.TestCase):

    def test_LDSD(self):
        g = nx.MultiDiGraph()
        g.add_node('r1')
        g.add_node('r2')
        g.add_node('r3')
        g.add_node('r4')
        g.add_edge('r1', 'r2', type='l1')
        g.add_edge('r1', 'r2', type='l2')
        g.add_edge('r1', 'r3', type='l2')
        g.add_edge('r1', 'r4', type='l3')
        g.add_edge('r2', 'r1', type='l1')
        g.add_edge('r2', 'r4', type='l3')

        self.assertEqual(_cd(g, 'l1', 'r1', 'r2'), 1)
        self.assertEqual(_cd(g, 'l1', 'r1', 'r3'), 0)

        self.assertEqual(_cd_n(g, 'l1', 'r1'), 1)
        self.assertEqual(_cd_n(g, 'l2', 'r1'), 2)

        self.assertEqual(_cii(g, 'l2', 'r2', 'r3'), 1)
        self.assertEqual(_cii(g, 'l2', 'r2', 'r4'), 0)

        self.assertEqual(_cio(g, 'l3', 'r1', 'r2'), 1)
        self.assertEqual(_cio(g, 'l2', 'r1', 'r2'), 0)

        self.assertEqual(_cii_n(g, 'l2', 'r2'), 1)
        self.assertEqual(_cii_n(g, 'l1', 'r2'), 0)

        self.assertEqual(_cio_n(g, 'l3', 'r1'), 1)
        self.assertEqual(_cio_n(g, 'l2', 'r1'), 0)
