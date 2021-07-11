import unittest
from src.knowledge_graph.construct_graph import construct_graph
from src.knowledge_graph.resolve_compare_function import resolve_compare_function, _dict
from src.knowledge_graph.applicable_actions import MockedActionsSupplier


"""Tests if every first-level key of the dictionary in _dict specified in resolve_compare_function
   is hit, in case we are dealing with two graphs at their maximum possible extension.
   In practice, verifies that every segue that we consider (adding a compare function key in that dictionary)
   is in effect ever possibly obtainable, under the assumption that the compare functions work properly).

   Moreover, it verifies that every compare function in _dict (last level) is effectively assigned,
   in case we are dealing with two graphs at their maximum possible extension.
"""


class TestApplicabilityCompareFunctions(unittest.TestCase):

    def _get_prescribed_values(self, o):
        if type(o) == dict:
            l = []
            for i in o.values():
                l += self._get_prescribed_values(i)
            return l
        elif type(o) == list:
            return [f.__name__ for f in o]

    def test_reachability_compare_functions(self):

        d = {
            'track_uri_spotify': 'bla',
            'track_name': 'bla',
            'artist_name': 'bla',
            'artist_uri_spotify': 'bla',
            'album_name': 'bla',
            'album_uri_spotify': 'bla',
        }

        g = construct_graph(d, supplier=MockedActionsSupplier())

        d = {}
        funcs_assigned = []
        for node_g1 in g.nodes():
            for node_g2 in g.nodes():
                n1 = g.nodes()[node_g1]
                n2 = g.nodes()[node_g2]
                funcs = resolve_compare_function(n1, n2)
                if len(funcs) > 0:
                    d[(n1['type'], n2['type'])] = funcs
                    funcs_assigned += [f.__name__ for f in funcs]

        funcs_prescribed = set(self._get_prescribed_values(_dict))
        funcs_assigned = set(funcs_assigned)

        self.assertEqual(funcs_prescribed, funcs_assigned)
        self.assertEqual(set(d.keys()), set(_dict.keys()))
