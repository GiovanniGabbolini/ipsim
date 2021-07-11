import unittest
import networkx as nx
from src.knowledge_graph.applicable_actions import applicable_actions_given_function
from src.features.used.album_uri_dbpedia import album_uri_dbpedia


class TestApplicableFunctions(unittest.TestCase):

    def test_applicable_actions_given_function(self):
        g = nx.DiGraph()

        g.add_node('a')
        g.nodes['a']['type'] = ['artist_uri_dbpedia']
        g.nodes['a']['value'] = 'a'

        g.add_node('b')
        g.nodes['b']['type'] = ['artist_uri_dbpedia']
        g.nodes['b']['value'] = 'b'

        g.add_node('c')
        g.nodes['c']['type'] = ['album_name']
        g.nodes['c']['value'] = 'c'

        g.add_node('d')
        g.nodes['d']['type'] = ['album_name']
        g.nodes['d']['value'] = 'd'

        g.add_node('e')
        g.nodes['e']['type'] = ['artist_name']
        g.nodes['e']['value'] = 'e'

        applied_actions = set([('c', 'a', 'e', 'c~album_uri_dbpedia')],)

        actions = applicable_actions_given_function(
            g, applied_actions, album_uri_dbpedia)

        self.assertEqual(len(actions), 3)
        self.assertEqual(actions[0], (album_uri_dbpedia,
                                      ('c', 'b', 'e')))
        self.assertEqual(actions[1], (album_uri_dbpedia,
                                      ('d', 'a', 'e')))
        self.assertEqual(actions[1], (album_uri_dbpedia,
                                      ('d', 'a', 'e')))
