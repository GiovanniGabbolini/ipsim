import unittest
from src.knowledge_graph.construct_graph import construct_graph
from src.features import used
from src.knowledge_graph.applicable_actions import MockedActionsSupplier


"""Tests whether it is possible to apply every functions at least once in the folders 
   features.used. The test build a graph assuming that every function
   produces always a non-null result
   
   E.g: If the types are badly defined, I can have a function argument of a type which is never generated
"""


class TestReachabilityFeatures(unittest.TestCase):

    def test_reachability_features(self):

        d = {
            'track_uri_spotify': 'bla',
            'track_name': 'bla',
            'artist_name': 'bla',
            'artist_uri_spotify': 'bla',
            'album_name': 'bla',
            'album_uri_spotify': 'bla',
        }

        g = construct_graph(d, supplier=MockedActionsSupplier())

        reached_functions = set()
        for n in g.nodes():
            if '~' in n:
                reached_functions.add(n.split('~')[-1].split('-')[0])

        defined_functions = used.__all__
        self.assertEqual(set(defined_functions), set(reached_functions))
